import sys
from itertools import permutations
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from WindowProcedurePackage import WindowProcedurePackage


# Classe principal da aplicação
class HapDoc(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HapDoc")
        self.setGeometry(100, 100, 600, 300)
        self.setWindowIcon(QIcon("./ARQUIVOS/logo/logo.ico"))
        self.program_hapdoc = QTabWidget()
        self.procedures_package = QWidget()
        self.procedures_package_ = QWidget()
        # Instanciando a classe ProcedurePackageProcess
        self.procedure_package_process = WindowProcedurePackage(parent=self)

        self.createview()

    # Função para criar as abas do programa
    def createview(self):
        space = 5 * ' '
        self.setCentralWidget(self.program_hapdoc)
        self.program_hapdoc.addTab(self.procedures_package, f'{space} Pacotes e Procedimentos {space}')
        self.program_hapdoc.addTab(self.procedures_package_, f'{space} Centro Clínico {space}')
        self.program_hapdoc.setDocumentMode(True)
        self.program_hapdoc.setMovable(True)
        # Criando a aba "Pacote Procedimento"
        self.procedure_package_process.create_procedures_and_package_tab(self.procedures_package)


# Loop do programa em funcionamento
def main():
    app = QApplication(sys.argv)
    window = HapDoc()
    window.show()
    sys.exit(app.exec_())

# Verifica se o arquivo é executado diretamente
if __name__ == "__main__":
    main()
        