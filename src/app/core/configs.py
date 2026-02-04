from urllib.parse import urljoin

class Settings:
    
    PATH_DIR = "data"
    OUTPUT_DIR_RAW = f"{PATH_DIR}/raw"
    OUTPUT_DIR_EXTRACTED = f"{PATH_DIR}/extracted"
    OUTPUT_DIR_CONSOLIDATED = f"{PATH_DIR}/consolidated"
    
    ENV: str = "dev"
    
    BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/"
    
    FILTER_PAGE_QUARTERS = "?C=N;O=D"
    REGEX_PATTERN_YEAR = r"^\d{4}/$"
    REGEX_PATTERN_QUARTER = r'^(\d{4}_\d_trimestre|[1-4]T\d{4}|\d{4}-[1-4]t)\.zip$i'
       
    