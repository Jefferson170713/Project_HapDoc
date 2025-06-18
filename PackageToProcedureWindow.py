import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTextEdit
import os
#from SearchWindow import SearchWindow
from ARQUIVOS.Oracle_Jdbc.jdbc_packges_by_procedures import JdbcPermission

class PackageToProcedureWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.file_path = None
        self.output_path = None
        self.df = pd.DataFrame()
        self.progress_bar_process = None
        self.df_search = pd.DataFrame()  # DataFrame para armazenar os dados pesquisados

    def create_window_packagetoprocedure(self, service_process):
        service = QVBoxLayout()

        # Layout horizontal para o QLabel e o botão "Limpar Status"
        status_layout = QHBoxLayout()

        # QLabel para exibir o status do arquivo
        self.label_status_win_one = QLabel("Nenhum arquivo carregado.")
        status_layout.addWidget(self.label_status_win_one)

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
        self.df_search = search_window.df_search
    
    # Função para processar e salvar o arquivo
    def process_and_save(self):
        ...
        
    
    # Função para limpar o status
    def clear_status(self):
        self.progress_bar_process.setValue(0)
        self.label_status_win_one.setText("Nenhum arquivo carregado.")

    
    def save_to_excel(self, df, file_path):

        ...



class SearchWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pesquisar Dados")
        self.setFixedSize(600, 400)  # Tamanho fixo da janela
        self.init_ui()
        self.df_search = pd.DataFrame()  # DataFrame para armazenar os dados pesquisados
        self.parent = parent  # Armazena a referência ao widget pai
        #elf.progress_bar_process_search = None

    def init_ui(self):
        # Cria o layout principal
        main_layout = QVBoxLayout()

        # Linha para entrada de texto e botão de pesquisa
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Digite os Protocolos...")
        search_layout.addWidget(self.search_input)

        btn_search = QPushButton("Pesquisar")
        btn_search.setFixedSize(100, 30)
        btn_search.clicked.connect(self.perform_search)  # Conecta à função de pesquisa
        search_layout.addWidget(btn_search)

        # Barra de progresso (agora como atributo da classe)
        self.progress_bar_process_search = QProgressBar()
        self.progress_bar_process_search.setValue(0)
        self.progress_bar_process_search.setMinimum(0)
        self.progress_bar_process_search.setMaximum(100)
        main_layout.addWidget(self.progress_bar_process_search)

        self.label_status = QLabel("Status: Nenhuma pesquisa realizada.")
        main_layout.addWidget(self.label_status)


        main_layout.addLayout(search_layout)

        # Separador
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator1)

        # Tabela para exibir os resultados
        self.table = QTableWidget()
        self.table.setColumnCount(15)  # Define 15 colunas
        self.table.setHorizontalHeaderLabels(
            ['TABELA', 'LOCAL_CAPA', 'CD_PROCEDIMENTO', 'CD_PROCEDIMENTO_TUSS',
            'NM_PROCEDIMENTO', 'NM_PROCEDIMENTO_TUSS', 'NU_ORDEM_PACOTE',
            'CD_TIPO_ACOMODACAO', 'URG_ELE_TAX_MAT_MED_CIR_ANE_AUX', 'VALOR',
            'CD_TIPO_REDE_ATENDIMENTO']
        )
        main_layout.addWidget(self.table)

        # Separador
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator2)

        # Botão para armazenar a informação (centralizado)
        btn_store_layout = QHBoxLayout()
        btn_store = QPushButton("Armazenar Informação")
        btn_store.setFixedSize(200, 40)
        btn_store.clicked.connect(self.store_information)  # Conecta à função de armazenamento
        btn_store_layout.addStretch()  # Adiciona espaço antes do botão
        btn_store_layout.addWidget(btn_store)
        btn_store_layout.addStretch()  # Adiciona espaço depois do botão
        main_layout.addLayout(btn_store_layout)

        # Adiciona o layout principal a um widget para o QScrollArea
        container_widget = QWidget()
        container_widget.setLayout(main_layout)

        # Cria uma área de rolagem
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container_widget)

        # Define o layout da janela
        window_layout = QVBoxLayout()
        window_layout.addWidget(scroll_area)
        self.setLayout(window_layout)

    def perform_search(self):
        # Obtém o termo de pesquisa e o caminho do driver JDBC
        search_term = self.search_input.text()
        path_drive = r'./ARQUIVOS/Oracle_Jdbc/ojdbc8.jar'

        if search_term:
            try:
                # Instancia a classe JdbcPermission
                jdbc_permission = JdbcPermission(path_drive)

                # Usa o método fetch_data para buscar os dados
                self.df_search, protocol = jdbc_permission.fetch_data(search_term, chunk_size=50000, progress_bar=self.progress_bar_process_search)

                self.label_status.setText(f"{len(self.df_search)} linhas carregadas.")
                # Atualiza o self.df_search com os dados encontrados
                #self.df_search = df

                # Define o número de linhas e colunas da tabela com base no DataFrame
                self.table.setRowCount(len(self.df_search))
                self.table.setColumnCount(len(self.df_search.columns))
                self.table.setHorizontalHeaderLabels(self.df_search.columns)

                # Preenche a tabela com os dados do DataFrame
                for row_idx, row_data in self.df_search.iterrows():
                    for col_idx, cell_data in enumerate(row_data):
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))

                if self.df_search.empty:
                    QMessageBox.warning(self, 'Aviso', f'Protocolo(s): ( {protocol} ) inelegível para automatização de documentos. \n\nSolicita-se verificação com a coordenação.')

            except Exception as erro:
                QMessageBox.critical(self, "Erro", f"Erro ao buscar dados:\n{str(erro)}")
        else:
            QMessageBox.warning(self, "Aviso", "Digite um termo para pesquisar!")

    def store_information(self):
        # Verifica se há dados no DataFrame
        if self.df_search.empty:
            QMessageBox.warning(self, "Aviso", "Nenhuma informação foi encontrada para armazenar!")
            return None

        # Exibe uma mensagem de sucesso e retorna o DataFrame
        QMessageBox.information(self, "Informação", "Informação armazenada com sucesso!")
        return self.df_search