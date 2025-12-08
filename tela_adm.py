# tela_adm.py
import sys
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QApplication
)
from PySide6.QtCore import Qt

# garantir que Back esteja no sys.path
ROOT_BACK = os.path.join(os.path.dirname(__file__), '..', 'Back')
if ROOT_BACK not in sys.path:
    sys.path.insert(0, ROOT_BACK)

# importa backend (se faltar, as funções serão None e mensagens serão mostradas)
try:
    from cadastrar import (
        cadastrar_cliente, atualizar_cliente, deletar_cliente, buscar_cliente
    )
except Exception:
    cadastrar_cliente = atualizar_cliente = deletar_cliente = buscar_cliente = None

try:
    from serv import (
        adicionar_servico, listar_servicos, atualizar_servico, deletar_servico
    )
except Exception:
    adicionar_servico = listar_servicos = atualizar_servico = deletar_servico = None

try:
    from agenda import (
        listar_agendamentos, deletar_agendamento
    )
except Exception:
    listar_agendamentos = deletar_agendamento = None


class TelaAdm(QWidget):
    def __init__(self, usuario=None):
        """
        usuario: tuple (usuario_id, tipo). Exige tipo == 'admin' para acesso.
        Se chamado sem parâmetro, acesso é negado (forçar uso via Login).
        """
        super().__init__()

        if not usuario or len(usuario) < 2 or usuario[1] != 'admin':
            QMessageBox.critical(None, "Acesso negado", "Acesso negado. Faça login como administrador.")
            raise PermissionError("Admin access required")

        self.usuario = usuario

        self.setWindowTitle("Painel Administrativo")
        self.setGeometry(200, 200, 880, 560)

        layout = QVBoxLayout(self)

        # menu de navegação
        menu = QHBoxLayout()
        self.btn_clientes = QPushButton("Clientes")
        self.btn_servicos = QPushButton("Serviços")
        self.btn_agend = QPushButton("Agendamentos")

        self.btn_clientes.clicked.connect(self.tela_clientes)
        self.btn_servicos.clicked.connect(self.tela_servicos)
        self.btn_agend.clicked.connect(self.tela_agendamentos)

        menu.addWidget(self.btn_clientes)
        menu.addWidget(self.btn_servicos)
        menu.addWidget(self.btn_agend)
        layout.addLayout(menu)

        # container das "telas"
        self.container = QVBoxLayout()
        layout.addLayout(self.container)

        # iniciar com clientes
        self.tela_clientes()

    # util
    def limpar_container(self):
        while self.container.count():
            item = self.container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    # -------------------- Clientes --------------------
    def tela_clientes(self):
        self.limpar_container()

        box = QVBoxLayout()

        # busca
        search_row = QHBoxLayout()
        self.input_busca = QLineEdit()
        self.input_busca.setPlaceholderText("Buscar cliente por nome ou email...")
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar_clientes)
        search_row.addWidget(self.input_busca)
        search_row.addWidget(btn_buscar)
        box.addLayout(search_row)

        # tabela
        self.tabela_clientes = QTableWidget()
        self.tabela_clientes.setColumnCount(4)
        self.tabela_clientes.setHorizontalHeaderLabels(["ID", "Nome", "Email", "Número"])
        self.tabela_clientes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        box.addWidget(self.tabela_clientes)

        # formulário
        form = QHBoxLayout()
        self.cli_nome = QLineEdit(); self.cli_nome.setPlaceholderText("Nome")
        self.cli_email = QLineEdit(); self.cli_email.setPlaceholderText("Email")
        self.cli_num = QLineEdit(); self.cli_num.setPlaceholderText("Número")
        self.cli_senha = QLineEdit(); self.cli_senha.setPlaceholderText("Senha")

        btn_add = QPushButton("Cadastrar"); btn_add.clicked.connect(self.cadastrar_cliente_admin)
        btn_update = QPushButton("Atualizar"); btn_update.clicked.connect(self.atualizar_cliente_admin)
        btn_delete = QPushButton("Deletar"); btn_delete.clicked.connect(self.excluir_cliente)

        form.addWidget(self.cli_nome)
        form.addWidget(self.cli_email)
        form.addWidget(self.cli_num)
        form.addWidget(self.cli_senha)
        form.addWidget(btn_add)
        form.addWidget(btn_update)
        form.addWidget(btn_delete)

        box.addLayout(form)

        self.container.addLayout(box)
        self.buscar_clientes()

    def buscar_clientes(self):
        if buscar_cliente is None:
            QMessageBox.critical(self, "Erro", "Função buscar_cliente não encontrada no backend.")
            return
        termo = self.input_busca.text().strip()
        clientes = buscar_cliente(termo)
        self.tabela_clientes.setRowCount(len(clientes))
        for row, (id_, nome, email, numero) in enumerate(clientes):
            self.tabela_clientes.setItem(row, 0, QTableWidgetItem(str(id_)))
            self.tabela_clientes.setItem(row, 1, QTableWidgetItem(nome))
            self.tabela_clientes.setItem(row, 2, QTableWidgetItem(email))
            self.tabela_clientes.setItem(row, 3, QTableWidgetItem(numero))

    def cadastrar_cliente_admin(self):
        if cadastrar_cliente is None:
            QMessageBox.critical(self, "Erro", "Função cadastrar_cliente não encontrada no backend.")
            return
        nome = self.cli_nome.text().strip()
        email = self.cli_email.text().strip()
        numero = self.cli_num.text().strip()
        senha = self.cli_senha.text().strip()
        if not (nome and email and numero and senha):
            QMessageBox.warning(self, "Erro", "Preencha todos os campos")
            return
        cadastrar_cliente(nome, email, numero, senha)
        QMessageBox.information(self, "OK", "Cliente cadastrado!")
        self.buscar_clientes()

    def atualizar_cliente_admin(self):
        if atualizar_cliente is None:
            QMessageBox.critical(self, "Erro", "Função atualizar_cliente não encontrada no backend.")
            return
        row = self.tabela_clientes.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erro", "Selecione um cliente")
            return
        cliente_id = int(self.tabela_clientes.item(row, 0).text())
        nome = self.cli_nome.text().strip()
        email = self.cli_email.text().strip()
        numero = self.cli_num.text().strip()
        senha = self.cli_senha.text().strip()
        atualizar_cliente(cliente_id, email, senha, nome, numero)
        QMessageBox.information(self, "OK", "Cliente atualizado!")
        self.buscar_clientes()

    def excluir_cliente(self):
        if deletar_cliente is None:
            QMessageBox.critical(self, "Erro", "Função deletar_cliente não encontrada no backend.")
            return
        row = self.tabela_clientes.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erro", "Selecione um cliente")
            return
        cliente_id = int(self.tabela_clientes.item(row, 0).text())
        deletar_cliente(cliente_id)
        QMessageBox.information(self, "OK", "Cliente deletado!")
        self.buscar_clientes()

    # -------------------- Serviços --------------------
    def tela_servicos(self):
        self.limpar_container()

        box = QVBoxLayout()

        # tabela
        self.tabela_serv = QTableWidget()
        self.tabela_serv.setColumnCount(3)
        self.tabela_serv.setHorizontalHeaderLabels(["ID", "Nome", "Preço"])
        self.tabela_serv.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        box.addWidget(self.tabela_serv)

        # formulário
        form = QHBoxLayout()
        self.serv_nome = QLineEdit(); self.serv_nome.setPlaceholderText("Nome do serviço")
        self.serv_preco = QLineEdit(); self.serv_preco.setPlaceholderText("Preço")

        btn_add = QPushButton("Adicionar"); btn_add.clicked.connect(self.add_serv)
        btn_up = QPushButton("Atualizar"); btn_up.clicked.connect(self.update_serv)
        btn_del = QPushButton("Deletar"); btn_del.clicked.connect(self.del_serv)

        form.addWidget(self.serv_nome)
        form.addWidget(self.serv_preco)
        form.addWidget(btn_add)
        form.addWidget(btn_up)
        form.addWidget(btn_del)
        box.addLayout(form)

        self.container.addLayout(box)
        self.reload_servicos()

    def reload_servicos(self):
        if listar_servicos is None:
            QMessageBox.critical(self, "Erro", "Função listar_servicos não encontrada no backend.")
            return
        dados = listar_servicos()
        self.tabela_serv.setRowCount(len(dados))
        for row, (id_, nome, preco) in enumerate(dados):
            self.tabela_serv.setItem(row, 0, QTableWidgetItem(str(id_)))
            self.tabela_serv.setItem(row, 1, QTableWidgetItem(nome))
            self.tabela_serv.setItem(row, 2, QTableWidgetItem(str(preco)))

    def add_serv(self):
        if adicionar_servico is None:
            QMessageBox.critical(self, "Erro", "Função adicionar_servico não encontrada no backend.")
            return
        nome = self.serv_nome.text().strip()
        preco = self.serv_preco.text().strip()
        if not (nome and preco):
            QMessageBox.warning(self, "Erro", "Preencha tudo")
            return
        try:
            adicionar_servico(nome, float(preco))
            QMessageBox.information(self, "OK", "Serviço adicionado!")
            self.reload_servicos()
        except ValueError:
            QMessageBox.warning(self, "Erro", "Preço inválido (use ponto como separador decimal).")

    def update_serv(self):
        if atualizar_servico is None:
            QMessageBox.critical(self, "Erro", "Função atualizar_servico não encontrada no backend.")
            return
        row = self.tabela_serv.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erro", "Selecione um serviço")
            return
        serv_id = int(self.tabela_serv.item(row, 0).text())
        nome = self.serv_nome.text().strip()
        preco = self.serv_preco.text().strip()
        try:
            atualizar_servico(serv_id, nome, float(preco))
            QMessageBox.information(self, "OK", "Serviço atualizado!")
            self.reload_servicos()
        except ValueError:
            QMessageBox.warning(self, "Erro", "Preço inválido.")

    def del_serv(self):
        if deletar_servico is None:
            QMessageBox.critical(self, "Erro", "Função deletar_servico não encontrada no backend.")
            return
        row = self.tabela_serv.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erro", "Selecione um serviço")
            return
        serv_id = int(self.tabela_serv.item(row, 0).text())
        deletar_servico(serv_id)
        QMessageBox.information(self, "OK", "Serviço deletado!")
        self.reload_servicos()

    # -------------------- Agendamentos --------------------
    def tela_agendamentos(self):
        self.limpar_container()

        box = QVBoxLayout()

        self.tabela_ag = QTableWidget()
        self.tabela_ag.setColumnCount(6)
        self.tabela_ag.setHorizontalHeaderLabels(
            ["ID", "Cliente", "Serviço", "Data", "Hora", "Status"]
        )
        self.tabela_ag.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        box.addWidget(self.tabela_ag)

        btn_del = QPushButton("Deletar Agendamento")
        btn_del.clicked.connect(self.del_agendamento)
        box.addWidget(btn_del)

        self.container.addLayout(box)
        self.reload_agend()

    def reload_agend(self):
        if listar_agendamentos is None:
            QMessageBox.critical(self, "Erro", "Função listar_agendamentos não encontrada no backend.")
            return
        dados = listar_agendamentos()
        self.tabela_ag.setRowCount(len(dados))
        for row, ag in enumerate(dados):
            for col, value in enumerate(ag):
                self.tabela_ag.setItem(row, col, QTableWidgetItem(str(value)))

    def del_agendamento(self):
        if deletar_agendamento is None:
            QMessageBox.critical(self, "Erro", "Função deletar_agendamento não encontrada no backend.")
            return
        row = self.tabela_ag.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erro", "Selecione um agendamento")
            return
        ag_id = int(self.tabela_ag.item(row, 0).text())
        deletar_agendamento(ag_id)
        QMessageBox.information(self, "OK", "Agendamento deletado!")
        self.reload_agend()


if __name__ == "__main__":
    # para testes locais: cria QApplication e abre painel com usuário admin de teste
    app = QApplication(sys.argv)
    try:
        tela = TelaAdm(usuario=(1, 'admin'))
        tela.show()
        sys.exit(app.exec())
    except PermissionError:
        # se não tiver permissão, fecha app
        sys.exit(1)
