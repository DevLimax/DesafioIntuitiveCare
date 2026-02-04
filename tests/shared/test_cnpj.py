import pytest
from pydantic import ValidationError
from app.shared import CNPJ

def test_deve_retornar_cnpj_valido():
    cnpj = CNPJ(value="30.978.161/0001-15")
    cnpj_2 = CNPJ(value="18881781000136")
    
    assert cnpj.value == "30978161000115"
    assert cnpj.formatted == "30.978.161/0001-15"
    
    assert cnpj_2.value == "18881781000136"
    assert cnpj_2.formatted == "18.881.781/0001-36"

@pytest.mark.parametrize("invalid_input", [
    ("11111111111111"), 
    ("123491827162514"),
    ("123456789"),
    ("ABCDEFASD"),
    ("")
])
def test_deve_retornar_excecao_com_cnpj_invalido(invalid_input):
    with pytest.raises(ValidationError):
        CNPJ(value=invalid_input)
        
