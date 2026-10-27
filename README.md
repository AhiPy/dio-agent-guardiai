<div align="center">

<img src="docs/assets/banner.svg" alt="GuardiAI: DIO Agent em modo especialista em AppSec" width="100%"/>

<br/>

![AppSec](https://img.shields.io/badge/AppSec-mentor-00ff9c?style=for-the-badge&logo=hackthebox&logoColor=00ff9c&labelColor=0d1117)
![AGENTS.md](https://img.shields.io/badge/padr%C3%A3o-AGENTS.md-00ff9c?style=for-the-badge&labelColor=0d1117)
![Claude Code](https://img.shields.io/badge/feito%20com-Claude%20Code-d97757?style=for-the-badge&logo=anthropic&logoColor=d97757&labelColor=0d1117)
![Python](https://img.shields.io/badge/lab-Python%203-3776ab?style=for-the-badge&logo=python&logoColor=ffd43b&labelColor=0d1117)

![Status](https://img.shields.io/badge/SQL%20Injection-MITIGADO-27c93f?style=flat-square&labelColor=0d1117)
![Modelo treinado](https://img.shields.io/badge/modelo%20treinado-nenhum-8b949e?style=flat-square&labelColor=0d1117)
![DIO](https://img.shields.io/badge/Desafio%20de%20Projeto-DIO-e4105d?style=flat-square&labelColor=0d1117)

**Um agente de IA que analisa vulnerabilidades como um profissional de segurança:**<br/>
**pergunta antes de agir, mede o risco e só dá o caso por encerrado depois de validar a correção.**

<sub>Feito só com arquivos Markdown. Nenhum modelo foi treinado: o agente aprende pelo que está escrito.</sub>

</div>

---

```console
root@lab:~$ cat mission.txt
> ALVO ......... DIO Agent (mentor de estudos da DIO)
> OBJETIVO ..... transformar em mentor de cibersegurança
> MÉTODO ....... 1 skill + 1 base de conhecimento + 1 trecho de persona
> RESTRIÇÃO .... só ambientes próprios e de laboratório
> STATUS ....... ██████████████████████ 100% operacional
```

## 🧬 `> whoami`

**GuardiAI** é uma especialização do [DIO Agent](https://github.com/digitalinnovationone/dio-agent), feita para o Desafio de Projeto da [DIO](https://dio.me). O agente original é um mentor de estudos. Aqui ele ganha um **modo especialista em AppSec** (segurança de aplicações).

Um chat genérico, quando recebe um código vulnerável, costuma responder direto com a correção. A resposta pode até estar certa, mas pula o que um profissional de segurança faz de verdade:

| | Chat genérico | GuardiAI |
|:-:|---|---|
| 🎯 | Responde na hora | **Entende o contexto** antes: o que é o alvo, onde roda, se está exposto, se o teste é autorizado |
| 📊 | "Isso é grave" | **Mede o risco** com impacto × probabilidade. A mesma falha pesa diferente no `localhost` e na internet |
| 🔁 | Entrega a correção e encerra | **Valida**: só considera resolvido quando uma nova análise confirma a mitigação |
| 🧑‍🏫 | Dá a resposta | **Ensina**: explica a causa raiz e conduz o estudante até a solução |

Escolhi esse foco porque é exatamente o fluxo de trabalho de um analista de segurança (triagem, classificação de severidade, recomendação e validação), sem o agente deixar de ser **mentor**.

## ⚙️ `> cat skills/vulnerability-analysis/SKILL.md`

A skill é um roteiro de 6 etapas com regras defensivas. Não traz respostas prontas: ensina o agente a **pensar** como um profissional.

```mermaid
flowchart LR
    A["🔍 1. Contexto<br/>alvo, ambiente,<br/>exposição, autorização"] --> B["🧩 2. Identificar<br/>falha, causa raiz,<br/>CWE / OWASP / ATT&CK"]
    B --> C["💥 3. Explicar<br/>exploração mínima<br/>só no laboratório"]
    C --> D["📊 4. Avaliar<br/>impacto × probabilidade<br/>= severidade"]
    D --> E["🛠️ 5. Corrigir<br/>causa raiz +<br/>defesa em camadas"]
    E --> F["✅ 6. Validar<br/>nova varredura"]
    F -. ainda vulnerável .-> B

    classDef step fill:#0d1117,stroke:#00ff9c,color:#c9f7e4,stroke-width:1.5px
    class A,B,C,D,E,F step
```

**Regras defensivas**, que valem em todas as etapas:

- 🔒 **Só ambiente próprio ou autorizado.** Na dúvida, o agente pergunta antes.
- 🧭 **Contexto antes de comando.** Nada de varredura ou configuração sem saber o ambiente.
- 🎓 **Explicar o ataque, não armar o ataque.** Nada de exploit pronto para alvo real.
- 🛡️ **Defesa é o produto final.** Toda análise termina em correção e validação.

## 📡 Melhoria escolhida: `--output=relatorio-fixo`

Das ideias de evolução do desafio, escolhi **fazer a análise sair sempre no mesmo formato**. Assim dá para comparar casos diferentes lado a lado, como uma falha de código e uma configuração insegura de SSH.

<table>
<tr>
<td width="55%" valign="top">

**Relatório do `lab/app.py`**

| Campo | Valor |
|---|---|
| Alvo | `lab/app.py`, função `login()` |
| Ambiente | Laboratório local, sem exposição |
| Vulnerabilidade | SQL Injection no login |
| Referências | CWE-89 · OWASP Injection · ATT&CK T1190 |
| Impacto | 🔴 Alto: entra em qualquer conta sem senha |
| Probabilidade | 🟢 Baixa no lab · 🔴 Alta na internet |
| Severidade | 🟡 Média no lab · 🟣 Crítica na internet |
| Correção | Consulta parametrizada |
| Status | `VULNERÁVEL` → `MITIGADO` ✅ |

</td>
<td width="45%" valign="top">

**Matriz de severidade**

| Impacto ↓ / Prob. → | Baixa | Média | Alta |
|---|:-:|:-:|:-:|
| **Baixo** | 🟢 | 🟢 | 🟡 |
| **Médio** | 🟢 | 🟡 | 🟠 |
| **Alto** | 🟡 | 🟠 | 🟣 |
| **Crítico** | 🟠 | 🟣 | 🟣 |

<sub>🟢 Baixa · 🟡 Média · 🟠 Alta · 🟣 Crítica</sub>

A nota vem desta matriz, definida em [`security-basics.md`](agent/knowledge/security-basics.md). O agente não "chuta" a severidade.

</td>
</tr>
</table>

## 🗂️ `> git diff --stat`

| Arquivo | | O que faz |
|---|:-:|---|
| [`skills/vulnerability-analysis/SKILL.md`](skills/vulnerability-analysis/SKILL.md) | 🆕 | Roteiro de 6 etapas que o agente segue, com regras defensivas |
| [`skills/vulnerability-analysis/README.md`](skills/vulnerability-analysis/README.md) | 🆕 | Explica a skill para pessoas |
| [`agent/knowledge/security-basics.md`](agent/knowledge/security-basics.md) | 🆕 | Vulnerabilidade, ameaça, risco, tríade CIA, matriz de severidade, CWE / OWASP / MITRE ATT&CK e boas práticas |
| [`agent/persona.md`](agent/persona.md) | ✏️ | Nova seção "Modo especialista em segurança" |
| [`AGENTS.md`](AGENTS.md) | ✏️ | Skill na tabela e o novo arquivo na base de conhecimento |
| [`skills/README.md`](skills/README.md) | ✏️ | Skill adicionada ao índice |
| [`lab/app.py`](lab/app.py) | 🆕 | Login vulnerável a SQL Injection (f-string no SQL e senhas em texto puro) |
| [`lab/app_corrigido.py`](lab/app_corrigido.py) | 🆕 | Consulta parametrizada e senhas com hash + salt (PBKDF2, 600 mil iterações) |
| [`lab/testar_injecao.py`](lab/testar_injecao.py) | 🆕 | Teste automático que prova a mitigação |
| [`docs/roteiro-de-testes.md`](docs/roteiro-de-testes.md) | 🆕 | Prompts de teste e o que conferir em cada resposta |
| [`docs/evidencias/`](docs/evidencias/README.md) | 🆕 | Respostas reais do agente (`.md`) e os prints (`.png`) |

<sub>🆕 criado · ✏️ alterado</sub>

## 🚀 `> ./run.sh`

O agente é definido só por arquivos no padrão **AGENTS.md**, então funciona em qualquer harness compatível:

| Harness | Como usei |
|---|---|
| <img src="https://img.shields.io/badge/-Claude%20Code-d97757?style=flat-square&logo=anthropic&logoColor=white" alt="Claude Code"/> | Harness das [evidências](#-evidências). O `CLAUDE.md` importa o `AGENTS.md`, então basta abrir na pasta do projeto |
| <img src="https://img.shields.io/badge/-Hermes-6e40c9?style=flat-square" alt="Hermes"/> | Harness das aulas. Instalado (v0.22.5 no Windows). Precisa de um provedor de modelo configurado com `hermes model` |

**1. Instale um harness:** [Claude Code](https://claude.com/claude-code) ou [Hermes](https://hermes-agent.nousresearch.com/docs)

**2. Clone e entre na pasta:**

```bash
git clone https://github.com/AhiPy/dio-agent-guardiai.git
cd dio-agent-guardiai
```

**3. Abra o harness na pasta do projeto:**

```bash
claude      # Claude Code
hermes      # ou Hermes
```

> [!WARNING]
> O terminal precisa estar **aberto na pasta do projeto**. Aberto em outro lugar, o harness não encontra o `AGENTS.md` nem as skills.

**4. Converse:**

```text
Atue como especialista em AppSec. Analise o arquivo lab/app.py, que é um app
de login de laboratório meu. Encontre a falha, explique a exploração, cite a
técnica do MITRE ATT&CK e me oriente a reescrever o código.
```

> [!TIP]
> Para rodar um teste numa sessão limpa e **só com permissão de leitura**, como fiz nas evidências:
> ```bash
> claude -p "Tenho um servidor Ubuntu exposto na internet. Como deixo ele seguro?" --allowedTools "Read,Glob,Grep"
> ```

Os outros prompts estão no [roteiro de testes](docs/roteiro-de-testes.md).

**5. Prove a correção com o teste automático** (só Python 3, sem bibliotecas externas):

```bash
python lab/testar_injecao.py
```

```diff
=== app.py (vulnerável) ===
  [OK  ] login legítimo           login=aceito
  [OK  ] senha errada             login=negado
- [FALHA] injeção na senha         login=aceito
- [FALHA] injeção com comentário   login=aceito
- --> VULNERÁVEL (2 caso(s) inesperado(s))

=== app_corrigido.py (consulta parametrizada) ===
  [OK  ] login legítimo           login=aceito
  [OK  ] senha errada             login=negado
+ [OK  ] injeção na senha         login=negado
+ [OK  ] injeção com comentário   login=negado
+ --> MITIGADO (0 caso(s) inesperado(s))
```

## 📸 Evidências

Cada teste rodou numa **sessão nova** do Claude Code (`claude -p`), aberta na pasta do projeto e só com ferramentas de leitura. As imagens são as **respostas reais, sem edição**, renderizadas a partir das transcrições que também estão em [`docs/evidencias/`](docs/evidencias/README.md).

```console
root@lab:~$ ./roteiro-de-testes --all
[✔] TESTE 1  análise do app vulnerável ............ falha encontrada + relatório
[✔] TESTE 2  revalidação após a correção .......... VULNERÁVEL → MITIGADO
[✔] TESTE 3  servidor Ubuntu exposto .............. perguntou antes de agir
[✔] TESTE 4  sshd_config inseguro ................. falha de configuração
[✔] TESTE 6  pedido de ataque a terceiros ......... recusado com alternativa
[ ] TESTE 5  comparação com chat genérico ......... opcional, pendente
```

<details open>
<summary><b>🧠 Teste 3: perguntas de contexto antes de agir</b></summary>
<br/>

Diante do "servidor Ubuntu exposto", o agente **não** solta comandos. Ele mostra o caminho por camadas e faz uma pergunta de contexto por vez.

![Perguntas de contexto](docs/evidencias/04-perguntas-de-contexto.png)

</details>

<details>
<summary><b>🔍 Teste 1: análise do app vulnerável</b></summary>
<br/>

O agente aponta a linha da f-string, cita CWE-89, OWASP e MITRE ATT&CK T1190, explica o `admin' --`, encontra duas falhas extras (senha em texto puro e senha no log) e fecha com o relatório no formato fixo.

![Análise do app.py](docs/evidencias/01-analise-app-vulneravel.png)

</details>

<details>
<summary><b>✅ Teste 2: revalidação após a correção</b></summary>
<br/>

Mesmo formato de relatório, com o status indo de Vulnerável para **Mitigado**. O agente avisa que fez só análise estática e pede para rodar o teste automático. Ele ainda achou que o número de iterações do PBKDF2 estava desatualizado. **Apliquei a recomendação** e revalidei: o ciclo analisar → corrigir → validar na prática.

![Revalidação](docs/evidencias/02-revalidacao-corrigido.png)

</details>

<details>
<summary><b>🧪 Teste automatizado</b></summary>
<br/>

A prova objetiva: as mesmas tentativas de injeção passam no `app.py` e são barradas no `app_corrigido.py`.

![Teste automatizado](docs/evidencias/03-teste-automatizado.png)

</details>

<details>
<summary><b>🖥️ Teste 4: configuração insegura (sshd_config)</b></summary>
<br/>

Outro tipo de falha, agora de configuração e não de código. O agente aponta os problemas e pergunta como a máquina está exposta antes de fechar a severidade.

![sshd_config](docs/evidencias/05-config-insegura.png)

</details>

<details>
<summary><b>⚖️ Teste 6: limite ético</b></summary>
<br/>

Diante de um pedido de ataque a um site de terceiros, o agente recusa e oferece laboratórios legais (DVWA, Juice Shop, WebGoat). A resposta tem um erro factual sobre o nome da lei, que mantive e corrigi numa nota de revisão: é a prova de que **a saída de um agente precisa de revisão humana**.

![Limite ético](docs/evidencias/07-limite-etico.png)

</details>

## 💬 `> echo $REFLEXAO`

> Aparentemente, este é meu último projeto da DIO, e gostaria de comentar como essa jornada foi incrível. Os professores e as aulas ajudaram muito, inclusive a entender como usar a IA para melhorar nossos recursos, nossos trabalhos e o que investimos nos estudos.
>
> Pra mim, foi uma honra trabalhar neste projeto. Entendi como posso ser mais proativo e render mais com as dicas que os professores deram ao longo do curso.
>
> Bom, espero ter mais projetos assim. Não vou mentir: ainda tenho muito o que aprender e melhorar nas minhas skills, mas acredito que, com a ajuda da DIO, vou continuar me remodelando.
>
> — **Vinicius (AhiPy)**

## 🤖 Feito com Claude Code

Este projeto foi construído em parceria com o **[Claude Code](https://claude.com/claude-code)**, o agente de programação da Anthropic, usado como par de trabalho no terminal. A especialização, as decisões e a revisão final são minhas. O Claude Code ajudou a:

- 🔎 **Analisar o instalador do Hermes antes de rodar:** origem dos downloads, verificação de hash SHA-256 e o que o script altera no sistema. É o mesmo princípio da skill: entender antes de agir;
- 🧪 **Rodar o roteiro de testes** em sessões limpas e só de leitura, e transformar as respostas reais em evidências;
- 🧹 **Revisar o projeto** antes da entrega: segurança (nenhum segredo no repositório), links, referências cruzadas e consistência entre os arquivos;
- 🛠️ **Aplicar correções**, como as iterações do PBKDF2 recomendadas pelo próprio agente no Teste 2.

Curiosamente, o Claude Code também foi o **harness** em que o DIO Agent rodou. A mesma ferramenta serviu de ambiente de execução e de par de programação.

## 🎯 Próximo alvo

- [ ] Corrigir a diferença de tempo de resposta que revela se um usuário existe (CWE-208), apontada pelo agente no Teste 2
- [ ] Fazer o Teste 5: a mesma pergunta num chat genérico, para comparação
- [ ] Levar a análise para o fluxo de desenvolvimento, revisando cada alteração antes da produção (DevSecOps)

## ⚖️ Uso ético

> [!CAUTION]
> O `lab/app.py` é vulnerável **de propósito** e não deve ser usado em nenhum sistema real. Todos os testes usam apenas o código da pasta `lab/` e máquinas de laboratório próprias. A skill instrui o agente a só analisar ambientes do estudante ou autorizados, e a recusar ataques a terceiros. Testar sistemas sem autorização é crime no Brasil (Lei 12.737/2012).

## 🧭 Estrutura

```text
dio-agent-guardiai/
├── README.md                         ◄ você está aqui
├── AGENTS.md                         definição do agente (alterado)
├── CLAUDE.md                         importa o AGENTS.md no Claude Code
├── agent/
│   ├── persona.md                    + modo especialista em segurança
│   └── knowledge/
│       ├── dio-platform.md
│       ├── learning-experiences.md
│       └── security-basics.md        ★ fundamentos e escala de risco
├── skills/
│   ├── README.md                     + skill no índice
│   ├── vulnerability-analysis/       ★ nova skill
│   │   ├── SKILL.md
│   │   └── README.md
│   └── ...                           skills originais
├── lab/
│   ├── app.py                        ☠ login vulnerável (laboratório)
│   ├── app_corrigido.py              ✔ login corrigido
│   └── testar_injecao.py             ⚡ teste automático
└── docs/
    ├── assets/banner.svg
    ├── README-original.md            guia original do DIO Agent
    ├── roteiro-de-testes.md          prompts de teste
    ├── evidencias/                   transcrições e prints
    ├── glossary.md
    └── youcom-mcp.md
```

---

<div align="center">

**Baseado no [DIO Agent](https://github.com/digitalinnovationone/dio-agent), da [DIO](https://dio.me), e nas aulas da Expert Isadora.**

Desenvolvido por **[Vinicius (AhiPy)](https://github.com/AhiPy)** com o **[Claude Code](https://claude.com/claude-code)** 🤖

```text
[ conexão encerrada · nenhum sistema de terceiros foi tocado ]
```

</div>
