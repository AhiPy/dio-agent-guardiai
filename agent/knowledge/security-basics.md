# Fundamentos de Segurança

Base de conhecimento que o agente consulta ao conduzir análises de segurança (skill `vulnerability-analysis`). Define os termos e a escala de risco usados em todas as análises, para que elas fiquem consistentes.

## Conceitos essenciais

- **Ativo:** tudo o que tem valor e precisa de proteção. Dados de clientes, senhas, um servidor, a reputação da empresa.
- **Vulnerabilidade:** uma fraqueza que pode ser explorada. Exemplo: um login que monta o SQL juntando o texto digitado pelo usuário.
- **Ameaça:** quem ou o que pode explorar a fraqueza. Exemplo: um atacante na internet, um bot automatizado, um funcionário mal-intencionado.
- **Exploit:** a forma concreta de aproveitar a vulnerabilidade. Exemplo: digitar `' OR '1'='1` no campo de senha.
- **Risco:** a chance de uma ameaça explorar uma vulnerabilidade **e** o estrago que isso causaria. Em resumo: risco = probabilidade × impacto.
- **Controle (mitigação):** o que reduz o risco. Exemplo: consulta parametrizada, firewall, autenticação em dois fatores.

Analogia: a casa é o **ativo**, a janela destrancada é a **vulnerabilidade**, o ladrão é a **ameaça**, pular a janela é o **exploit**, e trancar a janela é o **controle**. O **risco** depende de a casa ficar numa rua movimentada (probabilidade) e do que tem dentro dela (impacto).

## A tríade CIA

Toda falha de segurança afeta pelo menos um destes três pilares. Use-os para descrever o impacto.

| Pilar | Pergunta-chave | Exemplo de violação |
|-------|----------------|---------------------|
| **Confidencialidade** | Só quem pode, vê? | Vazamento da tabela de usuários |
| **Integridade** | Os dados são confiáveis e só mudam por quem pode? | Atacante altera o saldo de uma conta |
| **Disponibilidade** | O sistema funciona quando precisam dele? | Servidor derrubado por um ataque de negação de serviço |

## Escala de risco

Use sempre esta escala. Ela é simples de propósito: serve para comparar casos e ensinar o raciocínio. Para relatórios formais, o padrão de mercado é o CVSS (https://www.first.org/cvss/), e vale mencioná-lo ao estudante.

### Impacto

| Nível | Quando usar |
|-------|-------------|
| Baixo | Expõe informação pouco sensível ou afeta só o próprio usuário |
| Médio | Afeta dados ou funções de outros usuários de forma limitada |
| Alto | Acesso indevido a contas, dados pessoais ou funções administrativas |
| Crítico | Controle total do sistema, do banco de dados ou do servidor |

### Probabilidade

| Nível | Quando usar |
|-------|-------------|
| Baixa | Exige acesso interno, condições raras ou conhecimento muito específico |
| Média | Exige alguma autenticação ou interação, mas é viável |
| Alta | Exposto na internet, sem autenticação, com técnica conhecida e ferramentas públicas |

### Matriz de severidade

| Impacto \ Probabilidade | Baixa | Média | Alta |
|-------------------------|-------|-------|------|
| **Baixo** | Baixa | Baixa | Média |
| **Médio** | Baixa | Média | Alta |
| **Alto** | Média | Alta | Crítica |
| **Crítico** | Alta | Crítica | Crítica |

A mesma falha muda de severidade conforme o contexto. Um SQL Injection num app que só roda em `localhost` de laboratório tem probabilidade baixa. O mesmo código publicado na internet tem probabilidade alta.

## Referências que o agente cita

- **CWE** (https://cwe.mitre.org/): catálogo de tipos de fraqueza. Ex.: CWE-89 (SQL Injection).
- **OWASP Top 10** (https://owasp.org/Top10/): as categorias de risco mais comuns em aplicações web. Ex.: Injection.
- **MITRE ATT&CK** (https://attack.mitre.org/): técnicas usadas por atacantes reais. Ex.: T1190, Exploit Public-Facing Application, para falhas exploradas em aplicações expostas na internet.

Só cite IDs que você tem certeza que existem. Se não tiver, diga a categoria em palavras e oriente o estudante a conferir no site.

## Boas práticas de defesa

### Código
- **Nunca confie na entrada do usuário.** Valide formato e tamanho, e trate todo dado externo como potencialmente malicioso.
- **Separe código de dados.** Use consultas parametrizadas (prepared statements) ou um ORM, nunca concatenação de strings em SQL ou comandos de sistema.
- **Guarde senhas com hash forte e salt** (bcrypt, scrypt, Argon2). Nunca em texto puro ou com MD5/SHA-1.
- **Mensagens de erro genéricas** para o usuário; detalhes só no log.
- **Segredos fora do código** (variáveis de ambiente, cofre de segredos), nunca commitados no Git.

### Infraestrutura
- **Menor privilégio:** cada usuário, serviço e conta de banco só com as permissões que precisa.
- **Reduza a superfície de ataque:** desligue serviços e portas que não usa; firewall negando tudo por padrão.
- **SSH endurecido:** autenticação por chave, sem login de root, limite de tentativas (ex.: fail2ban).
- **Atualizações em dia** do sistema e das dependências.
- **Logs e monitoramento:** sem registro, não dá para detectar nem investigar um incidente.

### Processo
- **Defesa em profundidade:** várias camadas, para que a falha de uma não derrube tudo.
- **Segurança desde o início (shift left / DevSecOps):** revisar cada alteração antes de chegar à produção.
- **Teste só o que é seu ou o que você tem autorização por escrito para testar.** Testar sistemas de terceiros sem permissão é crime no Brasil (Lei 12.737/2012).

## Onde praticar com segurança (gratuito)

- PortSwigger Web Security Academy: https://portswigger.net/web-security
- DVWA (Damn Vulnerable Web Application): https://github.com/digininja/DVWA
- OWASP Juice Shop: https://owasp.org/www-project-juice-shop/
- TryHackMe (salas gratuitas): https://tryhackme.com
