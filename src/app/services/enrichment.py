import os
import zipfile
from pathlib import Path

import pandas as pd

from app.core.configs import Settings
from app.records.expense import AggregateExpense
from app.shared import RegisterANS, CNPJ, ValueExpense


class ANSValidation:
    
    def __init__(self, year):
        self.consolidated_dir = Path(Settings.OUTPUT_DIR_CONSOLIDATED) / str(year)
        self.active_operators_dir = Path(Settings.OUTPUT_DIR_RAW) / "operators"
    
    def generate_aggregate_expenses_and_statistics(self):
        
        expenses = self._get_expenses_with_merge_csv()
        
        df = pd.DataFrame([
            {   
                'CNPJ': e.cnpj.value,
                'RAZAO_SOCIAL': e.social_reason,
                'REGISTRO_ANS': str(e.ansReg.value),
                'MODALIDADE': e.modality,
                'UF': e.uf,
                'TRIMESTRE': e.quarter,
                'ANO': e.year,
                'VL_DESPESA': e.value.value
            } for e in expenses
        ])
        
        if df.empty:
            raise FileNotFoundError("Nao existe nenhuma linha consolidada para agregacao")
        
        df_stats = df.groupby(['RAZAO_SOCIAL','UF']).agg({
            'VL_DESPESA': [
                ('Total_Despesas', 'sum'),
                ('Media_Trimestral', 'mean'),
                ('Desvio_Padrao', 'std')
            ]
        })
        
        df_stats.columns = df_stats.columns.get_level_values(1)
        df_stats = df_stats.reset_index()
        
        df_stats['Desvio_Padrao'] = df_stats['Desvio_Padrao'].fillna(0.0)
        df_stats = df_stats.sort_values(by='Total_Despesas', ascending=False)
        
        df['VL_DESPESA'] = df['VL_DESPESA'].map(lambda x: ValueExpense(value=x).to_br_currency)
        df.to_csv(f"{self.consolidated_dir}/despesas_agregadas.csv", index=False, sep=',')
        df_stats.to_csv(f"{self.consolidated_dir}/estatisticas_despesas.csv", index=False, sep=',')
    
    def _get_expenses_with_merge_csv(self):
        
        df_consolidated = self._get_consolidated_df()
        df_active_operators = self._get_active_operators_df()
        
        df_final = pd.merge(
            df_consolidated,
            df_active_operators,
            on='REGISTRO_OPERADORA',
            how='left'
        )
        df_final = df_final.dropna(subset=['CNPJ'])
        
        if df_final.empty:
            raise SystemError("Nao foi possivel filtrar dados com planilhas disponveis!")

        aggregateExpenses = []
        for _, row in df_final.iterrows():
            aggregateExpense = AggregateExpense(
                ansReg=RegisterANS(value=row['REGISTRO_OPERADORA']),
                cnpj=CNPJ(value=row['CNPJ']),
                social_reason=str(row['Razao_Social']),
                modality=str(row['Modalidade']),
                uf=str(row['UF']),
                quarter=int(row['TRIMESTRE']),
                year=int(row['ANO']),
                value=ValueExpense(value=row['VL_DESPESA'])
            )        
            aggregateExpenses.append(aggregateExpense)
        return aggregateExpenses
    
    def _get_consolidated_df(self):
        if len(os.listdir(self.consolidated_dir)) <= 0:
            raise FileExistsError(f"Nao existe nenhum arquivo consolidado na pasta {self.consolidated_dir}")
        
        for file in os.listdir(self.consolidated_dir):
            if file.endswith('.zip'):
                zip_path = Path(self.consolidated_dir / file)
                with zipfile.ZipFile(zip_path, 'r') as z:
                    csv_filename = z.namelist()[0]
                    
                    with z.open(csv_filename) as f:
                        df = pd.read_csv(f, sep=",", encoding='utf-8')
                        return df
    
    def _get_active_operators_df(self):
        path = Path(self.active_operators_dir) / "active_operators"
        df = pd.read_csv(path, sep=';', encoding='utf-8', dtype={'CNPJ': str})
        return df
        
        