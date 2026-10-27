"""
app_corrigido.py  —  LOGIN CORRIGIDO

Mesma funcionalidade do app.py, com as falhas mitigadas:
1. Consulta parametrizada: a entrada do usuário nunca vira código SQL.
2. Senhas guardadas com hash + salt (PBKDF2-HMAC-SHA256, biblioteca padrão).
3. Comparação em tempo constante e mensagem de erro genérica.

Rode localmente:  python lab/app_corrigido.py
"""

import hashlib
import hmac
import os
import sqlite3

DB = ":memory:"
ITERACOES = 600_000  # recomendação atual da OWASP para PBKDF2-HMAC-SHA256


def gerar_hash(senha, salt=None):
    salt = salt or os.urandom(16)
    hash_senha = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, ITERACOES)
    return salt, hash_senha


def criar_banco():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE usuarios (id INTEGER PRIMARY KEY, usuario TEXT UNIQUE, salt BLOB, hash BLOB)"
    )
    for usuario, senha in [("admin", "S3nh@Forte!"), ("vini", "minhasenha123")]:
        salt, hash_senha = gerar_hash(senha)
        cur.execute(
            "INSERT INTO usuarios (usuario, salt, hash) VALUES (?, ?, ?)",
            (usuario, salt, hash_senha),
        )
    conn.commit()
    return conn


def login(conn, usuario, senha):
    # CORREÇÃO: os "?" são marcadores. O banco recebe os valores separados
    # do comando, então ' OR '1'='1 é tratado como texto, não como SQL.
    cur = conn.cursor()
    cur.execute("SELECT salt, hash FROM usuarios WHERE usuario = ?", (usuario,))
    linha = cur.fetchone()
    if linha is None:
        return False
    salt, hash_salvo = linha
    _, hash_tentativa = gerar_hash(senha, salt)
    return hmac.compare_digest(hash_salvo, hash_tentativa)


if __name__ == "__main__":
    conn = criar_banco()
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    if login(conn, usuario, senha):
        print("Login realizado com sucesso!")
    else:
        print("Usuário ou senha inválidos.")
