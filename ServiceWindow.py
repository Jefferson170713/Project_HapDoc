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
from ARQUIVOS.Oracle_Jdbc.jdbc_servicos import JdbcPermission 

class ServicesWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.file_path = None
        self.output_path = None
        self.df = pd.DataFrame()
        self.progress_bar_process = None
        self.df_search = pd.DataFrame()  # DataFrame para armazenar os dados pesquisados

    def create_window_services(self, service_process):
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
        if self.df_search.empty:
            QMessageBox.warning(self.parent, "Aviso", "Nenhum dado carregado para salvar!")
            return

        # Pede apenas o diretório onde salvar
        folder = QFileDialog.getExistingDirectory(
            self.parent,
            "Selecione a pasta para salvar o arquivo"
        )
        if not folder:
            return  # Usuário cancelou

        # Gera o nome do arquivo automaticamente
        protocolo = str(self.df_search['CD_PROTOCOLO'].iloc[0])
        file_name = f"PROTOCOLO_{protocolo}.xlsx"
        save_path = os.path.join(folder, file_name)

        try:
            self.df_search = self.adjust_values()
            self.progress_bar_process.setValue(20)
            self.df_search = self.creating_the_master_key()
            self.progress_bar_process.setValue(45)
            self.df_search = self.grouping_the_networks()
            self.progress_bar_process.setValue(75)
            self.df_search = self.breaking_the_primary_key_into_columns()
            self.progress_bar_process.setValue(95)

            self.save_to_excel(self.df_search, save_path)

            self.progress_bar_process.setValue(100)
            self.label_status_win_one.setText(f"{self.df_search.shape[0]} linhas carregadas e salvas no arquivo Excel.")
            #QMessageBox.information(self.parent, "Sucesso", f"Arquivo salvo em:\n{save_path}")
        except Exception as erro:
            QMessageBox.critical(self.parent, "Erro", f"Ocorreu um erro ao salvar o arquivo:\n{str(erro)}")
    
    # Função para limpar o status
    def clear_status(self):
        self.progress_bar_process.setValue(0)
        self.label_status_win_one.setText("Nenhum arquivo carregado.")
    
    def adjust_values(self):
        df_search = self.df_search.copy()
        df_search['CD_PROCEDIMENTO_TUSS'] = df_search['CD_PROCEDIMENTO_TUSS'].fillna(0).astype(str)
        df_search['CD_SERV_HONORARIO'] = df_search['CD_SERV_HONORARIO'].fillna(0)
        df_search['VL_FILME_PROPOSTO'] = df_search['VL_FILME_PROPOSTO'].fillna(0).astype(float)
        df_search['NM_PROCEDIMENTO_TUSS'] = df_search['NM_PROCEDIMENTO_TUSS'].fillna('-')
        df_search['CD_PROCEDIMENTO_TUSS'] = df_search['CD_PROCEDIMENTO_TUSS'].astype(int)
        df_search['CD_SERV_HONORARIO'] = df_search['CD_SERV_HONORARIO'].astype(str)#

        df_search['VL_PROPOSTO'] = df_search['VL_PROPOSTO'].astype(float).map(lambda x: '{:.5f}'.format(x).replace('.', ','))
        df_search['VL_DEFLATOR'] = df_search['VL_DEFLATOR'].astype(float).map(lambda x: '{:.5f}'.format(x).replace('.', ','))
        df_search['VL_DEFLATOR_UCO'] = df_search['VL_DEFLATOR_UCO'].astype(float).map(lambda x: '{:.5f}'.format(x).replace('.', ','))
        df_search['VL_FILME_PROPOSTO'] = df_search['VL_FILME_PROPOSTO'].astype(float).map(lambda x: '{:.5f}'.format(x).replace('.', ','))

        self.df_search = df_search.copy()

        return self.df_search
    
    def creating_the_master_key(self):
        
        self.df_search['KEY_SHARE_REDE'] = self.df_search.CD_PROTOCOLO.astype(str) + '_' + self.df_search.CD_SERV_HONORARIO.astype(str) + '_' + self.df_search.CD_PROCEDIMENTO_TUSS.astype(str) + '_' + self.df_search.CD_ANO.astype(str) + '_' + self.df_search.DT_STATUS + '_' + self.df_search.NM_PROCEDIMENTO.astype(str) + '_' + self.df_search.NM_PROCEDIMENTO_TUSS.astype(str) + '_' + self.df_search.VL_PROPOSTO.astype(str) + '_' + self.df_search.VL_DEFLATOR.astype(str) + '_' + self.df_search.VL_DEFLATOR_UCO.astype(str) + '_' + self.df_search.VL_FILME_PROPOSTO.astype(str) + '_' + self.df_search.CD_LOCAL.astype(str) + '_' + self.df_search.FL_URGENCIA.astype(str) + '_' + self.df_search.FL_ELETIVA.astype(str)
        
        self.df_search = self.df_search[['KEY_SHARE_REDE','REDE']].copy()

        self.df_search.rename(columns={'CD_TIPO_REDE_ATENDIMENTO' : 'REDE'}, inplace=True)
        self.df_search = self.df_search.sort_values(by=['REDE'])
        self.df_search.reset_index(drop=True, inplace=True)
        
        return self.df_search
    
    def grouping_the_networks(self):
        self.df_search = (
            self.df_search
            .groupby('KEY_SHARE_REDE')
            .agg(
                REDE=('REDE', lambda x: ', '.join(sorted(set(x)))),
                QTD_REDE=('REDE', 'nunique')
            )
            .reset_index()
        )
        self.df_search = self.df_search.sort_values(by=['REDE', 'QTD_REDE'], ascending=True)
        self.df_search.reset_index(drop=True, inplace=True)

        return self.df_search
    
    def breaking_the_primary_key_into_columns(self):

        self.df_search[['CD_PROTOCOLO', 'CD_SERV_HONORARIO', 'CD_PROCEDIMENTO_TUSS', 'CD_ANO','DT_STATUS','NM_PROCEDIMENTO', 'NM_PROCEDIMENTO_TUSS', 'VL_PROPOSTO', 'VL_DEFLATOR', 'VL_DEFLATOR_UCO', 'VL_FILME_PROPOSTO', 'CD_LOCAL', 'FL_URGENCIA', 'FL_ELETIVA']] = self.df_search['KEY_SHARE_REDE'].str.split('_', expand=True)
        self.df_search.drop(columns=['KEY_SHARE_REDE'], inplace=True)
        self.df_search = self.df_search[['CD_PROTOCOLO', 'CD_SERV_HONORARIO', 'CD_PROCEDIMENTO_TUSS', 'CD_ANO', 'DT_STATUS','NM_PROCEDIMENTO', 'NM_PROCEDIMENTO_TUSS', 'VL_PROPOSTO', 'VL_DEFLATOR', 'VL_DEFLATOR_UCO', 'VL_FILME_PROPOSTO', 'CD_LOCAL', 'FL_URGENCIA', 'FL_ELETIVA', 'QTD_REDE','REDE']]
        
        return self.df_search
    
    def rename_columns(self):
        self.df_search.rename(
            columns={
            'CD_PROTOCOLO': 'PROTOCOLO',
            'CD_SERV_HONORARIO': 'CÓDIGO NEGOCIAÇÃO',
            'CD_PROCEDIMENTO_TUSS': 'CÓDIGO TUSS',
            'CD_ANO': 'TABELA',
            'DT_STATUS': 'DT_STATUS',
            'NM_PROCEDIMENTO': 'DESCRIÇÃO',
            'NM_PROCEDIMENTO_TUSS': 'DESCRIÇÃO TUSS',
            'VL_PROPOSTO': 'CH',
            'VL_DEFLATOR': 'PORTE',
            'VL_DEFLATOR_UCO': 'UCO',
            'VL_FILME_PROPOSTO': 'FILME',
            'CD_LOCAL': 'LOCAL',
            'FL_URGENCIA': 'URGÊNCIA',
            'FL_ELETIVA': 'ELETIVO'
        }, 
        inplace=True)

        return self.df_search
    
    def save_to_excel(self, df, file_path):

        try:
            df_tabelas = pd.read_csv(r'./ARQUIVOS/de_para_sigo.csv', sep=';', encoding='latin1', low_memory=False)
            print(f'Quantidade de linhas e colunas df_tabelas: {df_tabelas.shape}')

            df_tabelas['ANO_TABELA'] = df_tabelas['ANO_TABELA'].astype(str)
            df_tabelas.rename(columns={'ANO_TABELA': 'TABELA', 'DESCRICAO':'DESCRIÇÃO TABELA'}, inplace=True)

            df_copy = df.copy()  # Cria uma cópia do DataFrame para evitar problemas de escrita 
            sheet_name = f'GERAL {df_copy.CD_PROTOCOLO.iloc[0]}'
            df_copy = self.rename_columns()  # Renomeia as colunas

            map_dict = dict(zip(df_tabelas['TABELA'], df_tabelas['DESCRIÇÃO TABELA']))
            df_copy['DESCRIÇÃO TABELA'] = df_copy['TABELA'].map(map_dict).fillna('-')
            
            order_columns = ['PROTOCOLO', 'TABELA', 'DESCRIÇÃO TABELA', 'CÓDIGO NEGOCIAÇÃO', 'CÓDIGO TUSS',
                'DESCRIÇÃO', 'DESCRIÇÃO TUSS', 'CH', 'PORTE', 'UCO', 'FILME', 'LOCAL',
                'URGÊNCIA', 'ELETIVO', 'QTD_REDE', 'REDE']
            df_copy = df_copy[order_columns].copy()  # Reordena as colunas
            print(f'df_copy: {df_copy.columns}')
            print(f'Teste 0')
            df_copy.to_excel(file_path, index=False, engine='openpyxl', sheet_name=sheet_name)
            self.label_status_win_one.setText(f"{df.shape[0]} linhas carregadas e salvas no arquivo Excel.")
            
            #print(f'Teste 1')
            df_copy['CÓDIGO TUSS'] = df_copy['CÓDIGO TUSS'].astype(str).replace('0', '-')
            df_copy['DESCRIÇÃO TUSS'] = df_copy['DESCRIÇÃO TUSS'].astype(str).replace('0', '-')
            df_copy['LOCAL'] = df_copy['LOCAL'].fillna('-')
            df_copy['DESCRIÇÃO TUSS'] = df_copy['DESCRIÇÃO TUSS'].astype(str).replace('0', '-')
            df_copy['LOCAL'] = df_copy['LOCAL'].fillna('-')
            df_copy['DESCRIÇÃO TUSS'] = df_copy['DESCRIÇÃO TUSS'].astype(str).replace('.0', '')
            #print(f'Teste 2')
            # criando a chave para separar os arquivos para salvar
            df_copy['KEY_BREAK'] = df_copy['CH'].astype(str) + '_' + df_copy['PORTE'].astype(str) + '_' + df_copy['UCO'].astype(str) + '_' + df_copy['FILME'].astype(str) + '_' + df_copy['LOCAL'].astype(str) + '_' + df_copy['URGÊNCIA'].astype(str) + '_' + df_copy['ELETIVO'].astype(str)
            #print(f'Teste 3')
            print(df_copy.columns)
            order_columns_02 = ['PROTOCOLO', 'TABELA', 'DESCRIÇÃO TABELA', 'CÓDIGO NEGOCIAÇÃO', 'CÓDIGO TUSS',
                'DESCRIÇÃO', 'DESCRIÇÃO TUSS', 'CH', 'PORTE', 'UCO', 'FILME', 'LOCAL',
                'URGÊNCIA', 'ELETIVO', 'QTD_REDE', 'REDE', 'KEY_BREAK']
            
            df_copy = df_copy[order_columns_02].copy()  # Reordena as colunas novamente
            # salvando no mesmo arquivo Excel, mas em abas diferentes por valor unique da chave
            unique_keys = df_copy['KEY_BREAK'].unique()
            neg = f'NEG. '
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
                for num, key in enumerate(unique_keys):
                    df_key = df_copy[df_copy['KEY_BREAK'] == key].copy()
                    df_key.drop(columns=['KEY_BREAK'], inplace=True)  # Remove a coluna de chave
                    df_key.reset_index(drop=True, inplace=True)  # Reseta o índice
                    name_sheet_aba = f'{neg}{num + 1}'
                    df_key.to_excel(writer, index=False, sheet_name=name_sheet_aba)

            self.file_path = file_path  # Armazena o caminho do arquivo
            self.output_path = os.path.dirname(file_path)  # Armazena o diretório do arquivo

            #self.text_edit_info.setText(f"Arquivo salvo com sucesso em:\n{file_path}\n\nTotal de linhas: {df.shape[0]}")
            QMessageBox.information(self.parent, "Sucesso", f"Arquivo salvo em:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self.parent, "Erro", f"Ocorreu um erro ao salvar o arquivo:\n{str(e)}")



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
        self.table.setHorizontalHeaderLabels([
            'CD_PROTOCOLO', 'CD_SERV_HONORARIO', 'CD_PROCEDIMENTO_TUSS', 'CD_ANO',
            'DT_STATUS', 'NM_PROCEDIMENTO', 'NM_PROCEDIMENTO_TUSS', 'REDE',
            'VL_PROPOSTO', 'VL_DEFLATOR', 'VL_DEFLATOR_UCO', 'VL_FILME_PROPOSTO',
            'CD_LOCAL', 'FL_URGENCIA', 'FL_ELETIVA'
        ])
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