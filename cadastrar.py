from banco import conectar

# cadastrar
def cadastrar_conta(email, senha, nome, numero):
    """
    Cadastra um novo cliente no sistema.
    A ordem de parâmetros está compatível com o main.py.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cliente (email, senha, nome, numero, tipo)
        VALUES (?, ?, ?, ?, 'cliente')
    """, (email, senha, nome, numero))

    conn.commit()
    cursor.close()
    conn.close()



# atualizar

def atualizar_cliente(cliente_id, email, senha, nome, numero):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cliente
        SET email = ?, senha = ?, nome = ?, numero = ?
        WHERE id = ?
    """, (email, senha, nome, numero, cliente_id))

    conn.commit()
    cursor.close()
    conn.close()



# deletar

def deletar_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cliente WHERE id = ?", (cliente_id,))

    conn.commit()
    cursor.close()
    conn.close()



# buscar
def buscar_cliente(termo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, email, numero
        FROM cliente
        WHERE nome LIKE ? OR email LIKE ?
    """, (f"%{termo}%", f"%{termo}%"))

    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultados



# login
def verificar_login(email, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, tipo
        FROM cliente
        WHERE email = ? AND senha = ?
    """, (email, senha))

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return resultado
