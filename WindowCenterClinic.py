import pandas as pd
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QWidget
from datetime import datetime
import os
from ARQUIVOS.Oracle_Jdbc.jdbc_permission import JdbcPermission 

class WindowCenterClinic:
    def __init__(self, parent=None):
        self.parent = parent
        self.file_path = None
        self.output_path = None
        self.df = pd.DataFrame()
    
    def create_center_clinic_tab(self, center_clinic):
        layout_center_clinic = QVBoxLayout()

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
        btn_clear_status.clicked.connect(self.clear_status)  # Conecta à função clear_status
        status_layout.addWidget(btn_clear_status)

        # Adiciona o layout horizontal ao layout vertical principal
        layout_center_clinic.addLayout(status_layout)

        # Adiciona os checkboxes para as opções
        checkbox_layout = QHBoxLayout()
        self.checkbox_group = QButtonGroup()
        self.checkbox_group.setExclusive(True)  # Apenas um pode ser selecionado

        self.checkbox_aditivo = QCheckBox("Aditivo")
        self.checkbox_aditivo.setChecked(True)  # Selecionado por padrão
        self.checkbox_group.addButton(self.checkbox_aditivo)
        checkbox_layout.addWidget(self.checkbox_aditivo)

        self.checkbox_contrato_medico = QCheckBox("Contrato Médico")
        self.checkbox_group.addButton(self.checkbox_contrato_medico)
        checkbox_layout.addWidget(self.checkbox_contrato_medico)

        self.checkbox_contratoterapia = QCheckBox("Contrato Terapia")
        self.checkbox_group.addButton(self.checkbox_contratoterapia)
        checkbox_layout.addWidget(self.checkbox_contratoterapia)

        layout_center_clinic.addLayout(checkbox_layout)

        # Separador horizontal
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout_center_clinic.addWidget(separator)

        # Layout horizontal para os botões
        button_layout = QHBoxLayout()

        # Botão para pesquisar o arquivo principal
        btn_search = QPushButton("Pesquisar")
        btn_search.setFixedSize(150, 35)
        btn_search.clicked.connect(self.search_file)  # Função de pesquisa (a ser implementada)
        button_layout.addWidget(btn_search)

        # Adiciona um espaço expansível entre os botões
        button_layout.addStretch()

        # Botão para processar e salvar o arquivo
        btn_process_save = QPushButton("Salvar")
        btn_process_save.setFixedSize(150, 35)
        btn_process_save.clicked.connect(self.process_and_save)
        button_layout.addWidget(btn_process_save)

        # Adiciona o layout horizontal ao layout vertical principal
        layout_center_clinic.addLayout(button_layout)

        # Configurando o layout na aba
        center_clinic.setLayout(layout_center_clinic)
    
    # Função para pesquisar o arquivo principal
    def search_file(self):
        search_window = SearchWindow(self.parent)
        search_window.exec_()  # Abre a janela de pesquisa como modal
    # Função para processar e salvar o arquivo
    def process_and_save(self):
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

            # Criando o arquivo Excel com a aba principal
            with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
                # Salvando a aba principal
                self.df.to_excel(writer, index=False, sheet_name='GERAL')

            QMessageBox.information(self.parent, "Sucesso", f"Arquivo processado e salvo em:\n{save_path}")

        except Exception as erro:
            # Mensagem de erro detalhada
            QMessageBox.critical(self.parent, "Erro", f"Ocorreu um erro ao processar o arquivo:\n{str(erro)}")
    
    # Função para limpar o status
    def clear_status(self):
        self.label_status.setText("Nenhum arquivo carregado.")

class SearchWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pesquisar Dados")
        self.setFixedSize(600, 400)  # Tamanho fixo da janela
        self.init_ui()
        self.df_search = pd.DataFrame()  # DataFrame para armazenar os dados pesquisados
        self.parent = parent  # Armazena a referência ao widget pai

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

        main_layout.addLayout(search_layout)

        # Separador
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator1)

        # Tabela para exibir os resultados
        self.table = QTableWidget()
        self.table.setColumnCount(14)  # Define 14 colunas
        self.table.setHorizontalHeaderLabels([
            "CD_PROTOCOLO", "NM_RAZAO_NOME", "DT_INI_VIGENCIA",
            "CD_ESPECIALIDADE", "DS_ESPECIALIDADE","VL_HORA_PROPOSTO", "CD_LOCAL",
            "CD_ORDEM_LOCAL", "NU_ORDEM_LOCA", "FL_URGENCIA",
            "FL_ELETIVA", "CD_LOCAL_ATENDIMENTO", "NM_FANTASIA", "CD_UF"
        ])
        #self.table.setRowCount()  # Exibe inicialmente 5 linhas
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
                df = jdbc_permission.fetch_data(search_term)

                # Verifica se o DataFrame retornado está vazio
                if df.empty:
                    QMessageBox.warning(self, "Aviso", "Nenhum dado encontrado para o termo pesquisado!")
                    return

                # Define o número de linhas e colunas da tabela com base no DataFrame
                self.table.setRowCount(len(df))
                self.table.setColumnCount(len(df.columns))
                self.table.setHorizontalHeaderLabels(df.columns)

                # Preenche a tabela com os dados do DataFrame
                for row_idx, row_data in df.iterrows():
                    for col_idx, cell_data in enumerate(row_data):
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))

            except Exception as erro:
                QMessageBox.critical(self, "Erro", f"Erro ao buscar dados:\n{str(erro)}")
        else:
            QMessageBox.warning(self, "Aviso", "Digite um termo para pesquisar!")

    def store_information(self):
        # Função para armazenar a informação selecionada (a ser implementada)
        QMessageBox.information(self, "Informação", "Informação armazenada com sucesso!")