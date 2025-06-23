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
        self.df_search = pd.DataFrame()  # DataFrame para armazenar os dados pesquisados
        self.progress_bar_process = None

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
        # pede ao usuário para selecionar a pasta de destino
        folder = QFileDialog.getExistingDirectory(self.parent, "Selecione a pasta de destino")
        if folder:
            if not self.df_search.empty:
                # Define o caminho do arquivo de saída
                #self.output_path = os.path.join(folder, "dados_procedimentos.xlsx")
                protocolo =  self.df_search['CD_PROTOCOLO'].iloc[0]
                print(f"Protocolo pesquisado: {protocolo}")
                ...
                try:
                    # Salva o DataFrame em um arquivo Excel
                    # self.save_to_excel(self.df_search, self.output_path)
                    # QMessageBox.information(self.parent, "Sucesso", f"Dados salvos em: {self.output_path}")
                    self.first_adjustments()
                    self.df_search = self.create_key()
                    self.df_search = self.agroup_by_key()
                    self.df_search = self.sort_values_to_df()
                    self.save_to_excel(folder)
                    ...
                except Exception as erro:
                    QMessageBox.critical(self.parent, "Erro", f"Erro ao salvar os dados: {erro}")
            else:
                QMessageBox.warning(self.parent, "Aviso", "Nenhum dado pesquisado para salvar.")
        
        
    
    # Função para limpar o status
    def clear_status(self):
        self.progress_bar_process.setValue(0)
        self.label_status_win_one.setText("Nenhum arquivo carregado.")
            

    # def save_to_excel(self, file_path):
    #     #import openpyxl
    #     name_protocolo = self.df_search['CD_PROTOCOLO'].iloc[0]
    #     df = self.df_search.copy()
    #     columns_to_show = [
    #         'TABELA', 'DESCRICAO', 'LOCAL_CAPA', 'CD_PROCEDIMENTO', 'CD_PROCEDIMENTO_TUSS',
    #         'NM_PROCEDIMENTO', 'NM_PROCEDIMENTO_TUSS', 'NU_ORDEM_PACOTE', 'CD_TIPO_ACOMODACAO',
    #         'URG_ELE_TAX_MAT_MED_CIR_ANE_AUX', 'VALOR', 'QUANTIDADE_REDES', 'REDES'
    #     ]
    #     # fazendo a barra de progresso crescer de acordo com a quantidade de NU_ORDEM_PACOTE
        
    #     for nu_ordem in df.NU_ORDEM_PACOTE.unique():
    #         # fazendo a barra de progresso crescer de 
    #         df_copy = df[df.NU_ORDEM_PACOTE == nu_ordem].copy()
    #         sheet_file_name = 'PROCEDIMENTO ' + str(name_protocolo) + ' ' + str(nu_ordem) + '.xlsx'
    #         output_file = os.path.join(file_path, sheet_file_name)
    #         df_copy = df_copy[columns_to_show].copy()

    #         # Sempre salva a aba GERAL_{nu_ordem} primeiro
    #         with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    #             aba_geral = f'GERAL {nu_ordem}'[:31]
    #             df_copy.to_excel(writer, sheet_name=aba_geral, index=False)

    #             # Se houver mais de uma negociação, cria abas separadas
    #             if df_copy.URG_ELE_TAX_MAT_MED_CIR_ANE_AUX.nunique() > 1:
    #                 print(f'NU_ORDEM_PACOTE: {nu_ordem} possui mais de uma URG_ELE_TAX_MAT_MED_CIR_ANE_AUX')
    #                 for num, valor in enumerate(df_copy.URG_ELE_TAX_MAT_MED_CIR_ANE_AUX.unique()):
    #                     aba_nome = f'NEGOCIACAO_{num + 1}'[:31]
    #                     df_valor = df_copy[df_copy.URG_ELE_TAX_MAT_MED_CIR_ANE_AUX == valor]
    #                     df_valor.to_excel(writer, sheet_name=aba_nome, index=False)
    #     print(f'Arquivo(s) salvo(s) com sucesso na pasta: {file_path}')

    def save_to_excel(self, file_path):
        name_protocolo = self.df_search['CD_PROTOCOLO'].iloc[0]
        df = self.df_search.copy()
        columns_to_show = [
            'TABELA', 'DESCRICAO', 'LOCAL_CAPA', 'CD_PROCEDIMENTO', 'CD_PROCEDIMENTO_TUSS',
            'NM_PROCEDIMENTO', 'NM_PROCEDIMENTO_TUSS', 'NU_ORDEM_PACOTE', 'CD_TIPO_ACOMODACAO',
            'URG_ELE_TAX_MAT_MED_CIR_ANE_AUX', 'VALOR', 'QUANTIDADE_REDES', 'REDES'
        ]
        nu_ordens = df.NU_ORDEM_PACOTE.unique()
        total = len(nu_ordens)
        self.progress_bar_process.setValue(0)
        for idx, nu_ordem in enumerate(nu_ordens, 1):
            df_copy = df[df.NU_ORDEM_PACOTE == nu_ordem].copy()
            sheet_file_name = 'PROCEDIMENTO ' + str(name_protocolo) + ' ' + str(nu_ordem) + '.xlsx'
            output_file = os.path.join(file_path, sheet_file_name)
            df_copy = df_copy[columns_to_show].copy()

            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                aba_geral = f'GERAL {nu_ordem}'[:31]
                df_copy.to_excel(writer, sheet_name=aba_geral, index=False)

                if df_copy.URG_ELE_TAX_MAT_MED_CIR_ANE_AUX.nunique() > 1:
                    print(f'NU_ORDEM_PACOTE: {nu_ordem} possui mais de uma URG_ELE_TAX_MAT_MED_CIR_ANE_AUX')
                    for num, valor in enumerate(df_copy.URG_ELE_TAX_MAT_MED_CIR_ANE_AUX.unique()):
                        aba_nome = f'NEGOCIACAO_{num + 1}'[:31]
                        df_valor = df_copy[df_copy.URG_ELE_TAX_MAT_MED_CIR_ANE_AUX == valor]
                        df_valor.to_excel(writer, sheet_name=aba_nome, index=False)
            # Atualiza a barra de progresso
            progresso = int((idx / total) * 100)
            self.progress_bar_process.setValue(progresso)
        print(f'Arquivo(s) salvo(s) com sucesso na pasta: {file_path}')
        self.progress_bar_process.setValue(100)

    
    def first_adjustments(self):
        path_df_sigo = r'./ARQUIVOS/de_para_sigo.csv'

        df_sigo = pd.read_csv(path_df_sigo, sep=';', encoding='latin1', low_memory=False)
        df_sigo['ANO_TABELA'] = df_sigo['ANO_TABELA'].astype(str).str.replace('.0', '').str.zfill(8)

        print(f'Quantidade de linhas e colunas: {self.df_search.shape}')
        self.df_search['TABELA'] = self.df_search['TABELA'].astype(str).str.replace('.0', '').str.zfill(8)
        self.df_search['NM_PROCEDIMENTO'] = self.df_search['NM_PROCEDIMENTO'].astype(str).str.replace(';', ',')
        self.df_search['NM_PROCEDIMENTO_TUSS'] = self.df_search['NM_PROCEDIMENTO_TUSS'].astype(str).str.replace(';', ', ')

        # Criando um dicionário de mapeamento a partir de df_sigo
        map_dict = dict(zip(df_sigo['ANO_TABELA'], df_sigo['DESCRICAO']))
        # Substituindo os valores em df_ppp['TABELA'] com base no dicionário
        self.df_search['DESCRICAO'] = self.df_search['TABELA'].map(map_dict).fillna(self.df_search['TABELA'])
        # Mostrando as primeiras linhas para verificar
        print(self.df_search['DESCRICAO'].value_counts())
        # filtrando as colunas e ordenando
        # print(self.df_search.columns)
        colum_filter_ordeby = ['CD_PROTOCOLO', 'TABELA', 'DESCRICAO', 'LOCAL_CAPA', 'CD_PROCEDIMENTO', 'CD_PROCEDIMENTO_TUSS',
            'NM_PROCEDIMENTO', 'NM_PROCEDIMENTO_TUSS', 'NU_ORDEM_PACOTE',
            'CD_TIPO_ACOMODACAO', 'URG_ELE_TAX_MAT_MED_CIR_ANE_AUX', 'VALOR',
            'CD_TIPO_REDE_ATENDIMENTO',]
        #print(self.df_search.columns)
        self.df_search = self.df_search[colum_filter_ordeby].copy()
        print(f'Quantidade de linhas e colunas após os ajustes: {self.df_search.shape}')
        print(self.df_search.head())  # Exibe as primeiras linhas do DataFrame ajustado

    def create_key(self):
        # Copiando o DataFrame para evitar alterações no original
        df_copy = self.df_search.copy()
        # Criando uma chave única
        df_copy['CHAVE'] = (
            df_copy.CD_PROTOCOLO.astype(str) + '@' +
            df_copy.TABELA.astype(str) + '@' +
            df_copy.DESCRICAO.astype(str) + '@' +
            df_copy.LOCAL_CAPA.astype(str) + '@' +
            df_copy.CD_PROCEDIMENTO.astype(str) + '@' +
            df_copy.CD_PROCEDIMENTO_TUSS.astype(str) + '@' +
            df_copy.NM_PROCEDIMENTO.astype(str) + '@' +
            df_copy.NM_PROCEDIMENTO_TUSS.astype(str) + '@' +
            df_copy.NU_ORDEM_PACOTE.astype(str) + '@' +
            df_copy.CD_TIPO_ACOMODACAO.astype(str) + '@' +
            df_copy.URG_ELE_TAX_MAT_MED_CIR_ANE_AUX.astype(str) + '@' +
            df_copy.VALOR.astype(str)
        )
        # Mostrando as colunas do DataFrame
        print(f'Colunas do DataFrame: \n {df_copy.columns}')
        # Mostrando as primeiras linhas do DataFrame copiado
        print(f'Quantidade de linhas e colunas do DataFrame copiado: {df_copy.shape}')
        # Filtrando somente as colunas que desejamos
        columns_to_show = ['CHAVE', 'CD_TIPO_REDE_ATENDIMENTO']
        df_copy = df_copy[columns_to_show].copy()
        df_copy.drop_duplicates(inplace=True)
        df_copy.reset_index(drop=True, inplace=True)
        #ordenando por CD_TIPO_REDE_ATENDIMENTO
        df_copy.sort_values(by=['CD_TIPO_REDE_ATENDIMENTO'], inplace=True)

        df_copy['CD_TIPO_REDE_ATENDIMENTO'] = df_copy['CD_TIPO_REDE_ATENDIMENTO'].astype(str).str.replace('.0', '')

        print(df_copy.head(3))  # Exibe as primeiras linhas do DataFrame copiado

        return df_copy
        ...

    def agroup_by_key(self):
        df_copy = self.df_search.copy()
        # horizontalizando os valores de CD_TIPO_REDE_ATENDIMENTO
        # Agrupando e criando as colunas horizontalizadas e de quantidade
        df_copy = (
            df_copy.groupby('CHAVE')['CD_TIPO_REDE_ATENDIMENTO']
            .agg([
                ('CD_TIPO_REDE_ATENDIMENTO', lambda x: ', '.join(sorted(set(x)))),
                ('QUANTIDADE_REDES', 'nunique')
            ])
            .reset_index()
        )
        # coçunas selecionas
        columns_to_show = ['CHAVE', 'QUANTIDADE_REDES', 'CD_TIPO_REDE_ATENDIMENTO']
        df_copy = df_copy[columns_to_show].copy()
        df_copy.drop_duplicates(inplace=True)
        df_copy.reset_index(drop=True, inplace=True)
        # Separando as colunas novamente agora
        df_copy[['CD_PROTOCOLO', 'TABELA', 'DESCRICAO', 'LOCAL_CAPA', 'CD_PROCEDIMENTO',
            'CD_PROCEDIMENTO_TUSS', 'NM_PROCEDIMENTO', 'NM_PROCEDIMENTO_TUSS',
            'NU_ORDEM_PACOTE', 'CD_TIPO_ACOMODACAO',
            'URG_ELE_TAX_MAT_MED_CIR_ANE_AUX', 'VALOR',]] = df_copy['CHAVE'].str.split('@', expand=True)
        # ordenando as colunas
        colum_filter_ordeby = ['CD_PROTOCOLO','TABELA', 'DESCRICAO', 'LOCAL_CAPA', 'CD_PROCEDIMENTO',
            'CD_PROCEDIMENTO_TUSS', 'NM_PROCEDIMENTO', 'NM_PROCEDIMENTO_TUSS',
            'NU_ORDEM_PACOTE', 'CD_TIPO_ACOMODACAO',
            'URG_ELE_TAX_MAT_MED_CIR_ANE_AUX', 'VALOR', 'QUANTIDADE_REDES',
            'CD_TIPO_REDE_ATENDIMENTO',]
        df_copy = df_copy[colum_filter_ordeby].copy()

        print(df_copy.head(3))  # Exibe as primeiras linhas do DataFrame copiado

        return df_copy
    
    def sort_values_to_df(self):
        df_copy = self.df_search.copy()
        # renomeando as colunas
        df_copy.rename(columns={'CD_TIPO_REDE_ATENDIMENTO': 'REDES', }, inplace=True)

        df_copy.sort_values(by=['NU_ORDEM_PACOTE', 'VALOR', 'QUANTIDADE_REDES'], inplace=True)
        df_copy.reset_index(drop=True, inplace=True)
        # covertendo a colunas de valores inteiros
        df_copy['TABELA'] = df_copy['TABELA'].astype(int)
        print(f'TABELA: OK')
        df_copy['LOCAL_CAPA'] = df_copy['LOCAL_CAPA'].astype(int)
        print(f'LOCAL_CAPA: OK')
        df_copy['CD_PROCEDIMENTO'] = df_copy['CD_PROCEDIMENTO'].astype(int)
        print(f'CD_PROCEDIMENTO: OK')
        df_copy['CD_PROCEDIMENTO_TUSS'] = df_copy['CD_PROCEDIMENTO_TUSS'].astype(int)
        print(f'CD_PROCEDIMENTO_TUSS: OK')
        df_copy['NU_ORDEM_PACOTE'] = df_copy['NU_ORDEM_PACOTE'].astype(int)
        print(f'NU_ORDEM_PACOTE: OK')
        df_copy['CD_TIPO_ACOMODACAO'] = df_copy['CD_TIPO_ACOMODACAO'].astype(int)
        print(f'CD_TIPO_ACOMODACAO: OK')

        print(f'Quantidade de linhas e colunas do DataFrame copiado removendo as duplicadas: {df_copy.shape}')
        print(df_copy.columns)  # Exibe as colunas do DataFrame copiado
        print(df_copy.head(3))  # Exibe as primeiras linhas do DataFrame copiado
        
        return df_copy


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
            ['CD_PROTOCOLO','TABELA', 'LOCAL_CAPA', 'CD_PROCEDIMENTO', 'CD_PROCEDIMENTO_TUSS',
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
                QMessageBox.warning(self, 'Aviso', f'Protocolo(s): ( {search_term} ) inelegível para automatização de documentos. \n\nSolicita-se verificação com a coordenação.')
                #QMessageBox.critical(self, "Erro", f"Erro ao buscar dados:\n{str(erro)}")
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