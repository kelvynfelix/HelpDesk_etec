# database/db.py
import sqlite3, os
from datetime import datetime
import uuid
import shutil

DB_PATH = os.path.join(os.path.dirname(__file__), "helpdesk.db")
UPLOADS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOADS, exist_ok=True)


def get_conn():
    return sqlite3.connect(DB_PATH)


def create_ticket(nome, sala, descricao, caminho_anexo=None):
    conn = get_conn()
    c = conn.cursor()
    nome_arquivo = None
    if caminho_anexo:
        ext = os.path.splitext(caminho_anexo)[1]
        nome_arquivo = f"{uuid.uuid4().hex}{ext}"
        destino = os.path.join(UPLOADS, nome_arquivo)
        shutil.copy2(caminho_anexo, destino)
    data_hora = datetime.now().isoformat(timespec="seconds")
    c.execute(
        "INSERT INTO chamados (nome_usuario, sala, descricao, anexo, data_hora) VALUES (?,?,?,?,?)",
        (nome, sala, descricao, nome_arquivo, data_hora),
    )
    conn.commit()
    conn.close()


def list_tickets():
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT id, nome_usuario, sala, descricao, anexo, status, data_hora FROM chamados ORDER BY id DESC"
    )
    rows = c.fetchall()
    conn.close()
    return rows


def update_status(ticket_id, novo_status):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE chamados SET status=? WHERE id=?", (novo_status, ticket_id))
    conn.commit()
    conn.close()


def verify_admin(usuario, senha_plain):
    import hashlib

    salt = b"escola_salt_2025"
    senha_hash = hashlib.pbkdf2_hmac("sha256", senha_plain.encode(), salt, 100000).hex()
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id FROM admin WHERE usuario=? AND senha=?", (usuario, senha_hash))
    r = c.fetchone()
    conn.close()
    return bool(r)
