import pandas as pd
import numpy as np
from pandas import ExcelWriter
import os
class ProcedurePackageProcess:
    def __init__(self, parent=None):
        self.parent = parent
        self.file_path = None
        self.model_path = "./ARQUIVOS/modelo_cod_renomeacao.csv"
        self.sigo_path = "./ARQUIVOS/de_para_sigo.csv"
        self.output_path = None
        self.df = pd.DataFrame()
        self.df_cod = pd.DataFrame()
        self.df_sigo = pd.DataFrame()
        self.df_filtered = pd.DataFrame()
        self.df_key = pd.DataFrame()
        self.df_key_grouped = pd.DataFrame()
        self.df_final = pd.DataFrame()


    # 1. Função para ler o arquivo principal e os arquivos auxiliares
    def load_data(self):
        # 1.2 - Lendo o arquivo principal 
        print(f'ETAPA - 1. Função para ler o arquivo principal e os arquivos auxiliares')
        print(f'ETAPA - 1.2 - Lendo o arquivo principal')
        self.df = pd.read_csv(self.file_path, sep=';', encoding='latin1', low_memory=False)
        print(f'Colunas de self.df : {self.df.columns}')
        print(f'Quantidade de linhas e colunas self.df: {self.df.shape}')
        
        # Ajustando colunas
        self.df['CD_SERVIÇO_HONORARIO'] = self.df['CD_SERVIÇO_HONORARIO'].astype(str).str.replace('.0', '').str.zfill(8)
        self.df['CD_PROCEDIMENTO_TUSS'] = self.df['CD_PROCEDIMENTO_TUSS'].astype(str).str.replace('.0', '')
        self.df['CD_TIPO_ACOMODACAO'] = self.df['CD_TIPO_ACOMODACAO'].astype(str).str.replace('.0', '')
        print(f'ETAPA - 1.2 - Concluida')
        # 1.3 - Lendo o arquivo df_cod
        print(f'ETAPA - 1.3 - Lendo o arquivo df_cod')
        self.df_cod = pd.read_csv(self.model_path, sep=';', encoding='latin1', low_memory=False)
        self.df_cod.rename(columns={'COD_RENOMEACAO': 'CD_SERVIÇO_HONORARIO'}, inplace=True)
        self.df_cod['CD_SERVIÇO_HONORARIO'] = self.df_cod['CD_SERVIÇO_HONORARIO'].astype(str).str.replace('.0', '').str.zfill(8)
        print(f'Colunas de self.df_cod : {self.df_cod.columns}')
        print(f'Quantidade de linhas e colunas self.df_cod: {self.df_cod.shape}')
        print(f'ETAPA - 1.3 - Concluida')
        # Lendo o arquivo SIGO
        print(f'ETAPA - 1.4 - Lendo o arquivo SIGO')
        self.df_sigo = pd.read_csv(self.sigo_path, sep=';', encoding='latin1', low_memory=False)
        self.df_sigo['ANO_TABELA'] = self.df_sigo['ANO_TABELA'].astype(str).str.replace('.0', '').str.zfill(8)
        print(f'Colunas de self.df_sigo : {self.df_sigo.columns}')
        print(f'Quantidade de linhas e colunas self.df_sigo: {self.df_sigo.shape}')
        print(f'ETAPA - 1.4 - Concluida')

        # executando a função 2
        self.process_data_one()
        self.df = self.df_key_grouped.copy()

        return self.df

    # 2. - Processando as colunas do arquivo principal
    def process_data_one(self):
        # 2.1 - Selecionando as (12) colunas que usaremos.
        print(f'Etapa - 2 - Processando as colunas do arquivo principal')
        print(f'Etapa - 2.1 - Selecionando as (12) colunas que usaremos')
        columns_selects = [
            'ANO_TABELA', 'CD_SERVIÇO_HONORARIO', 'CD_PROCEDIMENTO_TUSS', 'NM_SERV_HONORARIO', 'NM_PROCEDIMENTO_TUSS',
            'VALOR_PROPOSTO', 'CD_TIPO_ACOMODACAO', 'URGENCIA', 'ELETIVA', 'TAXAS', 'MATERIAL', 'MEDICAMENTO',
            'CONSULTA_HONORARIO', 'ANESTESISTA', 'AUXILIAR', 'CD_TIPO_REDE'
        ]
        self.df_filtered = self.df[columns_selects].copy()
        self.df_filtered['ANO_TABELA'] = self.df_filtered['ANO_TABELA'].astype(str).str.replace('.0', '').str.zfill(8)
        print(f'ETAPA - 2.1 - Concluida')

        # 2.2 - Criamos um dicionário para mapear as chaves de busca e trazer os valores do item *`1.4`*.
        print(f'Etapa - 2.2 - Criamos um dicionário para mapear as chaves de busca e trazer os valores do item *`1.4`*.')
        map_dict = dict(zip(self.df_sigo['ANO_TABELA'], self.df_sigo['DESCRICAO']))
        print(f'Etapa - 2.2 - Concluida')
        # 2.3 - Criamos um dicionário para mapear as chaves de busca e trazer os valores do item *`1.4`*.
        print(f'Eatapa - 2.3 - Criamos um dicionário para mapear as chaves de busca e trazer os valores do item *`1.4`*.')
        self.df_filtered['ANO_TABELA'] = (
            self.df_filtered['ANO_TABELA']
            .map(map_dict)
            .fillna(self.df_filtered['ANO_TABELA'])
            .infer_objects(copy=False)  # Ajusta os tipos de dados explicitamente
        )
        print(f'ETAPA - 2.3 - Concluída')

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
        print(f'ETAPA - 2.4 - Concluída')

        # chamando a função 3
        self.create_colum_key()
        self.process_data_juridic()
    
    # 3. - Criando a coluna CHAVE_1
    def create_colum_key(self):
        print(f'ETAPA - 3 - Criando a coluna CHAVE_1')
        print(f'ETAPA - 3.1 - Criando a coluna CHAVE_1')
        # Criando a coluna CHAVE_1 concatenando as colunas especificadas
        columns = 'URG_ELE_TAX_MAT_MED_CH_ANE_AUX'
        self.df_filtered['CHAVE_1'] = (
            self.df_filtered['URGENCIA'].astype(str) + ' ' + 
            self.df_filtered['ELETIVA'].astype(str) + ' ' + 
            self.df_filtered['TAXAS'].astype(str) + ' ' + 
            self.df_filtered['MATERIAL'].astype(str) + ' ' + 
            self.df_filtered['MEDICAMENTO'].astype(str) + ' ' + 
            self.df_filtered['CONSULTA_HONORARIO'].astype(str) + ' ' + 
            self.df_filtered['ANESTESISTA'].astype(str) + ' ' + 
            self.df_filtered['AUXILIAR'].astype(str)
            )
        self.df_filtered.rename(columns={'CHAVE_1': columns}, inplace=True)
        print(self.df_filtered.head(2))
        print(f'ETAPA - 3.1 - Concluída')
    
    # 4. Processando as regras do jurídico para utilizar o arquivo.
    def process_data_juridic(self):
        print(f'ETAPA - 4 - Processando as regras do jurídico para utilizar o arquivo.')
        print(f'ETAPA - 4.1 - Selecionando as colunas que serão utilizadas.')
        self.df_key = self.df_filtered[
            ['ANO_TABELA','CD_SERVIÇO_HONORARIO','VALOR_PROPOSTO',
            'URG_ELE_TAX_MAT_MED_CH_ANE_AUX','CD_TIPO_REDE', 'NOMENCLATURA', 
            'CD_TIPO_ACOMODACAO', 'CD_PROCEDIMENTO_TUSS']
        ].copy()
        print(f'ETAPA - 4.1 Concluído')

        print(f'ETAPA - 4.2 Concatenando as informações que precisamos em uma única coluna.')
        self.df_key['CHAVE_3_AUX'] = (
            self.df_key['CD_SERVIÇO_HONORARIO'].astype(str) + '#' +
            self.df_key['VALOR_PROPOSTO'].astype(str) + '#' +
            self.df_key['URG_ELE_TAX_MAT_MED_CH_ANE_AUX'].astype(str) + '#' +
            self.df_key['NOMENCLATURA'].astype(str) + '#' +
            self.df_key['CD_TIPO_ACOMODACAO'].astype(str) + '#' +
            self.df_key['CD_PROCEDIMENTO_TUSS'].astype(str) + '#' +
            self.df_key['ANO_TABELA'].astype(str)
        )
        print(f'ETAPA - 4.2 Concluído')

        print(f'ETAPA - 4.3 Removendo inconsistências da coluna e transformando em tipo String.')
        self.df_key['CD_TIPO_REDE'] = self.df_key['CD_TIPO_REDE'].astype(str).str.replace('.0', '')
        print(f'ETAPA - 4.3 Concluído')

        print(f'ETAPA - 4.4 Ordenando `CD_TIPO_REDE`.')
        self.df_key.sort_values(by=['CD_TIPO_REDE'], inplace=True)
        print(f'ETAPA - 4.4 Concluído')

        print(f'ETAPA - 4.5 Removendo as duplicadas e resetando o index da nova tabela.')
        self.df_key.drop_duplicates(inplace=True)
        self.df_key.reset_index(drop=True, inplace=True)
        print(f'ETAPA - 4.5 Concluído')

        print(f'ETAPA - 4.6 Agrupando por CD_SERVIÇO_HONORARIO e concatenando os valores de `CD_TIPO_REDE` por "#".')
        self.df_key_grouped = (
            self.df_key.groupby('CHAVE_3_AUX')['CD_TIPO_REDE']
            .apply(', '.join)
            .reset_index()
        )
        self.df_key_grouped['QUANTIDADE_REDES'] = (
            self.df_key.groupby('CHAVE_3_AUX')['CD_TIPO_REDE']
            .size()
            .values
        )
        print(f'ETAPA - 4.6 Concluído')

        print(f'ETAPA - 4.7 Renomeando as colunas para manter o formato desejado.')
        self.df_key_grouped.columns = ['CD_SERVIÇO_HONORARIO', 'CD_TIPO_REDE', 'QUANTIDADE_REDES']
        print(f'ETAPA - 4.7 Concluído')

        print(f'ETAPA - 4.8 Quebrando a coluna CHAVE em 3 colunas separadas por "#".')
        self.df_key_grouped[
            ['CD_SERVIÇO_HONORARIO', 'VALOR_PROPOSTO', 
             'URG_ELE_TAX_MAT_MED_CH_ANE_AUX', 'NOMENCLATURA', 
             'CD_TIPO_ACOMODACAO', 'CD_PROCEDIMENTO_TUSS',
               'ANO_TABELA']
            ] = self.df_key_grouped['CD_SERVIÇO_HONORARIO'].str.split('#', expand=True)
        
        self.df_key_grouped = self.df_key_grouped[
            ['ANO_TABELA','CD_SERVIÇO_HONORARIO',
             'CD_PROCEDIMENTO_TUSS' ,'NOMENCLATURA',
             'VALOR_PROPOSTO', 'CD_TIPO_ACOMODACAO', 
             'URG_ELE_TAX_MAT_MED_CH_ANE_AUX', 'QUANTIDADE_REDES', 
             'CD_TIPO_REDE']
        ].copy()
        print(f'ETAPA - 4.8 Concluído')

        print(f'ETAPA - 4.9 Ordenando a o df: "URG_ELE_TAX_MAT_MED_CH_ANE_AUX", "VALOR_PROPOSTO" e "QUANTIDADE_REDES".')
        self.df_key_grouped.sort_values(
            by=['URG_ELE_TAX_MAT_MED_CH_ANE_AUX', 'VALOR_PROPOSTO', 'QUANTIDADE_REDES'],
            inplace=True
        )
        self.df_key_grouped.reset_index(drop=True, inplace=True)
        self.df_key_grouped['CD_SERVIÇO_HONORARIO'] = self.df_key_grouped['CD_SERVIÇO_HONORARIO'].astype(str)

        self.df_key_grouped['VALOR_PROPOSTO'] = 'R$ ' + self.df_key_grouped['VALOR_PROPOSTO'].astype(str)
        print(f'Quantidade de linhas e colunas de self.df_key_grouped: {self.df_key_grouped.shape}')
        print(self.df_key_grouped.ANO_TABELA.value_counts())
        print(self.df_key_grouped.head(2))
        print(f'ETAPA - 4.9 Concluído')

    def save_to_excel(self):
        # Salvando os dados processados em um arquivo Excel
        with ExcelWriter(self.output_path, engine='openpyxl') as writer:
            self.df_filtered.to_excel(writer, index=False, sheet_name='GERAL')
        print(f"Arquivo salvo em: {self.output_path}")
