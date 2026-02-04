📊 Projeto Despesas - Pipeline ANS
Este é um sistema de Web Scraping desenvolvido em Python para automatizar a coleta, processamento e visualização de dados de despesas (Demonstrações Contábeis/DC) da Agência Nacional de Saúde Suplementar (ANS).

[!IMPORTANT]

Nota do Desenvolvedor: Por conta do tempo, o projeto foi focado na estabilidade do ciclo principal (Coleta -> Processamento -> Validação). Ele serve como uma base sólida para aprendizado de processos ETL e automação.

🔗 Fonte de Dados
O projeto consome dados da API/FTP pública da ANS:

https://dadosabertos.ans.gov.br/FTP/PDA/

🚀 Como Executar
Para rodar o pipeline completo, execute o arquivo principal a partir da raiz do projeto:

Bash
python src/app/main.py
Exemplo de Uso Interno
O fluxo foi desenhado para ser executado em sequência lógica:

Python
# 1. DOWNLOAD (Crawler)
crawler = ANSCrawler()
crawler.get_last_3_quarters(2023)

# 2. PROCESSAMENTO (Limpeza e Filtro Contábil)
processor = DataProcessor("2023")
processor.unzip_all()
processor.consolidate_quarters()

# 3. VALIDAÇÃO (Enriquecimento e Estatísticas)
validator = ANSValidation("2023")
validator.generate_aggregate_expenses_and_statistics()
📁 Estrutura de Dados (Fluxo ETL)
O projeto organiza os dados em camadas para garantir a integridade:

Plaintext
data/
├── raw/            # Arquivos .zip originais (Download bruto)
├── extracted/      # CSVs descompactados (Processamento temporário)
└── consolidated/   # Destino Final (Dados prontos para análise)
    └── {ano}/
        ├── consolidado_despesas.zip   # Dados filtrados por regra contábil
        ├── despesas_agregadas.csv     # Dados enriquecidos com CNPJ/Razão Social
        └── estatisticas_despesas.csv  # Insights: Média, Soma e Desvio Padrão
⚙️ Configurações (Settings)
Centralizadas em src/app/core/configs.py, utilizam caminhos dinâmicos e Regex para maior adaptabilidade.

Gestão de Diretórios: Automação na criação e mapeamento de pastas.

Parâmetros de Busca: Regex flexíveis para identificar anos (YYYY/) e diferentes nomenclaturas de trimestres (ex: 1T2023, 2023_1_trimestre).

Controle de Ambiente: Flag ENV = "dev" para alternar comportamentos de teste.

🛠️ Funcionalidades e Camadas
1. Crawler Automatizado (Services/Crawler)
Gerencia o ciclo de vida da extração com as seguintes características:

Mapeamento Inteligente: Localiza seções de "Demonstrações Contábeis" e "Operadoras Ativas".

Download Resiliente: Usa streams para arquivos grandes e valida se o conteúdo é binário (evita salvar erros HTML).

2. Processor (Services/Processor)
Realiza a "mágica" dos dados usando Pandas com chunksize, processando arquivos pesados sem estourar a memória RAM.

Filtro Contábil: * Contas iniciadas em 411 (Eventos/Sinistros).

Descrições que contenham "despesa" e ("evento" ou "sinistro").

Consolidação: Agrupa por Operadora/Ano/Trimestre com soma de valores.

3. Enrichment & Validation (Services/Validation)
O "Check-mate" dos dados. Cruza as despesas com o cadastro de operadoras (active_operators.csv).

Merge: Left join utilizando o REG_ANS como chave primária.

Estatísticas: Gera automaticamente Soma, Média e Desvio Padrão por Razão Social e UF.

Integridade: Filtra apenas operadoras com CNPJ válido.

📊 Desafio Adicional (Resultados)
Ao final da execução, o arquivo estatisticas_despesas.csv entrega uma tabela resumida com métricas de variação e performance financeira por estado e operadora.

Desenvolvido por [devlimax] 🚀

Abraços e obrigado pela atenção!
