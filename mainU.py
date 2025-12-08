import sys
import os
from PySide6.QtWidgets import QApplication

# garante que a raiz do projeto e as pastas Front/Back fiquem no sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'Front'))
sys.path.insert(0, os.path.join(ROOT, 'Back'))

from Login import LoginWindow

app = QApplication(sys.argv)
janela = LoginWindow()
janela.show()
sys.exit(app.exec())