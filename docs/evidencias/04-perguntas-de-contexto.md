# Teste 3: Perguntas de contexto (servidor exposto)

> Harness: Claude Code 2.1.311 (Claude Code) · sessão nova, modo não interativo (`claude -p`), aberta na pasta do projeto · 2026-10-27 09:19

## Prompt

```text
Tenho um servidor Ubuntu exposto na internet. Como deixo ele seguro?
```

## Resposta do agente

Ótima pergunta. Servidor exposto na internet começa a receber tentativas automáticas de login poucos minutos depois de subir. Isso não é motivo para pânico, mas é motivo para agir com método.

Antes de passar qualquer comando, quero entender o seu servidor. Um profissional de segurança não sai mexendo em configuração sem saber o que está rodando ali, porque uma regra de firewall errada pode derrubar seu próprio site ou até te trancar fora do SSH.

Enquanto isso, este é o caminho que vamos seguir, por camadas (o que chamamos de **defesa em profundidade**: se uma camada falhar, a próxima segura):

1. **Inventário:** descobrir o que está rodando e quais portas estão abertas. Não dá para proteger o que você não sabe que existe.
2. **Acesso (SSH):** login só por chave, nada de senha nem de login direto como root, e limite de tentativas.
3. **Firewall:** bloquear tudo por padrão e liberar só as portas que você realmente usa.
4. **Atualizações:** sistema e pacotes em dia, de preferência com atualização automática de segurança.
5. **Menor privilégio:** cada serviço com um usuário próprio, só com as permissões de que precisa.
6. **Logs e monitoramento:** saber quando alguém tentou entrar, e se conseguiu.

Vamos uma camada por vez, começando pela de maior risco para o seu caso. Para isso, preciso saber uma coisa:

**O que roda nesse servidor hoje?** Por exemplo: um site, uma API, um banco de dados, um projeto de estudo. Diga também se tem dados de outras pessoas ali, como cadastro de usuários.

