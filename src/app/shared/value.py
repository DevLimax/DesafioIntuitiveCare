from pydantic import BaseModel, Field, field_validator, ConfigDict
from decimal import Decimal
import re

class ValueExpense(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    value: Decimal = Field(...)
    
    @field_validator('value', mode='before')
    @classmethod
    def validate_data(cls, v):
        try:
            if isinstance(v, (int, float)):
                return Decimal(v)
            
            if isinstance(v, str):
                v = v.strip()
                if ',' in v and '.' and v:
                    v = v.replace(".", "").replace(",", ".")
                elif ',' in v:
                    v = v.replace(',', '.')
                    
            return Decimal(v)
        except Exception as e:
            raise ValueError(f"Erro durante formatacao do numero: {v}, detalhe: {e}")
    
    @property
    def to_br_currency(self) -> str:
        us_format = f"{self.value:,.2f}"
        
        return us_format.replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def __str__(self):
        return self.value