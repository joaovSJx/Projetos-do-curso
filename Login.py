import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QMessageBox, QStackedWidget
)
from PySide6.QtCore import Qt, QTimer

# telas externas
from tela_login import TelaLogin
from tela_usuario import TelaUsuario
from tela_admin import TelaAdmin

# garantir import do Back e Front
ROOT_BACK = os.path.join(os.path.dirname(__file__), '..', 'Back')
ROOT_FRONT = os.path.join(os.path.dirname(__file__), '..', 'Front')
sys.path.insert(0, ROOT_BACK)
sys.path.insert(0, ROOT_FRONT)

from cadastrar import cadastrar_conta, verificar_login


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login / Cadastro")
        self.setGeometry(300, 300, 420, 260)
        self.usuario_logado = None  # (id, tipo)

        # Stack de páginas
        self.stack = QStackedWidget(self)
        main = QVBoxLayout(self)
        main.addWidget(self.stack)

        # --- Página 0: Tela de Login 
        self.tela_login = TelaLogin()
        self.tela_login.signal_login.connect(self.login)          # recebe email e senha
        self.tela_login.signal_cadastro.connect(lambda: self.stack.setCurrentIndex(1))
        self.stack.addWidget(self.tela_login)

        # --- Página 1: Cadastro ---
        from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
        p_cad = QWidget()
        C = QVBoxLayout(p_cad)
        C.addWidget(QLabel("Cadastro de Cliente"))

        C.addWidget(QLabel("Nome:"))
        self.cad_nome = QLineEdit()
        C.addWidget(self.cad_nome)

        C.addWidget(QLabel("Número:"))
        self.cad_numero = QLineEdit()
        C.addWidget(self.cad_numero)

        C.addWidget(QLabel("Email:"))
        self.cad_email = QLineEdit()
        C.addWidget(self.cad_email)

        C.addWidget(QLabel("Senha:"))
        self.cad_senha = QLineEdit()
        self.cad_senha.setEchoMode(QLineEdit.Password)
        C.addWidget(self.cad_senha)

        row2 = QHBoxLayout()
        btn_cadastrar = QPushButton("Cadastrar")
        btn_cadastrar.clicked.connect(self.cadastrar)

        btn_back = QPushButton("Voltar")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        row2.addWidget(btn_cadastrar)
        row2.addWidget(btn_back)
        C.addLayout(row2)

        self.stack.addWidget(p_cad)

        # --- Página 2: Redirecionamento ---
        p_redirect = QWidget()
        R = QVBoxLayout(p_redirect)

        self.lbl_redirect = QLabel("Redirecionando...")
        self.lbl_redirect.setAlignment(Qt.AlignCenter)
        R.addWidget(self.lbl_redirect)

        self.stack.addWidget(p_redirect)

    # LOGIN
    def login(self, email, senha):
        email = email.strip()
        senha = senha.strip()

        if not email or not senha:
            QMessageBox.warning(self, "Erro", "Preencha email e senha")
            return

        resultado = verificar_login(email, senha)

        if not resultado:
            QMessageBox.warning(self, "Erro", "Email ou senha inválidos")
            return

        usuario_id, tipo = resultado
        self.usuario_logado = (usuario_id, tipo)

        # mostra a página 2 (terceira etapa)
        self.lbl_redirect.setText(f"Entrando como {'Administrador' if tipo=='admin' else 'Cliente'}...")
        self.stack.setCurrentIndex(2)

        # redireciona depois de 0.3s
        QTimer.singleShot(300, self.abrir_tela_pos_login)

    def abrir_tela_pos_login(self):
        if not self.usuario_logado:
            return

        usuario_id, tipo = self.usuario_logado

        try:
            if tipo == 'admin':
                self.tela_admin = TelaAdmin(usuario=(usuario_id, tipo))
                self.tela_admin.show()
            else:
                self.tela_usuario = TelaUsuario(usuario_id)
                self.tela_usuario.show()

        except PermissionError:
            QMessageBox.critical(self, "Erro", "Acesso negado (login necessário).")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao abrir tela:\n{e}")

    # CADASTRO
    def cadastrar(self):
        nome = self.cad_nome.text().strip()
        numero = self.cad_numero.text().strip()
        email = self.cad_email.text().strip()
        senha = self.cad_senha.text().strip()

        if not (nome and numero and email and senha):
            QMessageBox.warning(self, "Erro", "Preencha todos os campos")
            return

        try:
            cadastrar_conta(nome, email, numero, senha)

            QMessageBox.information(self, "Sucesso", "Conta criada com sucesso!")

            self.cad_nome.clear()
            self.cad_numero.clear()
            self.cad_email.clear()
            self.cad_senha.clear()

            self.stack.setCurrentIndex(0)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao cadastrar:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    sys.exit(app.exec())

