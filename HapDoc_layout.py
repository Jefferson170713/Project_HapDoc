import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView # type: ignore
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon


class HapDoc(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HapDoc")
        self.setGeometry(100, 100, 800, 500)  # Ajuste o tamanho da janela
        self.setWindowIcon(QIcon("./ARQUIVOS/logo/logo.ico"))
        self.initUI()

    def initUI(self):
        # Cria o QWebEngineView para renderizar o HTML
        self.webview = QWebEngineView()

        # Caminho para o arquivo HTML
        path = os.path.abspath("./layout/html/index_hapdoc.html")
        self.webview.setUrl(QUrl.fromLocalFile(path))

        # Adiciona o QWebEngineView à janela principal
        layout = QVBoxLayout()
        layout.addWidget(self.webview)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


# Loop do programa em funcionamento
def main():
    app = QApplication(sys.argv)
    window = HapDoc()
    window.show()
    sys.exit(app.exec_())


# Verifica se o arquivo é executado diretamente
if __name__ == "__main__":
    main()