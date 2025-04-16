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
from docx import Document

class WindowCenterClinic:
    def __init__(self, parent=None):
        self.parent = parent
        self.file_path = None
        self.output_path = None
        self.df = pd.DataFrame()
        self.doc = Document()
        self.count_contrat_meditate = 0
        self.count_contrat_therapy = 0
        self.count_aditivo = 0
    
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
        # Cria uma instância da janela de pesquisa
        search_window = SearchWindow(self.parent)
        search_window.exec_()  # Abre a janela de pesquisa como modal

        self.df = search_window.df_search  # Atribui o DataFrame ao self.df

    def process_and_save(self):
        # Abre um diálogo para o usuário escolher a pasta onde os arquivos serão salvos
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder_path = QFileDialog.getExistingDirectory(
            self.parent,
            "Selecione a pasta para salvar os documentos",
            options=options
        )

        # Verifica se o usuário selecionou uma pasta
        if folder_path:
            self.output_path = folder_path  # Armazena o caminho da pasta em self.output_path

            # Verifica qual checkbox está selecionado e executa a função correspondente
            if self.checkbox_contrato_medico.isChecked():
                self.create_contract_meditate()

            QMessageBox.information(self.parent, "Informação", f"Documentos serão salvos na pasta: {self.output_path}")
        else:
            QMessageBox.warning(self.parent, "Aviso", "Nenhuma pasta foi selecionada para salvar os documentos.")
        # print(self.df.head())
        # if self.df.empty:
        #     QMessageBox.warning(self.parent, "Aviso", "Nenhum arquivo carregado!")
        #     return None
        # # mostrar qual checkbox está selecionado
        # if self.checkbox_contrato_medico.isChecked():
        #     print(f'Selecionar a função de contrato médico')

        # if self.checkbox_aditivo.isChecked():
        #     print(f'Selecionar a função de aditivo')

        # if self.checkbox_contratoterapia.isChecked():
        #     print(f'Selecionar a função de contrato terapia')
    
    # Função para limpar o status
    def clear_status(self):
        self.label_status.setText("Nenhum arquivo carregado.")

    def create_contract_meditate(self):
        # Implementar a função de contrato médico
        protocol = self.df['CD_PROTOCOLO'].unique()
        path_document = r'./ARQUIVOS/CONTRATO AMBULATORIAL NDI RP.docx'
        doc = Document(path_document)

        # Salvando o arquivo
        for protocolo in protocol:
            # Criar o nome do arquivo baseado no protocolo
            self.count_contrat_meditate += 1
            df_protocol = self.df[self.df['CD_PROTOCOLO'] == protocolo]
            name_file = f'{self.count_contrat_meditate} - CONTRATO MÉDICO_{protocolo}.docx'
            name_string = df_protocol['NM_RAZAO_NOME'].iloc[0]  # Obtém o nome do DataFrame

            # Atualiza o texto no documento
            self.replace_text(doc, name_string=name_string)  # Substitui o texto no documento

            # Definindo o caminho completo para salvar o arquivo
            path_save = os.path.join(self.output_path, name_file)

            # Salva o documento com o nome do protocolo
            doc.save(path_save)

        QMessageBox.information(self.parent, "Informação", f"Contratos médicos salvos na pasta: {self.output_path}")

    # função para retornar a data de today em formato (dia, mês, ano)
    def date_today(self, value):
        # Obtém a data de today
        today = datetime.now()
        string_date = None
        if value == 0:
            date_complete = today.strftime('%d/%m/%Y')
            date_complete = date_complete.replace('/', '_')
            string_date = date_complete
        
        if value == 1:
            day = today.day
            month = today.month
            dict_month = {
                1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
                5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
                9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
            }
            year = today.year
            month = dict_month.get(month, 'Mês inválido')
            string_date = f'{day} de {month} de {year}'

        return string_date
    
    # Função para corrigir os nomes dos arquivos
    def replace_text(self, doc, name_string):
           # Dicionários de substituição
        dict_replace = {
            'XX de XXX de 20XX': self.date_today(1),
            '@NOME@': name_string,
        }
        # Iterando pelos parágrafos
        for pag, par in enumerate(doc.paragraphs):
            # Substitui os textos do dicionário dict_replace
            for key, value in dict_replace.items():
                if key in par.text:
                    for run in par.runs:
                        if key in run.text:
                            run.text = run.text.replace(key, value)

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


                # Atualiza o self.df_search com os dados encontrados
                self.df_search = df

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
        # Verifica se há dados no DataFrame
        if self.df_search.empty:
            QMessageBox.warning(self, "Aviso", "Nenhuma informação foi encontrada para armazenar!")
            return None

        # Exibe uma mensagem de sucesso e retorna o DataFrame
        QMessageBox.information(self, "Informação", "Informação armazenada com sucesso!")
        return self.df_search