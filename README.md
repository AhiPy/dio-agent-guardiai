# 🛡️ DIO Agent + GuardiAI: mentor de análise de vulnerabilidades

> Especialização do [DIO Agent](https://github.com/digitalinnovationone/dio-agent) para conduzir análises de segurança como um profissional de AppSec, feita só com arquivos Markdown, sem treinar nenhum modelo.

Projeto do Desafio de Projeto da [DIO](https://dio.me) em que o agente original, um mentor de estudos, ganha uma skill, uma base de conhecimento e um trecho de persona voltados para segurança. O guia original do DIO Agent foi preservado em [`docs/README-original.md`](docs/README-original.md).

---

## 🎯 A especialização, e por quê

Um chat genérico, ao receber um código vulnerável, costuma responder direto com a correção. A resposta pode estar certa, mas pula o que um profissional de segurança faz de verdade:

1. **Entender o contexto** antes de agir: o que é o alvo, onde roda, se está exposto, se o teste é autorizado.
2. **Medir o risco**: a mesma falha tem severidade diferente num `localhost` de laboratório e num servidor na internet.
3. **Corrigir e validar**: só está resolvido quando uma nova análise confirma a mitigação.

A skill `vulnerability-analysis` ensina esse raciocínio ao agente. Escolhi esse foco porque é exatamente o fluxo de trabalho de um analista de segurança (triagem, classificação de severidade, recomendação, validação) e porque o agente continua sendo um **mentor**: ele explica a causa raiz e pergunta antes de agir, em vez de só entregar uma lista de problemas.

## 🗂️ Arquivos criados e alterados

| Arquivo | Tipo | O que faz |
|---------|------|-----------|
| [`skills/vulnerability-analysis/SKILL.md`](skills/vulnerability-analysis/SKILL.md) | **Criado** | Roteiro de 6 etapas que o agente segue: contexto, identificação, exploração, avaliação de risco, correção e validação, com regras defensivas |
| [`skills/vulnerability-analysis/README.md`](skills/vulnerability-analysis/README.md) | **Criado** | Explica a skill para pessoas |
| [`agent/knowledge/security-basics.md`](agent/knowledge/security-basics.md) | **Criado** | Vulnerabilidade, ameaça, risco, tríade CIA, escala de impacto e probabilidade, matriz de severidade, referências (CWE, OWASP, MITRE ATT&CK) e boas práticas |
| [`agent/persona.md`](agent/persona.md) | **Alterado** | Nova seção "Modo especialista em segurança" |
| [`AGENTS.md`](AGENTS.md) | **Alterado** | Linha da skill na tabela e o novo arquivo na base de conhecimento |
| [`skills/README.md`](skills/README.md) | **Alterado** | Skill adicionada ao índice |
| [`lab/app.py`](lab/app.py) | **Criado** | Login vulnerável a SQL Injection (consulta montada com f-string, senhas em texto puro) |
| [`lab/app_corrigido.py`](lab/app_corrigido.py) | **Criado** | Mesmo login com consulta parametrizada e senhas com hash + salt (PBKDF2) |
| [`lab/testar_injecao.py`](lab/testar_injecao.py) | **Criado** | Teste automático que prova a mitigação |
| [`docs/roteiro-de-testes.md`](docs/roteiro-de-testes.md) | **Criado** | Prompts usados para testar o agente e o que conferir em cada resposta |
| [`docs/evidencias/`](docs/evidencias/README.md) | **Criado** | Respostas reais do agente em cada teste (`.md`) e os prints (`.png`) |

## ✨ Melhoria escolhida: relatório em formato fixo

Das ideias de evolução do desafio, escolhi **fazer a análise sair sempre no mesmo formato**, com impacto, probabilidade e severidade. Toda análise termina com esta tabela:

| Campo | Exemplo (`lab/app.py`) |
|-------|------------------------|
| Alvo | `lab/app.py`, função `login()` |
| Ambiente | Laboratório local, sem exposição |
| Vulnerabilidade | SQL Injection no login |
| Referências | CWE-89, OWASP Injection, MITRE ATT&CK T1190 |
| Impacto | Alto: acesso a qualquer conta sem senha |
| Probabilidade | Baixa no laboratório, Alta se publicado na internet |
| Severidade | Média (laboratório) / Crítica (internet) |
| Correção | Consulta parametrizada |
| Status | Vulnerável → Mitigado |

A severidade vem de uma matriz definida em [`security-basics.md`](agent/knowledge/security-basics.md), então o agente não "chuta" a nota. Com o formato fixo, dá para comparar casos diferentes lado a lado, como uma falha de código e uma configuração insegura de SSH (Teste 4 do roteiro).

## 🚀 Como rodar

O agente é definido só por arquivos no padrão **AGENTS.md**, então funciona em qualquer harness compatível. Testei em dois:

- **Claude Code**: o harness usado para gerar as [evidências](#-evidências). O `CLAUDE.md` importa o `AGENTS.md`, então basta abrir o Claude Code na pasta do projeto.
- **Hermes**: o harness usado nas aulas. Instalei a v0.22.5 no Windows. Ele precisa de um provedor de modelo configurado (`hermes model`).

### 1. Instale um harness

- **Claude Code:** https://claude.com/claude-code
- **Hermes:** siga a documentação oficial: https://hermes-agent.nousresearch.com/docs

### 2. Baixe o projeto

```bash
git clone https://github.com/AhiPy/dio-agent-guardiai.git
cd dio-agent-guardiai
```

### 3. Abra o harness na pasta do projeto

```bash
claude      # Claude Code
hermes      # ou Hermes
```

> ⚠️ O terminal precisa estar **aberto na pasta do projeto**. Aberto em outro lugar, o harness não encontra o `AGENTS.md` nem as skills.

Para rodar um teste numa sessão limpa, sem modo interativo (foi assim que gerei as evidências):

```bash
claude -p "Tenho um servidor Ubuntu exposto na internet. Como deixo ele seguro?" --allowedTools "Read,Glob,Grep"
```

O `--allowedTools` deixa o agente só com ferramentas de leitura, então ele analisa os arquivos sem conseguir alterar nada.

### 4. Converse

```
Atue como especialista em AppSec. Analise o arquivo lab/app.py, que é um app
de login de laboratório meu. Encontre a falha, explique a exploração, cite a
técnica do MITRE ATT&CK e me oriente a reescrever o código.
```

Os demais prompts estão no [roteiro de testes](docs/roteiro-de-testes.md).

### 5. Valide a correção com o teste automático

Requer só Python 3, sem bibliotecas externas:

```bash
python lab/testar_injecao.py
```

```
=== app.py (vulnerável) ===
[OK  ] login legítimo           login=aceito
[OK  ] senha errada             login=negado
[FALHA] injeção na senha         login=aceito
[FALHA] injeção com comentário   login=aceito
--> VULNERÁVEL (2 caso(s) inesperado(s))

=== app_corrigido.py (consulta parametrizada) ===
[OK  ] login legítimo           login=aceito
[OK  ] senha errada             login=negado
[OK  ] injeção na senha         login=negado
[OK  ] injeção com comentário   login=negado
--> MITIGADO (0 caso(s) inesperado(s))
```

## 📸 Evidências

Cada teste rodou numa **sessão nova** do Claude Code (`claude -p`), aberta na pasta do projeto e só com ferramentas de leitura. As imagens são as respostas reais, sem edição, renderizadas a partir das transcrições em texto que também estão em [`docs/evidencias/`](docs/evidencias/).

### Análise do app vulnerável
O agente aponta a linha da f-string, cita CWE-89, OWASP e MITRE ATT&CK T1190, explica o `admin' --`, encontra duas falhas extras (senha em texto puro e senha no log) e termina com o relatório no formato fixo.

![Análise do app.py](docs/evidencias/01-analise-app-vulneravel.png)

### Revalidação após a correção
Mesmo formato de relatório, com o status mudando de Vulnerável para **Mitigado**. O próprio agente avisa que fez só análise estática e pede para rodar o teste automático.

![Revalidação](docs/evidencias/02-revalidacao-corrigido.png)

### Teste automatizado
A prova objetiva: as mesmas tentativas de injeção passam no `app.py` e são barradas no `app_corrigido.py`.

![Teste automatizado](docs/evidencias/03-teste-automatizado.png)

### Perguntas de contexto antes de agir
Diante do "servidor Ubuntu exposto", o agente **não** solta comandos. Ele apresenta o caminho por camadas e faz uma pergunta de contexto por vez.

![Perguntas de contexto](docs/evidencias/04-perguntas-de-contexto.png)

### Configuração insegura (sshd_config)
Outro tipo de falha, agora de configuração e não de código. O agente aponta os problemas e pergunta onde a máquina está antes de fechar a severidade.

![sshd_config](docs/evidencias/05-config-insegura.png)

### Limite ético
Diante de um pedido de ataque a um site de terceiros, o agente recusa e oferece laboratórios legais (DVWA, Juice Shop, WebGoat). A resposta tem um erro factual sobre o nome da lei, que mantive e corrigi numa nota: é evidência de que a saída de um agente precisa de revisão humana.

![Limite ético](docs/evidencias/07-limite-etico.png)

A lista de prints e o que cada um mostra está em [`docs/evidencias/`](docs/evidencias/README.md).

## ⚖️ Uso ético

Todos os testes deste repositório usam apenas o código da pasta `lab/` e máquinas de laboratório próprias. O `lab/app.py` é vulnerável **de propósito** e não deve ser usado em nenhum sistema real. A própria skill instrui o agente a só analisar ambientes do estudante ou autorizados, e a recusar pedidos de ataque a terceiros.

## 🗂️ Estrutura

```
dio-agent-guardiai/
├── README.md                         Este arquivo
├── AGENTS.md                         Definição do agente (alterado)
├── CLAUDE.md
├── agent/
│   ├── persona.md                    + Modo especialista em segurança
│   └── knowledge/
│       ├── dio-platform.md
│       ├── learning-experiences.md
│       └── security-basics.md        Novo: fundamentos e escala de risco
├── skills/
│   ├── README.md                     + skill no índice
│   ├── vulnerability-analysis/       Nova skill
│   │   ├── SKILL.md
│   │   └── README.md
│   └── ...                           Skills originais
├── lab/
│   ├── app.py                        Login vulnerável (laboratório)
│   ├── app_corrigido.py              Login corrigido
│   └── testar_injecao.py             Teste automático
└── docs/
    ├── README-original.md            Guia original do DIO Agent
    ├── roteiro-de-testes.md          Prompts de teste
    ├── evidencias/                   Prints
    ├── glossary.md
    └── youcom-mcp.md
```

## 🙌 Créditos

Baseado no [DIO Agent](https://github.com/digitalinnovationone/dio-agent), da DIO, e nas aulas da Expert Isadora. Desenvolvido por [Vinicius (AhiPy)](https://github.com/AhiPy).
