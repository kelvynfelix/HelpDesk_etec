# database/init_db.py
import sqlite3
import hashlib
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "helpdesk.db")


def hash_password(password: str) -> str:
    # pbkdf2_hmac simples — suficiente para projeto escolar
    salt = b"escola_salt_2025"
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return dk.hex()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        senha TEXT
    );
    """
    )
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS chamados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_usuario TEXT,
        sala TEXT,
        descricao TEXT,
        anexo TEXT,
        status TEXT DEFAULT 'Aberto',
        data_hora TEXT
    );
    """
    )
    # cria um admin inicial (usuario: admin, senha: admin123) — peça para trocar depois
    try:
        c.execute(
            "INSERT INTO admin (usuario, senha) VALUES (?, ?)",
            ("admin", hash_password("admin123")),
        )
    except sqlite3.IntegrityError:
        pass
    conn.commit()
    conn.close()
    print("Banco inicial criado em:", DB_PATH)


if __name__ == "__main__":
    init_db()
