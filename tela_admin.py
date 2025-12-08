# ...existing code...
import sys
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
                               QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                               QMessageBox, QApplication)
from PySide6.QtCore import Qt

# permite importar Back
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Back'))

# importa funções do backend com fallback
try:
    from serv import adicionar_servico as backend_adicionar_servico, listar_servicos as backend_listar_servicos
except Exception:
    backend_adicionar_servico = None
    backend_listar_servicos = None

try:
    from agenda import listar_clientes as backend_listar_clientes, listar_agendamentos as backend_listar_agendamentos, confirmar_agendamento as backend_confirmar_agendamento, cancelar_agendamento as backend_cancelar_agendamento
except Exception:
    backend_listar_clientes = None
    backend_listar_agendamentos = None
    backend_confirmar_agendamento = None
    backend_cancelar_agendamento = None

try:
    from cadastrar import cadastrar_cliente as backend_cadastrar_cliente
except Exception:
    backend_cadastrar_cliente = None


class TelaAdmin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Administração")
        self.setGeometry(200, 100, 900, 600)

        main_layout = QVBoxLayout(self)

        # abas
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # aba listar
        self._criar_aba_listar()

        # aba cadastrar cliente
        self._criar_aba_cadastrar_cliente()

        # aba adicionar serviço
        self._criar_aba_adicionar_servico()

        # botão sair
        btn_sair = QPushButton("Sair")
        btn_sair.clicked.connect(self.close)
        main_layout.addWidget(btn_sair, alignment=Qt.AlignRight)

    def _criar_aba_listar(self):
        aba = QWidget()
        layout = QVBoxLayout(aba)

        btn_row = QHBoxLayout()
        btn_clientes = QPushButton("Listar Clientes")
        btn_servicos = QPushButton("Listar Serviços")
        btn_agendamentos = QPushButton("Listar Agendamentos")
        btn_confirmar = QPushButton("Confirmar Agendamento")
        btn_cancelar = QPushButton("Cancelar Agendamento")

        btn_row.addWidget(btn_clientes)
        btn_row.addWidget(btn_servicos)
        btn_row.addWidget(btn_agendamentos)
        btn_row.addWidget(btn_confirmar)
        btn_row.addWidget(btn_cancelar)

        layout.addLayout(btn_row)

        self.tabela_listar = QTableWidget()
        layout.addWidget(self.tabela_listar)

        self.tabs.addTab(aba, "Listar")

        # conexões
        btn_clientes.clicked.connect(self.mostrar_clientes)
        btn_servicos.clicked.connect(self.mostrar_servicos)
        btn_agendamentos.clicked.connect(self.mostrar_agendamentos)
        btn_confirmar.clicked.connect(self.confirmar_agendamento)
        btn_cancelar.clicked.connect(self.cancelar_agendamento)

    def _criar_aba_cadastrar_cliente(self):
        aba = QWidget()
        layout = QVBoxLayout(aba)

        layout.addWidget(QLabel("Nome:"))
        self.in_nome = QLineEdit()
        layout.addWidget(self.in_nome)

        layout.addWidget(QLabel("Email:"))
        self.in_email = QLineEdit()
        layout.addWidget(self.in_email)

        layout.addWidget(QLabel("Telefone:"))
        self.in_tel = QLineEdit()
        layout.addWidget(self.in_tel)

        btn_salvar = QPushButton("Salvar Cliente")
        btn_salvar.clicked.connect(self.salvar_cliente)
        layout.addWidget(btn_salvar)

        self.tabs.addTab(aba, "Cadastrar Cliente")

    def _criar_aba_adicionar_servico(self):
        aba = QWidget()
        layout = QVBoxLayout(aba)

        layout.addWidget(QLabel("Nome do Serviço:"))
        self.in_servico_nome = QLineEdit()
        layout.addWidget(self.in_servico_nome)

        layout.addWidget(QLabel("Preço do Serviço:"))
        self.in_servico_preco = QLineEdit()
        layout.addWidget(self.in_servico_preco)

        btn_salvar_servico = QPushButton("Salvar Serviço")
        btn_salvar_servico.clicked.connect(self.adicionar_servico)
        layout.addWidget(btn_salvar_servico)

        self.tabs.addTab(aba, "Adicionar Serviço")

    # ---- ações ----
    def salvar_cliente(self):
        nome = self.in_nome.text().strip()
        email = self.in_email.text().strip()
        tel = self.in_tel.text().strip()

        if not nome or not email:
            QMessageBox.warning(self, "Erro", "Nome e email são obrigatórios")
            return

        if backend_cadastrar_cliente is None:
            QMessageBox.critical(self, "Erro", "Função de cadastro indisponível (backend não encontrado).")
            return

        try:
            backend_cadastrar_cliente(nome, email, tel, "senhaPadrao")
            QMessageBox.information(self, "OK", "Cliente cadastrado com sucesso!")
            self.in_nome.clear()
            self.in_email.clear()
            self.in_tel.clear()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao cadastrar cliente:\n{e}")

    def mostrar_clientes(self):
        if backend_listar_clientes is None:
            QMessageBox.critical(self, "Erro", "Função listar_clientes indisponível.")
            return
        try:
            dados = backend_listar_clientes()
            self.tabela_listar.clear()
            self.tabela_listar.setRowCount(len(dados))
            self.tabela_listar.setColumnCount(4)
            self.tabela_listar.setHorizontalHeaderLabels(["ID", "Nome", "Email", "Telefone"])
            for r, linha in enumerate(dados):
                for c, valor in enumerate(linha):
                    self.tabela_listar.setItem(r, c, QTableWidgetItem(str(valor)))
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao listar clientes:\n{e}")

    def mostrar_servicos(self):
        if backend_listar_servicos is None:
            QMessageBox.critical(self, "Erro", "Função listar_servicos indisponível.")
            return
        try:
            dados = backend_listar_servicos()
            self.tabela_listar.clear()
            self.tabela_listar.setRowCount(len(dados))
            self.tabela_listar.setColumnCount(3)
            self.tabela_listar.setHorizontalHeaderLabels(["ID", "Nome", "Preço"])
            for r, linha in enumerate(dados):
                for c, valor in enumerate(linha):
                    self.tabela_listar.setItem(r, c, QTableWidgetItem(str(valor)))
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao listar serviços:\n{e}")

    def mostrar_agendamentos(self):
        if backend_listar_agendamentos is None:
            QMessageBox.critical(self, "Erro", "Função listar_agendamentos indisponível.")
            return
        try:
            dados = backend_listar_agendamentos()
            self.tabela_listar.clear()
            self.tabela_listar.setRowCount(len(dados))
            # inclui status na tabela
            self.tabela_listar.setColumnCount(6)
            self.tabela_listar.setHorizontalHeaderLabels(["ID", "Cliente", "Serviço", "Data", "Hora", "Status"])
            for r, linha in enumerate(dados):
                for c, valor in enumerate(linha):
                    self.tabela_listar.setItem(r, c, QTableWidgetItem(str(valor)))
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao listar agendamentos:\n{e}")

    def confirmar_agendamento(self):
        linha = self.tabela_listar.currentRow()
        if linha == -1:
            QMessageBox.warning(self, "Erro", "Selecione um agendamento para confirmar.")
            return
        if backend_confirmar_agendamento is None:
            QMessageBox.critical(self, "Erro", "Função confirmar_agendamento indisponível.")
            return
        agendamento_id = int(self.tabela_listar.item(linha, 0).text())
        try:
            backend_confirmar_agendamento(agendamento_id)
            QMessageBox.information(self, "OK", "Agendamento confirmado.")
            self.mostrar_agendamentos()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao confirmar:\n{e}")

    def cancelar_agendamento(self):
        linha = self.tabela_listar.currentRow()
        if linha == -1:
            QMessageBox.warning(self, "Erro", "Selecione um agendamento para cancelar.")
            return
        if backend_cancelar_agendamento is None:
            QMessageBox.critical(self, "Erro", "Função cancelar_agendamento indisponível.")
            return
        agendamento_id = int(self.tabela_listar.item(linha, 0).text())
        try:
            backend_cancelar_agendamento(agendamento_id)
            QMessageBox.information(self, "OK", "Agendamento cancelado.")
            self.mostrar_agendamentos()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao cancelar:\n{e}")

    def adicionar_servico(self):
        nome = self.in_servico_nome.text().strip()
        preco_text = self.in_servico_preco.text().strip()
        if not nome or not preco_text:
            QMessageBox.warning(self, "Erro", "Nome e preço são obrigatórios")
            return
        try:
            preco = float(preco_text)
        except ValueError:
            QMessageBox.warning(self, "Erro", "Preço deve ser um número válido")
            return

        if backend_adicionar_servico is None:
            QMessageBox.critical(self, "Erro", "Função adicionar_servico indisponível.")
            return

        try:
            backend_adicionar_servico(nome, preco)
            QMessageBox.information(self, "OK", "Serviço adicionado com sucesso!")
            self.in_servico_nome.clear()
            self.in_servico_preco.clear()
            self.mostrar_servicos()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao adicionar serviço:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela = TelaAdmin()
    tela.show()
    sys.exit(app.exec())