from banco import conectar

def adicionar_servico(nome, valor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO servicos (nome, valor) VALUES (?, ?)", (nome, valor))
    conn.commit()
    cursor.close()
    conn.close()

def listar_servicos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, valor FROM servicos")
    servicos = cursor.fetchall()
    cursor.close()
    conn.close()
    return servicos 

def atualizar_servico(servico_id, nome, valor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE servicos SET nome = ?, valor = ? WHERE id = ?", (nome, valor, servico_id))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_servico(servico_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM servicos WHERE id = ?", (servico_id,))
    conn.commit()
    cursor.close()
    conn.close()