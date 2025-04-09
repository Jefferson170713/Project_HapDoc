# Projeto - *__HapDoc__* para automatizar processos e documentos.

### *__Pacote e Procedimentos__*
- 1 - Leitura do arquivo extraído do sistema.
    - 1.2 Começamos com algumas tratativas nas colunas necessárias que precisamos.
        - Correção de 3 colunas com valores inteiros, removendo __'.0'__ inconsistência.
        - Selecionando somente as colunas necessárias(14) ao invés de 31 colunas.
    - 1.3 - Leitura do arquivo para Auxiliar na descrição dos procedimentos.
        - Quando o código deste arquivo for encontrado no arquivo principal, seguirá certas regras específicas.
        - Poderá trazer o nome do procedimento ou o nome do serviço de acordo com cada linha.
    - 1.4 - Leitura do arquivo `De Para` para Auxiliar a confecção do arquivo principal.
        - Correção de 1 coluna com valore inteiro, removendo __'.0'__ inconsistência.
        - Formando um dicionário para criar um mecanismo de chave de busca.
        - Usar a nova coluna chave para auxiliar no material principal.

- 2 - Processando as colunas do arquivo principal
    - 2.1 - Selecionando as (12) colunas que usaremos.
    - 2.2 - Criamos um dicionário para mapear as chaves de busca e trazer os valores do item *`1.4`*.
    - 2.3 - Substituindo os valores em df com base no dicionário.
    - 2.4 - filtrar o que precisamos.

- 3 - Criando a Coluna *__CHAVE__*.
    - 3.1 União e combinações possíveis para as seguintes colunas:
      - `URGENCIA`, `ELETIVA`, `TAXAS`, `MATERIAL`, `CONSULTA_HONORARIO`, `ANESTESISTA`, `AUXILIAR`.

- 4 - Processando as regras do jurídico para utilizar o arquivo.
    - 4.1 - Selecionando as colunas que serão utilizadas.
    - 4.2 - Concatenando as informações que precisamos em uma única coluna.
    - 4.3 - Removendo inconsistências da coluna e transformando em tipo String.
    - 4.4 - Ordenando `CD_TIPO_REDE`.
    - 4.5 - Removendo as duplicadas e resetando o index da nova tabela.
    - 4.6 - Agrupando por CD_SERVIÇO_HONORARIO e concatenando os valores de `CD_TIPO_REDE` por '#".
        - Adicionando uma coluna com a quantidade de redes.
    - 4.7 - Renomeando as colunas para manter o formato desejado.
    - 4.8 - Quebrando a coluna CHAVE em 3 colunas separadas por '#'.
        - Reordenando as colunas desejadas.
    - 4.9 - Ordenando a o df por:
        -   ´URG_ELE_TAX_MAT_CH_ANE_AUX´.
        -   ´VALOR_PROPOSTO´.
        -   ´QUANTIDADE_REDES´.

---