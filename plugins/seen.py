import os
import sqlite3
from datetime import datetime

DB_PATH = "db/seen.db"

def init_db():
    # Inicializa a base de dados, criando a tabela 'seen' se não existir.
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS seen (nick TEXT PRIMARY KEY, last_seen TEXT)")
        conn.commit()

def log_seen(nick):
    # Regista a última vez que o utilizador foi visto.
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT OR REPLACE INTO seen (nick, last_seen) VALUES (?, ?)", (nick, now))
        conn.commit()
    finally:
        conn.close()

def get_seen(nick):
    # Obtém a última vez que o utilizador foi visto.
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()
        c.execute("SELECT last_seen FROM seen WHERE nick=?", (nick,))
        row = c.fetchone()
        if row:
            return f"{nick} foi visto pela última vez em {row[0]}"
        return f"{nick} nunca foi visto."
    finally:
        conn.close()
