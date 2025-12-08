import sqlite3
from banco import conectar

def autenticar_usuario(email, senha):
    """
    Retorna:
      - tuple com dados do usuário se autenticado
      - None se falhar
    """

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, email, numero, tipo
        FROM usuario
        WHERE email = ? AND senha = ?
    """, (email, senha))

    resultado = cursor.fetchone()

    conn.close()

    return resultado




