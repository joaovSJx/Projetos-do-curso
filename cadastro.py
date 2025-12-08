import sys
from banco import conectar
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Back'))
from cadastrar import cadastrar_conta, verificar_cadastro

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Cadastro - Login e Cadastro")
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        # Campos comuns
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Email")
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_edit)

        self.senha_edit = QLineEdit()
        self.senha_edit.setPlaceholderText("Senha")
        self.senha_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Senha:"))
        layout.addWidget(self.senha_edit)

        self.nome_edit = QLineEdit()
        self.nome_edit.setPlaceholderText("Nome")
        layout.addWidget(QLabel("Nome:"))
        layout.addWidget(self.nome_edit)

        self.numero_edit = QLineEdit()
        self.numero_edit.setPlaceholderText("Número")
        layout.addWidget(QLabel("Número:"))
        layout.addWidget(self.numero_edit)

        # Botões
        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        button_layout.addWidget(self.login_button)

        self.cadastrar_button = QPushButton("Cadastrar")
        self.cadastrar_button.clicked.connect(self.cadastrar)
        button_layout.addWidget(self.cadastrar_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def login(self):
        email = self.email_edit.text()
        senha = self.senha_edit.text()
        nome = self.nome_edit.text()
        numero = self.numero_edit.text()

        if verificar_cadastro(email, senha, nome, numero):
            QMessageBox.information(self, "Sucesso", "Login realizado com sucesso!")
        else:
            QMessageBox.warning(self, "Erro", "Credenciais inválidas!")
    