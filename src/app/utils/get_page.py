from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError

from app.responses.erros_response import NOT_FOUND_404

def get_soup(url: str, parser: str = "html.parser") -> BeautifulSoup:
    try:    
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code != 200:
            raise Exception("Pagina nao encontrada!")

        return BeautifulSoup(response.text, parser)
    
    except HTTPError as e:
        return None
    
