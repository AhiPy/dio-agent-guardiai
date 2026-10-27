"""
testar_injecao.py  —  prova automática de que a correção funcionou.

Roda as mesmas tentativas contra o app vulnerável e o corrigido.
Uso (na raiz do projeto):  python lab/testar_injecao.py
"""

import contextlib
import io

import app
import app_corrigido

CASOS = [
    ("login legítimo", "admin", "S3nh@Forte!", True),
    ("senha errada", "admin", "errada", False),
    ("injeção na senha", "admin", "' OR '1'='1", False),
    ("injeção com comentário", "admin' --", "qualquer", False),
]


def rodar(modulo, nome):
    conn = modulo.criar_banco()
    print(f"\n=== {nome} ===")
    falhas = 0
    for descricao, usuario, senha, esperado in CASOS:
        with contextlib.redirect_stdout(io.StringIO()):
            resultado = modulo.login(conn, usuario, senha)
        ok = resultado == esperado
        falhas += not ok
        marca = "OK  " if ok else "FALHA"
        print(f"[{marca}] {descricao:<24} login={'aceito' if resultado else 'negado'}")
    print(f"--> {'VULNERÁVEL' if falhas else 'MITIGADO'} ({falhas} caso(s) inesperado(s))")


if __name__ == "__main__":
    rodar(app, "app.py (vulnerável)")
    rodar(app_corrigido, "app_corrigido.py (consulta parametrizada)")
