from app.services.processor import DataProcessor

def extract_DC_by_year(year: int):
    p = DataProcessor(str(year))
    p.unzip_all()
    print("Arquivos Extraidos!")
    p.consolidate_quarters()
    
