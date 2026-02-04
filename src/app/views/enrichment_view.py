from app.services import ANSValidation
from app.core.configs import Settings

def generate_aggregate_expenses_view(year: int):
    v = ANSValidation(year)
    v.generate_aggregate_expenses_and_statistics()
    print(f"Gerado o arquivo de despesas agregadas e estatisticas em {Settings.OUTPUT_DIR_CONSOLIDATED}/{year}")