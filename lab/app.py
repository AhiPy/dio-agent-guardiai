"""
app.py  —  LOGIN VULNERÁVEL (APENAS PARA LABORATÓRIO)

Este arquivo existe para testar a skill vulnerability-analysis.
Ele monta a consulta SQL juntando o texto digitado pela pessoa,
o que permite SQL Injection. NÃO use este padrão em código real.

Rode localmente:  python lab/app.py
"""

import sqlite3

DB = ":memory:"


def criar_banco():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE usuarios (id INTEGER PRIMARY KEY, usuario TEXT, senha TEXT)")
    # Senhas em texto puro: segunda falha, proposital, para o agente encontrar.
    cur.executemany(
        "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
        [("admin", "S3nh@Forte!"), ("vini", "minhasenha123")],
    )
    conn.commit()
    return conn


def login(conn, usuario, senha):
    # FALHA: a entrada do usuário vira parte do comando SQL.
    query = f"SELECT * FROM usuarios WHERE usuario = '{usuario}' AND senha = '{senha}'"
    print(f"[debug] SQL executado: {query}")
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchone() is not None


if __name__ == "__main__":
    conn = criar_banco()
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    if login(conn, usuario, senha):
        print("Login realizado com sucesso!")
    else:
        print("Usuário ou senha inválidos.")
