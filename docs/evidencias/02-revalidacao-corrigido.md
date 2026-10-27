# Teste 2: Validação da correção

> Harness: Claude Code 2.1.311 (Claude Code) · sessão nova, modo não interativo (`claude -p`), aberta na pasta do projeto · 2026-10-27 09:18

## Prompt

```text
Corrigi o login. Faça uma nova varredura em lab/app_corrigido.py e confirme se o SQL Injection foi mitigado. Use o mesmo formato de relatório da análise anterior.
```

## Resposta do agente

Parabéns, a correção ficou muito boa. 🎉 Refiz a análise em `lab/app_corrigido.py`. O contexto é o mesmo: app de login em Python + SQLite, só na sua máquina, banco em memória e entrada pelo terminal.

**Sobre o teste:** tentei rodar `python lab/testar_injecao.py`, mas a execução não foi liberada nesta sessão. Então esta revalidação é só uma **análise estática**, feita lendo o código. Vale você rodar o script para confirmar na prática (instruções no fim).

## 1. SQL Injection: mitigado ✅

**Onde:** `lab/app_corrigido.py:47`

```python
cur.execute("SELECT salt, hash FROM usuarios WHERE usuario = ?", (usuario,))
```

**Por que resolve a causa raiz:** antes, o texto digitado era colado dentro do comando SQL, e o banco não conseguia separar código de dado. Agora o comando vai com o marcador `?` e o valor vai separado, no segundo argumento. O driver trata esse valor sempre como dado. Uma aspa digitada continua sendo só um caractere e nunca fecha a string.

Conferi todos os pontos do arquivo que falam com o banco:

| Linha | Comando | Situação |
|-------|---------|----------|
| 30-32 | `CREATE TABLE` | Texto fixo, sem entrada do usuário |
| 35-38 | `INSERT` | Parametrizado com `?` |
| 47 | `SELECT` do login | Parametrizado com `?` |

Não sobrou nenhuma f-string, `%` ou `+` montando SQL. Tem mais uma melhoria: a senha saiu do `WHERE`. Agora você busca o usuário só pelo nome e compara o hash no Python. Assim a senha nem chega perto da query.

**O que acontece com os ataques do relatório anterior:**
- `admin' --` como usuário: o banco procura um usuário chamado literalmente `admin' --`. Ele não existe, então o login é **negado**.
- `' OR '1'='1` como senha: vira só texto, que gera um hash diferente do salvo. Login **negado**.

## 2. Falhas secundárias da análise anterior

| Falha anterior | Situação |
|----------------|----------|
| Senha em texto puro (CWE-256) | ✅ Resolvida. PBKDF2-HMAC-SHA256 com salt aleatório de 16 bytes por usuário, e comparação com `hmac.compare_digest` (tempo constante) |
| Senha no log (CWE-532) | ✅ Resolvida. O `print` de debug foi removido |

## 3. Pontos novos (baixa severidade, nenhum bloqueia)

Achei três detalhes. Nenhum é SQL Injection. São ajustes para deixar o código no nível de produção:

1. **Iterações do PBKDF2 desatualizadas** (`lab/app_corrigido.py:18`). O comentário cita 310.000 como recomendação da OWASP. Esse era o número de 2021. O OWASP Password Storage Cheat Sheet atual recomenda **600.000** para PBKDF2-HMAC-SHA256. Na sua tabela original eu tinha sugerido `bcrypt`/`argon2`. O PBKDF2 da biblioteca padrão também é aceitável, só precisa subir o número.
2. **Diferença de tempo que revela se o usuário existe** (`lab/app_corrigido.py:49-50`, CWE-208). Se o usuário não existe, a função retorna na hora. Se existe, ela calcula 310 mil rodadas de hash. Medindo o tempo de resposta, um atacante descobre quais nomes de usuário são válidos, mesmo com a mensagem de erro genérica. Pista para corrigir: faça a função gastar o mesmo tempo nos dois caminhos.
3. **Reforços que já estavam na lista:** limite de tentativas (CWE-307) e usar `getpass` no lugar de `input()` para a senha não aparecer na tela. As senhas fixas no código (linha 33) são aceitáveis aqui porque são só dados de exemplo do lab.

### Relatório de análise

| Campo          | Valor |
|----------------|-------|
| Alvo           | `lab/app_corrigido.py`, função `login()` (linha 47) |
| Ambiente       | Laboratório local, sem exposição de rede, banco em memória |
| Vulnerabilidade| SQL Injection (+ senha em texto puro, + senha no log) |
| Referências    | CWE-89, CWE-256, CWE-532; OWASP Injection; MITRE ATT&CK T1190 (se exposto); CAPEC-66 |
| Impacto        | Alto: login como qualquer usuário, inclusive admin, sem senha |
| Probabilidade  | Baixa: só acessível localmente pelo terminal |
| Severidade     | Média (Crítica se publicado na internet) |
| Correção       | Consulta parametrizada com `?` e valores passados separados ao `execute()` |
| Status         | **Mitigado** (antes: Vulnerável). Confirmado por análise estática; falta rodar o `testar_injecao.py` |

Mantive impacto, probabilidade e severidade iguais ao relatório anterior para dar para comparar o antes e o depois. Elas descrevem a falha original. O que mudou é o Status. As três falhas da seção 3 são novas, ficam como risco residual de severidade Baixa e não entram nesta linha.

### Como confirmar na prática

Na raiz do projeto, rode:

```
python lab/testar_injecao.py
```

O resultado esperado é `VULNERÁVEL` para o `app.py` e `MITIGADO` para o `app_corrigido.py`, com os quatro casos `OK`. Se der diferente, me mande a saída que eu olho.

Se quiser praticar mais, os labs de SQL Injection e de *username enumeration* (o item 2 acima) da PortSwigger Web Security Academy são gratuitos.

Pergunta para checar o aprendizado: com as suas palavras, por que a mensagem "Usuário ou senha inválidos" sozinha não impede que alguém descubra quais usuários existem?

