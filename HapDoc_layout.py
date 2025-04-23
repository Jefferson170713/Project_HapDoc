import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView # type:ignore
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
import pandas as pd
from ProcedurePackageProcess import ProcedurePackageProcess


class HapDoc(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HapDoc")
        self.setGeometry(100, 100, 800, 500)  # Ajuste o tamanho da janela
        self.setWindowIcon(QIcon("./ARQUIVOS/logo/logo.ico"))
        self.processor = ProcedurePackageProcess()  # Instância do processador
        self.initUI()

    def initUI(self):
        # Cria o QWebEngineView para renderizar o HTML
        self.webview = QWebEngineView()

        # Caminho para o arquivo HTML
        path = os.path.abspath("./layout/html/index_hapdoc.html")
        self.webview.setUrl(QUrl.fromLocalFile(path))

        # Configura o canal de comunicação entre o HTML e o Python
        self.channel = QWebChannel()
        self.channel.registerObject("api", self)  # Registra a classe como API
        self.webview.page().setWebChannel(self.channel)

        # Adiciona o QWebEngineView à janela principal
        layout = QVBoxLayout()
        layout.addWidget(self.webview)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Método para processar o arquivo CSV
    def processFile(self, file_path):
        try:
            print(f"Arquivo recebido: {file_path}")
            self.processor.file_path = file_path
            data = self.processor.load_data()  # Processa o arquivo CSV
            return data.values.tolist()  # Retorna os dados como uma lista de listas
        except Exception as erro:
            print(f"Erro ao processar o arquivo: {erro}")
            return {"error": str(erro)}


# Loop do programa em funcionamento
def main():
    app = QApplication(sys.argv)
    window = HapDoc()
    window.show()
    sys.exit(app.exec_())


# Verifica se o arquivo é executado diretamente
if __name__ == "__main__":
    main()