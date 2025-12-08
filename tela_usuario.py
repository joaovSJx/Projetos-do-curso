import sys
import os
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget, QApplication
from PySide6.QtCore import Qt

# permite importar módulos do Back se precisar (opcional)
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Back'))

class TelaUsuario(QWidget):
    def __init__(self, usuario_id=None):
        super().__init__()
        self.usuario_id = usuario_id
        self.setWindowTitle("Tela do Usuário")
        self.resize(600, 400)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        self.lbl_welcome = QLabel("Bem-vindo(a)!")
        self.lbl_welcome.setAlignment(Qt.AlignCenter)
        self.lbl_welcome.setStyleSheet("font-size:18px; font-weight:600;")
        layout.addWidget(self.lbl_welcome)

        self.lbl_info = QLabel(f"ID do usuário: {self.usuario_id}" if self.usuario_id else "Nenhum usuário logado")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_info)

        self.lista_agend = QListWidget()
        layout.addWidget(self.lista_agend)

        self.btn_atualizar = QPushButton("Atualizar")
        self.btn_sair = QPushButton("Fechar")
        self.btn_atualizar.clicked.connect(self.atualizar)
        self.btn_sair.clicked.connect(self.fechar)
        layout.addWidget(self.btn_atualizar)
        layout.addWidget(self.btn_sair, alignment=Qt.AlignRight)

        self.setLayout(layout)
        self.atualizar()

    def atualizar(self):
        self.lista_agend.clear()
        if self.usuario_id:
            self.lista_agend.addItem(f"Agendamento 1 do usuário {self.usuario_id}")
            self.lista_agend.addItem(f"Agendamento 2 do usuário {self.usuario_id}")
        else:
            self.lista_agend.addItem("Nenhum agendamento encontrado")

    def fechar(self):
        self.close()
