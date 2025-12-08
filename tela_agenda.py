from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from agend import (
    criar_agendamento,
    buscar_agendamentos,
    atualizar_agendamento,
    deletar_agendamento,
)


class TelaAgendamentos(QWidget):
    def _init_(self):
        super()._init_()
        self.setWindowTitle("Gerenciar Agendamentos")
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout()
        titulo = QLabel("AGENDAMENTOS")
        titulo.setFont(QFont("Arial", 22, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # campos
        self.input_cliente = QLineEdit()
        self.input_cliente.setPlaceholderText("ID do Cliente")

        self.input_servico = QLineEdit()
        self.input_servico.setPlaceholderText("ID do Serviço")

        self.input_data = QLineEdit()
        self.input_data.setPlaceholderText("Data (AAAA-MM-DD)")

        self.input_hora = QLineEdit()
        self.input_hora.setPlaceholderText("Hora (HH:MM)")

        layout.addWidget(self.input_cliente)
        layout.addWidget(self.input_servico)
        layout.addWidget(self.input_data)
        layout.addWidget(self.input_hora)

        # botões superiores
        btns_top = QHBoxLayout()

        self.btn_confirmar = QPushButton("Confirmar Agendamento")
        self.btn_confirmar.clicked.connect(self.confirmar_agendamento)

        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.carregar_tabela)

        self.btn_limpar = QPushButton("Limpar Campos")
        self.btn_limpar.clicked.connect(self.limpar_campos)

        btns_top.addWidget(self.btn_confirmar)
        btns_top.addWidget(self.btn_buscar)
        btns_top.addWidget(self.btn_limpar)

        layout.addLayout(btns_top)

        # tabela de agendamentos
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(
            ["ID", "Cliente", "Serviço", "Data", "Hora"]
        )
        self.tabela.cellClicked.connect(self.preencher_campos)

        layout.addWidget(self.tabela)

        # botões inferiores
        btns_bottom = QHBoxLayout()

        self.btn_atualizar = QPushButton("Atualizar")
        self.btn_atualizar.clicked.connect(self.atualizar)

        self.btn_deletar = QPushButton("Excluir")
        self.btn_deletar.clicked.connect(self.deletar)

        btns_bottom.addWidget(self.btn_atualizar)
        btns_bottom.addWidget(self.btn_deletar)

        layout.addLayout(btns_bottom)

        self.setLayout(layout)

        # Carrega tabela inicial
        self.carregar_tabela()

    # tabela de agendamentos
    def carregar_tabela(self):
        agendamentos = buscar_agendamentos()

        self.tabela.setRowCount(0)

        for linha, ag in enumerate(agendamentos):
            self.tabela.insertRow(linha)
            for coluna, valor in enumerate(ag):
                self.tabela.setItem(linha, coluna, QTableWidgetItem(str(valor)))

    # preencher campos
    def preencher_campos(self, row, column):
        self.id_agendamento = self.tabela.item(row, 0).text()
        self.input_cliente.setText(self.tabela.item(row, 1).text())
        self.input_servico.setText(self.tabela.item(row, 2).text())
        self.input_data.setText(self.tabela.item(row, 3).text())
        self.input_hora.setText(self.tabela.item(row, 4).text())

    # confirmar agendamento
    def confirmar_agendamento(self):
        cliente = self.input_cliente.text()
        servico = self.input_servico.text()
        data = self.input_data.text()
        hora = self.input_hora.text()

        if not cliente or not servico or not data or not hora:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return

        criar_agendamento(cliente, servico, data, hora)

        QMessageBox.information(self, "Sucesso", "Agendamento criado!")
        self.carregar_tabela()
        self.limpar_campos()

    # atyualizar agendamento
    def atualizar(self):
        try:
            atualizar_agendamento(
                self.id_agendamento,
                self.input_cliente.text(),
                self.input_servico.text(),
                self.input_data.text(),
                self.input_hora.text(),
            )

            QMessageBox.information(self, "OK", "Agendamento atualizado!")
            self.carregar_tabela()
        except:
            QMessageBox.warning(self, "Erro", "Selecione um agendamento na tabela.")

    # deletar agendamento
    def deletar(self):
        try:
            deletar_agendamento(self.id_agendamento)
            QMessageBox.information(self, "OK", "Agendamento deletado!")
            self.carregar_tabela()
            self.limpar_campos()
        except:
            QMessageBox.warning(self, "Erro", "Selecione um agendamento.")

    # limpar camposS
    def limpar_campos(self):
        self.input_cliente.clear()
        self.input_servico.clear()
        self.input_data.clear()
        self.input_hora.clear()