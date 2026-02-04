import os
import re
import zipfile

from app.core.configs import Settings

def extract_folder_name_to_quarters_path(path: str):
    try:
        idx = path.index("/")
        return path[:idx]
    
    except Exception as e:
        print("Nao foi possivel extrair o nome da pasta com o arquivo enviado")
        
def extract_filename_to_quarters_path(path: str):
    try:
        idx = path.index("/")
        return path[idx+1:]
    except Exception as e:
        print("Nao foi possivel extrair o nome da arquivo com o arquivo enviado")
        
def extract_quarter_and_year(path: str):
    
    pattern = r"(\d)T.*?(\d{4})"
    match = re.search(pattern, path, re.IGNORECASE)
    
    if match:
        quarter = match.group(1)
        year = match.group(2)
        return quarter, year
    
    return None, None

def extract_zipfile_by_folder(path: str, extract_path: str):
    if len(os.listdir(path)) <= 0:
        return print("Pasta vazia!")
    
    try:
        for file in os.listdir(path):
            if file.endswith('.zip'):
                path_to_zip = os.path.join(path, file)
                with zipfile.ZipFile(path_to_zip, 'r') as zip_ref:
                    if extract_path:
                        zip_ref.extractall(extract_path)
                    else:
                        zip_ref.extractall(path)
                    print(f"{file} extraido na pasta: {extract_path if extract_path else path}")

    except Exception as e:
        raise FileNotFoundError("Nao foi possivel encontrar o arquivo para extracao")

        

    