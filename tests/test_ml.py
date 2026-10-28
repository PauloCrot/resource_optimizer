import pandas as pd
import pytest
from src.ml import train_and_predict_risk

def test_train_and_predict_risk():
    """
    Valida se a probabilidade predita pela IA esta entre 0% e 100%.
    """

    df_dummy = pd.DataFrame({
        'ID_Proj': ['PRJ-01', 'PRJ-02'],
        'Nome_Projeto': ['Projeto Alfa', 'Projeto Beta'],
        'Data_Ref': ['2026-10-01', '2026-10-01'],
        'CPI': [0.70, 1.10],
        'SPI': [0.65, 1.05],
        'Status_Risco': ['🔴 CRÍTICO', '🟢 SAUDÁVEL']
    })

    df_res = train_and_predict_risk(df_dummy)

    assert 'Prob_Critico_Futuro' in df_res.columns
    assert 0.0 <= df_res['Prob_Critico_Futuro'].iloc[0] <= 100.0
    assert 0.0 <= df_res['Prob_Critico_Futuro'].iloc[1] <= 100.0