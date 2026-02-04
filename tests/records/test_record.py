import pytest
from app.records.expense import ExpenseRecord

from app.shared import RegisterANS, ValueExpense

def test_deve_retornar_instancia_de_expense_valida():
    
    expense = ExpenseRecord(
        year=2024,
        quarter=3,
        ansReg=RegisterANS(value="928121"),
        value=ValueExpense(value="-670.12"),
    )
    
    assert expense.ansReg.value == 928121
    assert expense.value.value == -670.12
    