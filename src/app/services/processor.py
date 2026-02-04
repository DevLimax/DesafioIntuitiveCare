import zipfile
import os
import pandas as pd

from app.core.configs import Settings
from app.utils.extract import extract_quarter_and_year, extract_zipfile_by_folder

from app.records.expense import ExpenseRecord
from app.shared import RegisterANS, ValueExpense

class DataProcessor:
    def __init__(self, year):
        self.raw_dir = os.path.join(Settings.OUTPUT_DIR_RAW, year)
        self.extracted_dir = os.path.join(Settings.OUTPUT_DIR_EXTRACTED, year)
        self.consolidated_dir = os.path.join(Settings.OUTPUT_DIR_CONSOLIDATED, year)
        
        self._consolidated = []
        
        os.makedirs(Settings.OUTPUT_DIR_EXTRACTED, exist_ok=True)
        os.makedirs(self.consolidated_dir, exist_ok=True)
        
    def unzip_all(self):
        extract_zipfile_by_folder(self.raw_dir, self.extracted_dir)
    
    def _get_consolidate_data(self):
        
        for filepath in os.listdir(self.extracted_dir):
            quarter, year = extract_quarter_and_year(filepath)
            path = os.path.join(self.extracted_dir, filepath) 

            chunks = pd.read_csv(path, sep=';', encoding='latin-1', chunksize=50000)
            for chunk in chunks:
                account_condition = chunk['CD_CONTA_CONTABIL'].astype(str).str.startswith('411')
                desc_lower = chunk['DESCRICAO'].astype(str).str.lower()
                description_condition = desc_lower.str.startswith('despesa') & desc_lower.str.contains('evento|sinistro', na=False)
            
                filtered_data = chunk[account_condition & description_condition]

            if not filtered_data.empty:
                
                for _, row in filtered_data.iterrows():    
                    expense = ExpenseRecord(
                        ansReg = RegisterANS(value=row['REG_ANS']),
                        description = row['DESCRICAO'],
                        value = ValueExpense(value=row['VL_SALDO_FINAL']),
                        quarter = int(quarter),
                        year = int(year)
                    )
                    self._consolidated.append(expense)
            
    def consolidate_quarters(self):
        self._get_consolidate_data()
        
        if not self._consolidated:
            print("⚠️ Nenhum dado relevante encontrado para consolidar.")\
        
        df = pd.DataFrame([
            {   
                
                'REGISTRO_OPERADORA': str(e.ansReg.value),
                'DESCRICAO': e.description,
                'VL_DESPESA': e.value.value,
                'TRIMESTRE': e.quarter,
                'ANO': e.year
            } for e in self._consolidated
        ])
        
        df_consolidate = df.groupby(['REGISTRO_OPERADORA', 'ANO', 'TRIMESTRE'], as_index=False).agg({
                'VL_DESPESA': 'sum',
                'DESCRICAO': 'first'
        })
        df_consolidate['VL_DESPESA'] = df_consolidate['VL_DESPESA'].map(lambda x: ValueExpense(value=x).to_br_currency)       
        df_consolidate.to_csv(f"{self.consolidated_dir}/consolidado_despesas.zip",index=False, sep=',')
        print(f"Arquivo consolidado gerado em: {self.consolidated_dir}") 
            
            
    