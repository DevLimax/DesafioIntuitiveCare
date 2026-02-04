from app.services import ANSCrawler
from app.core.configs import Settings

from app.utils import extract_filename_to_quarters_path, extract_folder_name_to_quarters_path

from urllib.parse import urljoin

def download_DC_View(year: int):
    ans = ANSCrawler()
    
    if len(str(year)) > 4 or len(str(year)) < 4:
        return print("Ano invalido para pesquisa!")
    

    response = ans.get_last_3_quarters(year)    
    if response.status_code == 400:
        print(response.content)
        return False
    
    if response.status_code == 200:  
        for quarter in response.content:
            folder = extract_folder_name_to_quarters_path(quarter)
            filename = extract_filename_to_quarters_path(quarter)
            url = urljoin(ans.financial_statements_url, f"{folder}/{filename}")            
            ans.download_file(url, filename, folder)
        _download_activeOPerators()
        print("Download de arquivos finalizado")
        return True
    else:
        print(f"Erro: {response.content}, status: {response.status_code}")
        return False
    
def _download_activeOPerators():
    ans = ANSCrawler()
    
    link = ans.get_active_operators()
    url = urljoin(ans.active_operators_url, link)
    ans.download_file(url,
                      folder='operators',
                      filename='active_operators')
    
    
    
    