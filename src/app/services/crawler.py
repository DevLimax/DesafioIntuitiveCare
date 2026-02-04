import os 
import requests
import re

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.core.configs import Settings
from app.records.response import Response
from app.responses.erros_response import NOT_FOUND_404
from app.utils import save_file, delete_file, get_soup

class ANSCrawler:
    def __init__(self):
        self.financial_statements_url = urljoin(Settings.BASE_URL, "demonstracoes_contabeis/")
        self.active_operators_url = urljoin(Settings.BASE_URL, "operadoras_de_plano_de_saude_ativas/")
        self.output_dir = Settings.OUTPUT_DIR_RAW
        os.makedirs(self.output_dir, exist_ok=True)
        
    def _get_page_quarters_by_year(self, year):
            page = get_soup(self.financial_statements_url)
            href_elements = page.find_all("a", href=re.compile(Settings.REGEX_PATTERN_YEAR))
            content = [element.get('href') for element in href_elements if str(year) in element['href']]
            if len(content) == 0:
                return NOT_FOUND_404(f"'/{year}'", self.financial_statements_url)
            
            return Response(content[0], 200)
        
    def get_last_3_quarters(self, year: int):
        response = self._get_page_quarters_by_year(year)
        if response.status_code == 404:
            return response
        
        path = response.content        
        url = urljoin(self.financial_statements_url, f"{path}/{Settings.FILTER_PAGE_QUARTERS}")
        page = get_soup(url)
        
        links_to_quarters_download = page.find_all("a", href=True)
        quarters_set = set()
        
        for link in links_to_quarters_download:
            if len(quarters_set) == 3:
                break
            
            elif link.get('href').endswith(".zip"):
                quarters_set.add(urljoin(path, link.get('href')))
        return Response(sorted(list(quarters_set), reverse=True), 200)
    
    def get_active_operators(self):
        page = get_soup(self.active_operators_url)
        
        link_csv_report = page.find_all("a", href= lambda href: href and href.endswith(".csv"))
        return link_csv_report[0].get('href')    
    
    
    def download_file(self, 
                      url: str,
                      filename: str,
                      folder: str):
        path_upload = os.path.join(Settings.OUTPUT_DIR_RAW, folder, filename)
        os.makedirs(os.path.dirname(path_upload), exist_ok=True)
        try: 
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                
                if "text/html" in r.headers.get("Content-Type", ""):
                    print(f"Erro: o link {url} retornou HTML em vez de ZIP")
                
                save_file(path_upload, r)
            print(f"Download Concluido: {path_upload}")
            
            if Settings.ENV == "test":
                delete_file(path_upload, os.path.join(Settings.OUTPUT_DIR_RAW, folder))        
        
        except Exception as e:
            print(f"Falha ao baixar {url}: {e}")
            
        
    