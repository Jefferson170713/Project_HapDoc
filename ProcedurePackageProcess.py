import pandas as pd
import numpy as np
from pandas import ExcelWriter

class ProcedurePackageProcess:
    def __init__(self, file_path, model_path, sigo_path, output_path):
        self.file_path = file_path
        self.model_path = model_path
        self.sigo_path = sigo_path
        self.output_path = output_path

    def load_data(self):
        # Lendo o arquivo principal
        self.df = pd.read_csv(self.file_path, sep=';', encoding='latin1', low_memory=False)
        print(f'Quantidade de linhas e colunas: {self.df.shape}')

        # Ajustando colunas
        self.df['CD_SERVIÇO_HONORARIO'] = self.df['CD_SERVIÇO_HONORARIO'].astype(str).str.replace('.0', '').str.zfill(8)
        self.df['CD_PROCEDIMENTO_TUSS'] = self.df['CD_PROCEDIMENTO_TUSS'].astype(str).str.replace('.0', '')
        self.df['CD_TIPO_ACOMODACAO'] = self.df['CD_TIPO_ACOMODACAO'].astype(str).str.replace('.0', '')

        # Lendo o arquivo modelo
        self.df_cod = pd.read_csv(self.model_path, sep=';', encoding='latin1', low_memory=False)
        self.df_cod.rename(columns={'COD_RENOMEACAO': 'CD_SERVIÇO_HONORARIO'}, inplace=True)
        self.df_cod['CD_SERVIÇO_HONORARIO'] = self.df_cod['CD_SERVIÇO_HONORARIO'].astype(str).str.replace('.0', '').str.zfill(8)

        # Lendo o arquivo SIGO
        self.df_sigo = pd.read_csv(self.sigo_path, sep=';', encoding='latin1', low_memory=False)

    def process_data(self):
        # Filtrando colunas necessárias
        columns_selects = [
            'ANO_TABELA', 'CD_SERVIÇO_HONORARIO', 'CD_PROCEDIMENTO_TUSS', 'NM_SERV_HONORARIO', 'NM_PROCEDIMENTO_TUSS',
            'VALOR_PROPOSTO', 'CD_TIPO_ACOMODACAO', 'URGENCIA', 'ELETIVA', 'TAXAS', 'MATERIAL',
            'CONSULTA_HONORARIO', 'ANESTESISTA', 'AUXILIAR', 'CD_TIPO_REDE'
        ]
        self.df_filtered = self.df[columns_selects].copy()

        # Mapeando valores do SIGO
        map_dict = dict(zip(self.df_sigo['ANO_TABELA'], self.df_sigo['DESCRICAO']))
        self.df_filtered['ANO_TABELA'] = self.df_filtered['ANO_TABELA'].map(map_dict).fillna(self.df_filtered['ANO_TABELA'])

        # Criando a coluna NOMENCLATURA
        self.df_filtered['NOMENCLATURA'] = np.where(
            self.df_filtered['CD_SERVIÇO_HONORARIO'].isin(self.df_cod['CD_SERVIÇO_HONORARIO']),
            self.df_filtered['NM_PROCEDIMENTO_TUSS'],
            self.df_filtered['NM_SERV_HONORARIO']
        )

        # Removendo duplicatas
        self.df_filtered.drop_duplicates(inplace=True)
        self.df_filtered.reset_index(drop=True, inplace=True)

    def save_to_excel(self):
        # Salvando os dados processados em um arquivo Excel
        with ExcelWriter(self.output_path, engine='openpyxl') as writer:
            self.df_filtered.to_excel(writer, index=False, sheet_name='GERAL')
        print(f"Arquivo salvo em: {self.output_path}")