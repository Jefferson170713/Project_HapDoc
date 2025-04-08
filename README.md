# Projeto - *__HapDoc__* para automatizar processos e documentos.

### *__Pacote e Procedimentos__*
    - 1 - Leitura do arquivo extraído do sistema.
        - 1.2 Começamos com algumas tratativas nas colunas necessárias que precisamos.
            - Correção de 3 colunas com valores inteiros, removendo __'.0'__ inconsistência.
            - Selecionando somente as colunas necessárias(14) ao invés de 31 colunas.
        - 1.3 - Leitura do arquivo `De Para` para Auxiliar a confecção do arquivo principal.
            - Correção de 1 coluna com valore inteiro, removendo __'.0'__ inconsistência.
            - Formando um dicionário para criar um mecanismo de chave de busca.
            - Usar a nova coluna chave para auxiliar no material principal.
        - 1.4 - Leitura do arquivo para Auxiliar na descrição dos proceddimentos.
            - Quando o código deste arquivo for encontrado no arquivo principal, seguirá certas regras específicas.
            - Poderá trazer o nome do procedimento ou o nome do serviço de acordo com cada linha.