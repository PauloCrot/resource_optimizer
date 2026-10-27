import pandas as pd
import pytest
from src.metrics import calculate_evm_indices, apply_risk_classification

def test_calculate_evm_indices():
    """Valida se CPI (EV/AC) e SPI (EV/PV) estao matematicamente corretos."""
    df_dummy = pd.DataFrame({
        'PV_Clean': [100000.0],
        'EV_Clean': [80000.0],
        'AC_Clean': [100000.0]
    })
    
    df_res = calculate_evm_indices(df_dummy)
    
    assert df_res['CPI'].iloc[0] == pytest.approx(0.8)
    assert df_res['SPI'].iloc[0] == pytest.approx(0.8)

def test_apply_risk_classification():
    """Valida a categorizacao de status de risco conforme as regras de negocio."""
    df_dummy = pd.DataFrame({
        'CPI': [0.75, 0.95, 1.05],
        'SPI': [0.70, 0.98, 1.00]
    })
    
    df_res = apply_risk_classification(df_dummy)
    
    assert "CRÍTICO" in df_res['Status_Risco'].iloc[0]
    assert "ATENÇÃO" in df_res['Status_Risco'].iloc[1]
    assert "SAUDÁVEL" in df_res['Status_Risco'].iloc[2]