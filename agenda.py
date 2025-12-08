from banco import conectar

# Criar agendamento
def confirmar_agendamento(cliente_id, servico_id, data, hora):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO agend (cliente_id, servico_id, data, hora)
        VALUES (?, ?, ?, ?)
    """, (cliente_id, servico_id, data, hora))
    conn.commit()
    cursor.close()
    conn.close()


# Listar todos os agendamentos
def listar_agendamentos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            a.id AS agend_id,
            c.id AS cliente_id,
            c.nome AS cliente_nome,
            s.id AS servico_id,
            s.nome AS servico_nome,
            a.data,
            a.hora
        FROM agend a
        JOIN cliente c ON a.cliente_id = c.id
        JOIN servicos s ON a.servico_id = s.id
        ORDER BY a.data, a.hora
    """)
    agendamentos = cursor.fetchall()
    cursor.close()
    conn.close()
    return agendamentos


# Atualizar agendamento
def atualizar_agendamento(agend_id, data, hora):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE agend
        SET data = ?, hora = ?
        WHERE id = ?
    """, (data, hora, agend_id))
    conn.commit()
    cursor.close()
    conn.close()


# Cancelar agendamento
def cancelar_agendamento(agend_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agend WHERE id = ?", (agend_id,))
    conn.commit()
    cursor.close()
    conn.close()


# Verificar se horário está disponível
def horario_disponivel(servico_id, data, hora):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1 FROM agend
        WHERE servico_id = ? AND data = ? AND hora = ?
    """, (servico_id, data, hora))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado is None


# Horários disponíveis
horarios = [
    "08:00", "09:00", "10:00", "11:00",
    "13:00", "14:00", "15:00", "16:00"
]


def listar_horarios_disponiveis(servico_id, data):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT hora FROM agend WHERE servico_id = ? AND data = ?", (servico_id, data))
    horarios_ocupados = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return [h for h in horarios if h not in horarios_ocupados]


def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, numero FROM cliente")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados
