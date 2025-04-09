from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from ProcedurePackageProcess import ProcedurePackageProcess

class WindowProcedurePackage:
    def __init__(self, parent=None):
        self.parent = parent
        self.file_path = None
        self.model_path = "./modelo_cod_renomeacao.csv"
        self.sigo_path = "./ARQUIVOS/de_para_sigo.csv"
        self.output_path = None
    
    # Criar a aba de "Pacote Procedimento"
    def create_procedures_and_package_tab(self, procedures_package):
        layout_procedures_package = QVBoxLayout()

        # QLabel para exibir o status do arquivo
        self.label_status = QLabel("Nenhum arquivo carregado.")
        layout_procedures_package.addWidget(self.label_status)

        # Botão para selecionar o arquivo principal
        btn_select_file = QPushButton("Selecionar Arquivo")
        btn_select_file.clicked.connect(self.select_file)
        layout_procedures_package.addWidget(btn_select_file)

        # QTextEdit para exibir informações do arquivo carregado
        self.text_edit_info = QTextEdit()
        self.text_edit_info.setReadOnly(True)
        layout_procedures_package.addWidget(self.text_edit_info)

        # Separador horizontal
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout_procedures_package.addWidget(separator)

        # Botão para processar e salvar o arquivo
        btn_process_save = QPushButton("Processar e Salvar")
        btn_process_save.clicked.connect(self.process_and_save)
        layout_procedures_package.addWidget(btn_process_save)

        # Configurando o layout na aba
        procedures_package.setLayout(layout_procedures_package)
    
    # Função para selecionar o arquivo principal
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.parent, "Selecionar Arquivo", "", "Arquivos CSV (*.csv)")
        if file_path:
            self.file_path = file_path
            self.label_status.setText(f"Arquivo carregado: {file_path}")
            self.text_edit_info.setText(f"Arquivo selecionado:\n{file_path}")
        else:
            self.label_status.setText("Nenhum arquivo carregado.")
            self.text_edit_info.clear()
    
    # Função para processar e salvar o arquivo
    def process_and_save(self):
        if not self.file_path:
            QMessageBox.warning(self.parent, "Aviso", "Nenhum arquivo foi carregado!")
            return

        # Selecionar o local para salvar o arquivo processado
        save_path, _ = QFileDialog.getSaveFileName(self.parent, "Salvar Arquivo", "", "Arquivos Excel (*.xlsx)")
        if not save_path:
            return

        # Processar o arquivo
        try:
            self.output_path = save_path
            self.load_data()
            self.process_data()
            self.save_to_excel()

            QMessageBox.information(self.parent, "Sucesso", f"Arquivo processado e salvo em:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(self.parent, "Erro", f"Ocorreu um erro ao processar o arquivo:\n{str(e)}")