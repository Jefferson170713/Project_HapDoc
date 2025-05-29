import pandas as pd
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTextEdit
from datetime import datetime
import os
from SearchWindow import SearchWindow

class ServicesWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.file_path = None
        self.output_path = None
        self.df = pd.DataFrame()
        self.progress_bar_process = None

    def create_window_services(self, service_process):
        service = QVBoxLayout()

        # Layout horizontal para o QLabel e o botão "Limpar Status"
        status_layout = QHBoxLayout()

        # QLabel para exibir o status do arquivo
        self.label_status = QLabel("Nenhum arquivo carregado.")
        status_layout.addWidget(self.label_status)

        # Adiciona um espaço expansível para empurrar o botão para a direita
        status_layout.addStretch()

        # Botão para limpar o status
        btn_clear_status = QPushButton("Limpar Status")
        btn_clear_status.setFixedSize(150, 35)
        btn_clear_status.clicked.connect(self.clear_status)
        status_layout.addWidget(btn_clear_status)

        # Adiciona o layout horizontal ao layout vertical principal
        service.addLayout(status_layout)

        # Barra de progresso (agora como atributo da classe)
        self.progress_bar_process = QProgressBar()
        self.progress_bar_process.setValue(0)
        self.progress_bar_process.setMinimum(0)
        self.progress_bar_process.setMaximum(100)
        service.addWidget(self.progress_bar_process)

        # QTextEdit para exibir informações do arquivo carregado
        self.text_edit_info = QTextEdit()
        self.text_edit_info.setReadOnly(True)
        service.addWidget(self.text_edit_info)

        # Separador horizontal
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        service.addWidget(separator)

        # Layout horizontal para os botões
        button_layout = QHBoxLayout()

        # Botão para selecionar o arquivo principal
        btn_search = QPushButton("Pesquisar")
        btn_search.setFixedSize(150, 35)
        btn_search.clicked.connect(self.searchwindow)
        button_layout.addWidget(btn_search)

        # Adiciona um espaço expansível entre os botões
        button_layout.addStretch()

        # Botão para processar e salvar o arquivo
        btn_process_save = QPushButton("Salvar")
        btn_process_save.setFixedSize(150, 35)
        btn_process_save.clicked.connect(self.process_and_save)
        button_layout.addWidget(btn_process_save)

        # Adiciona o layout horizontal ao layout vertical principal
        service.addLayout(button_layout)

        # Configurando o layout na aba
        service_process.setLayout(service)
    
    # Função para pesquisar no banco por protocolo
    def searchwindow(self):
        # Cria uma instância da janela de pesquisa
        search_window = SearchWindow(self.parent)
        search_window.exec_()  # Exibe a janela de forma modal
    
    # Função para processar e salvar o arquivo
    def process_and_save(self):
        print(self.df.head(2))
        if not self.file_path:
            QMessageBox.warning(self.parent, "Aviso", "Nenhum arquivo foi carregado!")
            return

        # Selecionar o local para salvar o arquivo processado
        save_path, _ = QFileDialog.getSaveFileName(self.parent, "Salvar Arquivo", "", "Arquivos Excel (*.xlsx)")
        if not save_path:
            return

        try:
            # Adiciona a extensão .xlsx se não estiver presente
            if not save_path.endswith(".xlsx"):
                save_path += ".xlsx"

            # Adiciona a data e hora ao nome do arquivo
            date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Formato: AAAA-MM-DD_HH-MM-SS
            base_name, ext = os.path.splitext(save_path)  # Divide o caminho em nome base e extensão
            save_path = f"{base_name}_{date}{ext}"  # Adiciona a data ao nome do arquivo

            # Processar o arquivo
            self.output_path = save_path

            # Verifica se o DataFrame self.df está carregado
            if self.df.empty:
                QMessageBox.warning(self.parent, "Aviso", "Os dados não foram carregados corretamente!")
                return

            # Renomeia as colunas antes de salvar
            self.df.rename(
                columns={
                    'CD_SERVIÇO_HONORARIO': 'CÓDIGO AUTORIZAÇÃO',
                    'VALOR_PROPOSTO': 'VALOR',
                    'CD_PROCEDIMENTO_TUSS': 'CÓDIGO TUSS',
                },
                inplace=True
            )

            # # Criando o arquivo Excel com a aba principal
            # with ExcelWriter(save_path, engine='openpyxl') as writer:
            #     # Salvando a aba principal
            #     self.df.to_excel(writer, index=False, sheet_name='GERAL')

            #     # Salvando as abas adicionais
            #     for num, save in enumerate(self.df['URG_ELE_TAX_MAT_MED_CH_ANE_AUX'].unique()):
            #         # Filtrando os dados
            #         filtered_df = self.df[self.df['URG_ELE_TAX_MAT_MED_CH_ANE_AUX'] == save].copy()
            #         sheet_name = f'NEG. {num + 1}'

            #         # Salvando no mesmo arquivo Excel com o nome da aba correspondente
            #         filtered_df.to_excel(writer, index=False, sheet_name=sheet_name)
            print(f"Arquivo processado e salvo em: {save_path}")

            QMessageBox.information(self.parent, "Sucesso", f"Arquivo processado e salvo em:\n{save_path}")

        except Exception as e:
            # Mensagem de erro detalhada
            QMessageBox.critical(self.parent, "Erro", f"Ocorreu um erro ao processar o arquivo:\n{str(e)}")
    
    # Função para limpar o status
    def clear_status(self):
        self.label_status.setText("Nenhum arquivo carregado.")
        self.text_edit_info.clear()
        