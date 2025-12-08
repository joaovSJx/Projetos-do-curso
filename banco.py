import sqlite3
import os

# SEMPRE usa o banco dentro da pasta Back
DB_PATH = os.path.join(os.path.dirname(__file__), "agend.db")


def conectar():
    return sqlite3.connect(DB_PATH)


def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()

    # tabela de serviços
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor REAL NOT NULL
        )
    """
    )

    # tabela de usuarios
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            numero TEXT NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL DEFAULT 'cliente'
        )
    """
    )

    # tabela de agendamentos
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS agend (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            servico_id INTEGER NOT NULL,
            )
         """)

    # cria adxmin padrão apenas se não existir
    cursor.execute("""
        INSERT OR IGNORE INTO cliente (nome, email, numero, senha, tipo)
        VALUES ('Admin', 'admin@gmail.com', '00000', '1234', 'admin')
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

# inicializa banco
inicializar_banco()