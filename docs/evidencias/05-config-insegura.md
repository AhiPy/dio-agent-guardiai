# Teste 4: Configuração insegura (sshd_config)

> Harness: Claude Code 2.1.311 (Claude Code) · sessão nova, modo não interativo (`claude -p`), aberta na pasta do projeto · 2026-10-27 09:18

## Prompt

```text
Esse trecho do sshd_config do meu Ubuntu de laboratório está seguro?

PermitRootLogin yes
PasswordAuthentication yes
Port 22
```

## Resposta do agente

Boa pergunta. Revisar o `sshd_config` é um dos primeiros passos para proteger um servidor.

Resposta curta: **não, essa configuração não é segura.** Mas o tamanho do risco depende de onde essa máquina está. Antes de calcular a severidade e passar as correções, deixa eu adiantar o que já dá para ver:

1. **`PermitRootLogin yes`**: permite entrar direto como `root`, o usuário com poder total no sistema. Todo Linux tem esse usuário, então o atacante já sabe o login e só precisa descobrir a senha. Se conseguir, controla a máquina inteira.
2. **`PasswordAuthentication yes`**: libera login por senha. Isso abre espaço para **força bruta**, que são bots testando milhares de senhas até acertar. Junto com o item 1, é a combinação que esses bots mais procuram.
3. **`Port 22`**: essa linha sozinha **não é uma vulnerabilidade**. Trocar a porta só diminui o "barulho" de robôs nos logs. É uma camada leve, não uma proteção de verdade. Vou explicar isso melhor na hora das correções.

Os itens 1 e 2 juntos são o problema principal. Pense numa porta de casa com o nome do morador escrito nela e uma fechadura que aceita palpites sem limite.

Para eu classificar o risco do jeito certo, preciso de uma informação:

**Como essa VM está exposta?** Ela é acessível só do seu computador (rede host-only/NAT, sem redirecionamento de porta), da sua rede local, ou pela internet (VPS na nuvem, ou porta 22 aberta no roteador)?

A falha é a mesma nos três casos, mas a severidade muda bastante. Num servidor exposto na internet, ela seria crítica.

