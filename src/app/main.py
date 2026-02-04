from app.views.crawler_view import download_DC_View
from app.views.processor_view import extract_DC_by_year
from app.views.enrichment_view import generate_aggregate_expenses_view
from app.services.enrichment import ANSValidation

def main():
    try:
        choice_year = int(input("Informe o ano em que deseja obter os dados para consolidacao: "))
        did_download = download_DC_View(choice_year)
        
        if did_download:
            extract_DC_by_year(choice_year)
            generate_aggregate_expenses_view(choice_year)
    
    except ValueError as e:
        print(f"Formato invalido!: {e}")
        
           
if __name__ == "__main__":
    main()