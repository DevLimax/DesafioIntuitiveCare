from pydantic import BaseModel, Field, field_validator

from app.shared import CNPJ, ValueExpense, RegisterANS

class ExpenseRecord(BaseModel):
    ansReg: RegisterANS
    year: int
    quarter: int
    description: str = None
    value: ValueExpense

    @field_validator('year', mode='before')
    @classmethod
    def validate_year(cls, v):
        v = str(v)
        
        if len(v) < 4 or len(v) > 4:
            raise ValueError(f"Ano inserido: {v}, esta invalido!")
        return v
    
    @field_validator('quarter', mode='before')
    @classmethod
    def validate_quarter(cls, v):
        if v > 4 or v < 1:
            raise ValueError(f"Trimestre {v} nao e valido")
        return v
        
class AggregateExpense(ExpenseRecord):
    cnpj: CNPJ = None
    social_reason: str = None
    modality: str = None
    uf: str = None
    
    @field_validator('uf', mode='before')
    @classmethod
    def validar_uf(cls, v):
        if not isinstance(v, str):
            raise ValueError("UF invalida!")
        if len(v) < 2 or len(v) > 2:
            raise ValueError("UF invalida!")
        return v.upper()
    
    
    
    
    
    
        