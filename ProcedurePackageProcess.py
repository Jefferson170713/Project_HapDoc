import pandas as pd
import numpy as np
from pandas import ExcelWriter
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

class ProcedurePackageProcess:
    def __init__(self, parent=None):
        self.parent = parent
        self.file_path = None
        self.model_path = "./modelo_cod_renomeacao.csv"
        self.sigo_path = "./ARQUIVOS/de_para_sigo.csv"
        self.output_path = None


    # 1. Função para ler o arquivo principal e os arquivos auxiliares
    def load_data(self):
        # 1.2 - Lendo o arquivo principal 
        print(f'Estapa - 1. Função para ler o arquivo principal e os arquivos auxiliares')
        print(f'Estapa - 1.2 - Lendo o arquivo principal')
        self.df = pd.read_csv(self.file_path, sep=';', encoding='latin1', low_memory=False)
        print(f'Colunas de self.df : {self.df.columns}')
        print(f'Quantidade de linhas e colunas self.df: {self.df.shape}')
        
        # Ajustando colunas
        self.df['CD_SERVIÇO_HONORARIO'] = self.df['CD_SERVIÇO_HONORARIO'].astype(str).str.replace('.0', '').str.zfill(8)
        self.df['CD_PROCEDIMENTO_TUSS'] = self.df['CD_PROCEDIMENTO_TUSS'].astype(str).str.replace('.0', '')
        self.df['CD_TIPO_ACOMODACAO'] = self.df['CD_TIPO_ACOMODACAO'].astype(str).str.replace('.0', '')
        print(f'Etapa - 1.2 - Concluida')
        # 1.3 - Lendo o arquivo df_cod
        print(f'ETAPA - 1.3 - Lendo o arquivo df_cod')
        self.df_cod = pd.read_csv(self.model_path, sep=';', encoding='latin1', low_memory=False)
        self.df_cod.rename(columns={'COD_RENOMEACAO': 'CD_SERVIÇO_HONORARIO'}, inplace=True)
        self.df_cod['CD_SERVIÇO_HONORARIO'] = self.df_cod['CD_SERVIÇO_HONORARIO'].astype(str).str.replace('.0', '').str.zfill(8)
        print(f'Colunas de self.df_cod : {self.df_cod.columns}')
        print(f'Quantidade de linhas e colunas self.df_cod: {self.df_cod.shape}')
        print(f'Estapa - 1.3 - Concluida')
        # Lendo o arquivo SIGO
        print(f'Estapa - 1.4 - Lendo o arquivo SIGO')
        self.df_sigo = pd.read_csv(self.sigo_path, sep=';', encoding='latin1', low_memory=False)
        self.df_sigo['ANO_TABELA'] = self.df_sigo['ANO_TABELA'].astype(str).str.replace('.0', '').str.zfill(8)
        print(f'Colunas de self.df_sigo : {self.df_sigo.columns}')
        print(f'Quantidade de linhas e colunas self.df_sigo: {self.df_sigo.shape}')
        print(f'Estapa - 1.4 - Concluida')

    # 2. - Processando as colunas do arquivo principal
    def process_data(self):
        # 2.1 - Selecionando as (12) colunas que usaremos.
        print(f'Etapa - 2 - Processando as colunas do arquivo principal')
        print(f'Etapa - 2.1 - Selecionando as (12) colunas que usaremos')
        columns_selects = [
            'ANO_TABELA', 'CD_SERVIÇO_HONORARIO', 'CD_PROCEDIMENTO_TUSS', 'NM_SERV_HONORARIO', 'NM_PROCEDIMENTO_TUSS',
            'VALOR_PROPOSTO', 'CD_TIPO_ACOMODACAO', 'URGENCIA', 'ELETIVA', 'TAXAS', 'MATERIAL',
            'CONSULTA_HONORARIO', 'ANESTESISTA', 'AUXILIAR', 'CD_TIPO_REDE'
        ]
        self.df_filtered = self.df[columns_selects].copy()
        print(f'Estapa - 2.1 - Concluida')

        # 2.2 - Criamos um dicionário para mapear as chaves de busca e trazer os valores do item *`1.4`*.
        print(f'Etapa - 2.2 - Criamos um dicionário para mapear as chaves de busca e trazer os valores do item *`1.4`*.')
        map_dict = dict(zip(self.df_sigo['ANO_TABELA'], self.df_sigo['DESCRICAO']))
        print(f'Etapa - 2.2 - Concluida')
        # 2.3 - Criamos um dicionário para mapear as chaves de busca e trazer os valores do item *`1.4`*.
        print(f'Eatapa - 2.3 - Criamos um dicionário para mapear as chaves de busca e trazer os valores do item *`1.4`*.')
        self.df_filtered['ANO_TABELA'] = self.df_filtered['ANO_TABELA'].map(map_dict).fillna(self.df_filtered['ANO_TABELA'])

        print(f'Eatapa - 2.4 - Substituindo os valores em df com base no dicionário.')
        self.df_filtered['NOMENCLATURA'] = np.where(
            self.df_filtered['CD_SERVIÇO_HONORARIO'].isin(self.df_cod['CD_SERVIÇO_HONORARIO']),
            self.df_filtered['NM_PROCEDIMENTO_TUSS'],
            self.df_filtered['NM_SERV_HONORARIO']
        )
        # Removendo duplicatas
        self.df_filtered.drop_duplicates(inplace=True)
        self.df_filtered.reset_index(drop=True, inplace=True)
        print(f'Quantidade de linhas e Colunas de self.df_filtered : {self.df_filtered.shape}')
        print(f'Colunas de self.df_filtered: {self.df_filtered.columns}')
        print(f'Estapa - 2.4 - Concluída')

    def save_to_excel(self):
        # Salvando os dados processados em um arquivo Excel
        with ExcelWriter(self.output_path, engine='openpyxl') as writer:
            self.df_filtered.to_excel(writer, index=False, sheet_name='GERAL')
        print(f"Arquivo salvo em: {self.output_path}")

    # Criar a aba de "Pacote Procedimento"
    def creat_procedures_and_package_tab(self, procedures_package):
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