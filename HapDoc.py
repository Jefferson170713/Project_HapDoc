import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QWidget
#from WindowProcedurePackage import WindowProcedurePackage
from PackageToProcedureWindow import PackageToProcedureWindow
from WindowCenterClinic import WindowCenterClinic
from ServiceWindow import ServicesWindow


# Classe principal da aplicação
class HapDoc(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HapDoc")
        self.setGeometry(100, 100, 600, 300)
        self.setWindowIcon(QIcon("./ARQUIVOS/logo/logo.ico"))
        self.program_hapdoc = QTabWidget()
        self.procedures_package = QWidget()
        self.center_clinic = QWidget()
        self.service = QWidget()
        # Instanciando a classe ProcedurePackageProcess
        #self.procedure_package_process = WindowProcedurePackage(parent=self)
        self.procedure_package_process = PackageToProcedureWindow(parent=self)
        self.center_clinic_process = WindowCenterClinic(parent=self)
        self.services_process = ServicesWindow(parent=self)

        self.createview()

    # Função para criar as abas do programa
    def createview(self):
        space = 5 * '   '
        self.setCentralWidget(self.program_hapdoc)
        self.program_hapdoc.addTab(self.procedures_package, f'{space} Pacote por Procedimento {space}')
        self.program_hapdoc.addTab(self.center_clinic, f'{space} Centro Clínico {space}')
        self.program_hapdoc.addTab(self.service, f'{space} Serviços {space}')
        self.program_hapdoc.setDocumentMode(True)
        self.program_hapdoc.setMovable(True)
        # Criando a aba "Pacote Procedimento"
        self.procedure_package_process.create_window_packagetoprocedure(self.procedures_package)
        self.center_clinic_process.create_center_clinic_tab(self.center_clinic)
        self.services_process.create_window_services(self.service)


# Loop do programa em funcionamento
def main():
    app = QApplication(sys.argv)
    window = HapDoc()
    window.show()
    sys.exit(app.exec_())

# Verifica se o arquivo é executado diretamente
if __name__ == "__main__":
    main()
        