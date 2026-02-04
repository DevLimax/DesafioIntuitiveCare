from pydantic import BaseModel, Field, field_validator, ConfigDict
import re

class RegisterANS(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    value: str = Field(...)
    
    @field_validator('value', mode='before')
    @classmethod
    def validate_data(cls, v):
        try:
            if isinstance(v, (float, int)):
                v = str(v)
                        
            if len(v) < 1:
                raise ValueError(f"Numero {v} invalido!")
        
            return v
        except Exception as e:
            raise ValueError(f"Erro durante conversao: {e}")
        
    @property
    def valueStr(self):
        return f"{self.value}"
        
        
        