from banco import conectar
def cadastrar_conta(email, senha, nome, numero):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cliente (email, senha, nome, numero) VALUES (?, ?, ?, ?)", (email, senha, nome, numero))
    conn.commit()
    cursor.close()
    conn.close()


def verificar_login(email, senha, nome, numero):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cliente WHERE email = ? AND senha = ? AND nome = ? AND numero = ?",  (email, senha, nome, numero))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado is not None