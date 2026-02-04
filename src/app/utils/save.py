import os
import shutil

def save_file(path, request) -> bool:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        for chunk in request.iter_content(chunk_size=8192):
            f.write(chunk)
            
def delete_file(path, folder):
    if os.path.exists(path):
        try:
            shutil.rmtree(folder)
            print("arquivo apagado em env de TESTE")
        except Exception as e:
            print(f"Error ao excluir {folder}: {e}")
            return False