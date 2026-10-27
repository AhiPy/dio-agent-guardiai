# Evidências

Resultados dos testes do [roteiro de testes](../roteiro-de-testes.md). Cada teste do agente rodou numa sessão nova do Claude Code (`claude -p`), aberta na pasta do projeto e só com ferramentas de leitura (`Read`, `Glob`, `Grep`).

Para cada teste há dois arquivos:

- o `.md`, com o prompt e a resposta original do agente, sem edição;
- o `.png`, com essa mesma transcrição renderizada como imagem.

| Arquivo | Teste do roteiro | O que mostra |
|---------|------------------|--------------|
| `01-analise-app-vulneravel` | 1 | O agente analisando `lab/app.py` e o relatório final |
| `02-revalidacao-corrigido` | 2 | A nova varredura em `lab/app_corrigido.py` com status Mitigado |
| `03-teste-automatizado` | 2 (script) | Saída de `python lab/testar_injecao.py` |
| `04-perguntas-de-contexto` | 3 | O agente perguntando o contexto antes de sugerir comandos para o Ubuntu exposto |
| `05-config-insegura` | 4 | Análise do `sshd_config` de laboratório |
| `07-limite-etico` | 6 | Recusa de um pedido de ataque a terceiros, com caminho de laboratório no lugar (inclui uma nota de revisão humana) |

O Teste 5 do roteiro (comparação com um chat genérico) é opcional e ainda não foi feito. Quando for, o print entra aqui como `06-chat-generico.png`.
