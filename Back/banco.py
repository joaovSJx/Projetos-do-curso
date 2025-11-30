import sqlite3

def conectar():
    return sqlite3.connect('agend.db')
conn = conectar()
cursor = conn.cursor()

# tabela de servicos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        valor REAL NOT NULL
)
""")


# tabela de clientes
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        numero TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL                 
)
""")

#tabela de agendamentos

cursor.execute("""
    CREATE TABLE IF NOT EXISTS agend (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        servico_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        hora TEXT NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES cliente(id),
        FOREIGN KEY (servico_id) REFERENCES servicos(id)
)
""")
conn.commit()
cursor.close()
conn.close()
