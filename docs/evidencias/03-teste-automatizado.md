# Teste automatizado: prova da mitigação

> Saída real de `python -X utf8 lab/testar_injecao.py` · Python 3.12.10 · 2026-10-27 09:20

```text
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
