# Projeto Despesas 

Este é um sistema de **Web Scraping** desenvolvido em python para automatizar a coleta, processamento e visualização de dados de despesas (Demonstraçõs Contabeis/DC).
O projeto navega pela API Publica disponibilizada no Desafio.
## URL -> ("https://dadosabertos.ans.gov.br/FTP/PDA/").

**OBS**: por conta do tempo, não consegui finalizar o projeto por completo, e nem documenta-lo 100%, apenas registrei as etapas e processos mais importantes para o ciclo ser iniciado e finalizado sem erros, mas ainda sim irei usar esse projeto como base, para um melhor aprendizado de processos.
desde ja agredeço o tempo e atençao dedicados a visualização da minha solução. Abraços!!

# Execução do projeto:
    Para executar o projeto por completo sem nenhum tipo de erro, peço que por favor, inicie o arquivo na **main.py** localizado na pasta "src/app", rode o arquivo via terminal dentro do diretorio raiz do Projeto.

## 📁 Estrutura de Pastas de Dados
O fluxo de dados segue este caminho dentro do projeto:

data/
├── raw/          # Arquivos .zip originais baixados pelo crawler
├── extracted/    # CSVs originais após descompactação
└── consolidated/ # Destino Final
    └── {ano}/
        ├── consolidado_despesas.zip   # Saída do processamento
        ├── despesas_agregadas.csv     # Dados enriquecidos (Enriquecimento)
        └── estatisticas_despesas.csv  # Insights estatísticos (Validação)
------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ⚙️ Configurações Centrais (Settings):
    O coração do projeto reside no arquivo core/configs.py. Ele utiliza caminhos dinâmicos e padrões de busca (Regex) para garantir que o sistema se adapte a diferentes anos e estruturas de pastas no servidor da ANS.

    📂 Gestão de Diretórios
    O projeto segue uma estrutura de camadas para garantir a integridade dos dados:
        - PATH_DIR: Pasta raiz de dados (data/).

        - OUTPUT_DIR_RAW: Onde os arquivos brutos (Zips) são armazenados logo após o download.

        - OUTPUT_DIR_EXTRACTED: Pasta temporária para descompactação e leitura dos CSVs.

        - OUTPUT_DIR_CONSOLIDATED: Local final onde os relatórios enriquecidos e estatísticas são gerados.

    🌐 Parâmetros de Conexão e Busca:
        - BASE_URL: Endpoint oficial da ANS para dados abertos.

        - FILTER_PAGE_QUARTERS: Parâmetros de ordenação para garantir a captura dos trimestres mais recentes primeiro. 

        - REGEX_PATTERN_YEAR: Identifica pastas no formato YYYY/ (Ex: 2023/).

        - REGEX_PATTERN_QUARTER: Identifica arquivos de trimestres em múltiplos formatos (Ex: 2023_1_trimestre.zip, 1T2023.zip).

    🚀 Como Customizar o Ambiente
        O projeto possui uma flag de ambiente para controle de comportamento:

        Python
        # No arquivo core/configs.py
        ENV: str = "dev"
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Funcionalidades -> Services/

**Crawler Automatizado** -> Navega por links para identificar arquivos de despesas e o relatorio de operadoras de saúde ativas.

A classe principal ANSCrawler no arquivo src/app/services/crawler.py gerencia o ciclo de vida da extração:

Mapeamento de Origem: Utiliza URLs base configuradas via Settings para localizar as seções de "Demonstrações Contábeis" e "Operadoras Ativas".
Filtro Temporal: Localiza pastas específicas por ano utilizando Expressões Regulares (Regex).
Coleta de Trimestres: Acessa as páginas internas e identifica os últimos 3 arquivos .zip disponíveis para download.
Download Resiliente: Realiza o download via stream (para lidar com arquivos grandes) e valida se o conteúdo recebido é binário, evitando salvar páginas de erro HTML como se fossem dados.

## Descrição dos Métodos Principais:

Método -> **_get_page_quarters_by_year()**
Descrição: Método privado que busca o link da pasta do ano específico no portal

Método -> **get_last_3_quarters()**
Descrição: Navega até a página de trimestres e retorna uma lista com os 3 links de download mais recentes

Método -> **get_active_operators()**
Descrição: Localiza e retorna a URL direta para o relatório CSV de operadoras ativas.

Método -> **download_file()**
Descrição: Gerencia a persistência no disco, criando diretórios automaticamente e tratando erros de conexão.

## Estrutura de Saída
O sistema organiza os arquivos baixados seguindo a hierarquia definida no Settings.OUTPUT_DIR_RAW:

data/
└── raw/
    ├── {folder_name}/
    │   └── {filename}.zip
    └── operadoras_ativas.csv
------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Processor**

A classe DataProcessor realiza a "mágica" dos dados, utilizando Pandas com processamento em blocos (chunksize) para não estourar a memória RAM ao ler arquivos CSV pesados que foram extraidos do processamento de download do **Crawler**.

**OBS**: se voce tentar utilizar o DataProcessor sem antes ter feito o download dos arquivos .zip por meio do crawler, ira resultar em erro e o algoritimo não sera realizado de forma 100% efetiva.

## 🔍 Lógica de Filtragem Contábil
Para garantir a precisão dos dados de despesas, o processador aplica os seguintes filtros:
    - Código Contábil: Apenas contas que iniciam com 411 (Referentes a eventos/sinistros).
    - Descrição: Filtra registros onde a descrição contém termos como "despesa" E ("evento" OU "sinistro").

## Descrição dos Métodos Principais:

Método -> **unzip_all()**
Descrição: Extrai todos os arquivos baixados para a pasta de processamento.

Método -> **_get_consolidate_data()**
Descrição: Lê os CSVs em pedaços (chunks), aplica os filtros e mapeia cada linha para o objeto **ExpenseRecord**, após isso cada objeto é adicionado a lista privada da classe Principal. -> **self._consolidated = []**.

Método -> **consolidate_quarters()**
Descrição: Agrupa os dados por Operadora/Ano/Trimestre, soma os valores e gera o CSV final formatado em Real (R$).

## Estrutura de Saída
O sistema organiza os arquivos extraidos e consolidados seguindo a hierarquia definida no Settings.OUTPUT_DIR_EXTRACTED e Settings.OUTPUT_DIR_CONSOLIDATED:

data/    
├── extracted/
│    ├── {folder_name}/
│        └── {filename}.csv
├── consolidated/
    ├── {folder_name}/
        └── consolidado_despesas.zip
------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Enrichment and Validation**

O arquivo **enrichment.py** é responsável pelo "Check-mate" dos dados. 
Ele utiliza o registro da operadora **(REG_ANS)** contido no **active_operators.csv** e **consolidado despesas.csv** como chave primária para enriquecer o relatório financeiro.

## 🧩 Funcionalidades Principais:
    - Merge de Dados: Realiza um left join entre as despesas consolidadas e o cadastro de operadoras ativas.
    - Cálculo Estatístico: Gera automaticamente a Soma Total, Média Trimestral e o Desvio Padrão das despesas por Razão Social e Estado (UF).
    - Validação de Integridade: Garante que apenas operadoras com CNPJ válido e dados presentes no cruzamento de planilhas sejam reportadas.

    **Relatórios Gerados:**
        - despesas_agregadas.csv -> Relatório detalhado com CNPJ, Razão Social, UF, Modalidade e Valor.

        **Resposta Desafio Adicional:**
        - estatisticas_despesas.csv -> Tabela resumida com métricas de média, soma e variação (desvio padrão).
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------


# 🚀 Como Executar o Pipeline Completo
O projeto foi desenhado para ser executado em sequência:

Python
    # 1. DOWNLOAD
    crawler = ANSCrawler()
    crawler.get_last_3_quarters(2023)

    # 2. PROCESSAMENTO (Limpeza e Filtro Contábil)
    processor = DataProcessor("2023")
    processor.unzip_all()
    processor.consolidate_quarters()

    # 3. VALIDAÇÃO (Enriquecimento e Estatísticas)
    validator = ANSValidation("2023")
    validator.generate_aggregate_expenses_and_statistics()

    
