import pytest
from app.shared import ValueExpense


def test_format():
    value = ValueExpense(value=571672990.21)
    
    assert value.to_br_currency == "571.672.990,21"