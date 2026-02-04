
from pydantic import BaseModel, Field, field_validator, ConfigDict
from validate_docbr import CNPJ as CNPJValidator
import re

class CNPJ(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    value: str = Field(..., max_length=14)
      
    @field_validator('value', mode='before')
    @classmethod
    def validate_data(cls, v):
        validator = CNPJValidator()
        if not isinstance(v, str):
            v = str(v)
        
        cleaned = re.sub(r'\D', '', v)
        if not validator.validate(cleaned):
            raise ValueError('CNPJ invalido!')
        return cleaned
        
    @property
    def formatted(self) -> str:
        return CNPJValidator().mask(self.value)
    
    def __str__(self):
        return self.value
        