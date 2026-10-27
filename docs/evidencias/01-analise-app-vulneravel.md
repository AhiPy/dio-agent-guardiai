# Teste 1: Análise do app vulnerável

> Harness: Claude Code 2.1.311 (Claude Code) · sessão nova, modo não interativo (`claude -p`), aberta na pasta do projeto · 2026-10-27 09:17

## Prompt

```text
Atue como especialista em AppSec. Analise o arquivo lab/app.py, que é um app de login de laboratório meu, rodando só na minha máquina. Encontre a falha, explique como ela seria explorada, cite a técnica do MITRE ATT&CK e me oriente a reescrever o código.
```

## Resposta do agente

Li o `lab/app.py`. É um app de login em Python + SQLite, roda só na sua máquina, com banco em memória e entrada pelo terminal. Encontrei uma falha principal e duas secundárias. Vou da mais grave para a menos grave.

## 1. SQL Injection no login (a principal)

**Onde:** `lab/app.py:31`, na função `login()`

```python
query = f"SELECT * FROM usuarios WHERE usuario = '{usuario}' AND senha = '{senha}'"
```

**Causa raiz:** o texto que a pessoa digita é colado direto dentro do comando SQL. Para o banco, não existe diferença entre o que é **código** (o SQL que você escreveu) e o que é **dado** (o que o usuário digitou). Se a pessoa digitar uma aspa `'`, ela fecha a string e passa a escrever SQL junto com você.

**Referências:**
- **CWE-89:** SQL Injection
- **OWASP Top 10:** Injection (A03 na edição 2021, A05 na edição 2025)
- **MITRE ATT&CK:** **T1190, Exploit Public-Facing Application**. Um detalhe importante: o ATT&CK descreve o *comportamento do atacante*, não o tipo de bug. A T1190 só se aplica de verdade quando o app está exposto na rede ou na internet. No seu cenário local não existe "aplicação pública", então a T1190 descreve o que *aconteceria* se esse código fosse publicado. Para catalogar o padrão de ataque em si, a referência mais precisa é o CAPEC-66 (SQL Injection), também mantido pelo MITRE.

### Como seria explorado

O atacante controla os dois campos. O objetivo dele é mudar o sentido da cláusula `WHERE` para que ela fique verdadeira sem a senha certa.

Exemplo mínimo para o seu lab:

```
Usuário: admin' --
Senha:   qualquercoisa
```

A query que chega ao banco fica assim:

```sql
SELECT * FROM usuarios WHERE usuario = 'admin' --' AND senha = 'qualquercoisa'
```

O `'` fecha a string do usuário e o `--` inicia um comentário em SQL. Com isso, **toda a checagem de senha é ignorada**. Resultado: login como `admin` sem saber a senha. Como o seu código imprime a query (`[debug]`), você vai ver isso acontecer na tela.

## 2. Senhas em texto puro

**Onde:** `lab/app.py:21-24`. **CWE-256** (Plaintext Storage of a Password), categoria OWASP *Cryptographic Failures*.

Se alguém conseguir ler a tabela, seja por injection, por backup vazado ou por acesso ao arquivo, já tem todas as senhas prontas. E como muita gente repete senha, o estrago vai além do seu app.

## 3. Log que expõe a senha

**Onde:** `lab/app.py:32`. **CWE-532** (Sensitive Information in Log File).

O `print` de debug mostra a senha digitada na tela. Em um sistema real, isso iria para um arquivo de log. Esse ponto não estava marcado no arquivo, mas é um vazamento real.

## Avaliação de risco (falha 1)

- **Impacto: Alto.** Permite entrar como qualquer usuário, inclusive o admin, sem senha (quebra a confidencialidade e o controle de acesso). Não marquei como Crítico porque o `cursor.execute()` do SQLite não roda vários comandos de uma vez, o que limita ataques como `DROP TABLE`.
- **Probabilidade: Baixa.** O app só roda em `localhost`, com banco em memória e entrada pelo terminal. Só você consegue digitar ali.
- **Severidade: Média** (Alto × Baixa).

⚠️ O mesmo código atrás de um formulário web na internet passaria a ter probabilidade **Alta** e severidade **Crítica**. É técnica conhecida, sem autenticação, com ferramentas públicas. Por isso a correção vale mesmo em código de estudo.

## Como reescrever (a direção)

**Correção principal: consulta parametrizada.** Em vez de montar a string, você escreve o SQL com marcadores `?` e passa os valores **separados**, como segundo argumento do `execute()`. O driver envia os valores como dado puro, então uma aspa digitada continua sendo só um caractere e nunca vira SQL. Isso resolve a causa raiz, não só o sintoma.

Dica: o seu próprio arquivo já faz isso certo em um lugar. Olhe o `executemany` na linha 22 e compare com a linha 31. 😉

**Reforços (defesa em profundidade):**
1. **Hash de senha:** guarde o hash, não a senha. Use `bcrypt` ou `argon2-cffi`. No login, busque o usuário **só pelo nome** e compare a senha digitada com o hash usando a função de verificação da biblioteca.
2. **Remova o `print` da query**, ou pelo menos não imprima a senha.
3. **Validação de entrada** (tamanho máximo, caracteres permitidos) e **limite de tentativas**. São camadas extras, não substituem a parametrização.

### Como validar

Depois de reescrever, repita o teste com `admin' --`. O login tem que **falhar**. Teste também com `admin` / `S3nh@Forte!`, que tem que **funcionar**.

### Relatório de análise

| Campo          | Valor |
|----------------|-------|
| Alvo           | `lab/app.py`, função `login()` (linha 31) |
| Ambiente       | Laboratório local, sem exposição de rede, banco em memória |
| Vulnerabilidade| SQL Injection (+ senha em texto puro, + senha no log) |
| Referências    | CWE-89, CWE-256, CWE-532; OWASP Injection; MITRE ATT&CK T1190 (se exposto); CAPEC-66 |
| Impacto        | Alto: login como qualquer usuário, inclusive admin, sem senha |
| Probabilidade  | Baixa: só acessível localmente pelo terminal |
| Severidade     | Média (Crítica se publicado na internet) |
| Correção       | Consulta parametrizada com `?` e valores passados separados ao `execute()` |
| Status         | Vulnerável |

Para fixar o aprendizado: rode `python lab/app.py` e teste o `admin' --` **antes** de corrigir. Ver o bypass acontecer muda a forma como você enxerga o código. Depois tente reescrever e me mande a nova versão, que eu refaço a análise e atualizo o Status. Se travar, posso mostrar o trecho corrigido com comentários.

Para praticar mais, os labs de SQL Injection da PortSwigger Web Security Academy são gratuitos e muito bons.

Pergunta rápida para checar: com as suas palavras, por que o `?` impede o ataque e escapar as aspas "na mão" não seria a mesma coisa?

