import sys
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QApplication, QMessageBox
)
from PySide6.QtGui import QPixmap, QFont, QColor, QPalette
from PySide6.QtCore import Qt

class TelaLogin(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login - Barbershop")
        self.setGeometry(300, 50, 500, 700)

        # fundo
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 500, 700) 
        self.background.setPixmap(QPixmap("FundoBarbearia.jpg").scaled(
            500, 700, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        ))
        self.background.lower()

        
        # layout principal
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # título
        self.titulo = QLabel("Barbershop")
        fonte = QFont("Segoe Script", 48)
        fonte.setBold(True)
        self.titulo.setFont(fonte)
        self.titulo.setStyleSheet("""
            color: #d4af37;   /* dourado */
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        """)
        self.titulo.setAlignment(Qt.AlignCenter)

        #  caixa de login
        box = QWidget()
        box_layout = QVBoxLayout(box)
        box_layout.setSpacing(12)
        box_layout.setContentsMargins(40, 30, 40, 30)

        box.setStyleSheet("""
            background-color: rgba(0, 0, 0, 130);
            border: 2px solid #d4af37;
            border-radius: 15px;
        """)

        # Campos de entrada
        
        self.email = QLineEdit()
        self.email.setPlaceholderText("E-mail")
        self.email.setStyleSheet("""
            background: white;
            padding: 10px;
            border-radius: 8px;
        """)

        self.senha = QLineEdit()
        self.senha.setEchoMode(QLineEdit.Password)
        self.senha.setPlaceholderText("Senha")
        self.senha.setStyleSheet("""
            background: white;
            padding: 10px;
            border-radius: 8px;
        """)

        # botão login
        self.btn_login = QPushButton("Login")
        self.btn_login.setStyleSheet("""
            background-color: #d4af37;
            color: white;
            padding: 10px;
            font-size: 18px;
            border-radius: 8px;
        """)

        #botão cadastro
        self.btn_cadastro = QPushButton("Cadastrar-se")
        self.btn_cadastro.setStyleSheet("""
            background-color: #0b4257;
            color: white;
            padding: 10px;
            font-size: 16px;
            border-radius: 8px;
        """)

        # adicionando ao layout
        box_layout.addWidget(self.email)
        box_layout.addWidget(self.senha)
        box_layout.addWidget(self.btn_login)
        box_layout.addWidget(self.btn_cadastro)

        layout.addWidget(self.titulo)
        layout.addSpacing(20)
        layout.addWidget(box)

        # eventos dos botões (você liga ao seu backend)
        self.btn_login.clicked.connect(self.fazer_login)
        self.btn_cadastro.clicked.connect(self.abrir_cadastro)

    
    def fazer_login(self):
        email = self.email.text().strip()
        senha = self.senha.text().strip()

        if not email or not senha:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return

        # Aqui você conecta ao seu backend!
        print("Login:", email, senha)

    def abrir_cadastro(self):
        print("Abrir tela de cadastro")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    t = TelaLogin()
    t.show()
    sys.exit(app.exec())
