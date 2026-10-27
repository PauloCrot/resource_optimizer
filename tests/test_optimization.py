import pandas as pd
from src.optimization import optimize_resource_allocation

def test_optimize_resource_allocation_budget_constraint():
    """Garante que a soma dos aportes nunca excede o teto orcamentario global estipulado."""
    df_dummy = pd.DataFrame({
        'ID_Proj': ['PRJ-01', 'PRJ-02'],
        'Nome_Projeto': ['Projeto Alfa', 'Projeto Beta'],
        'Data_Ref': ['2026-10-01', '2026-10-01'],
        'CPI': [0.70, 0.75],
        'SPI': [0.65, 0.70],
        'AC_Clean': [2000000.0, 2000000.0]
    })
    
    orcamento_limite = 500000.0
    df_opt = optimize_resource_allocation(df_dummy, total_budget=orcamento_limite)
    
    total_alocado = df_opt['Aporte_Otimizado'].sum()
    assert total_alocado <= orcamento_limite

def test_optimize_resource_allocation_max_demand_constraint():
    """Garante que nenhum projeto recebe mais de 30% do seu Custo Real (AC)."""
    df_dummy = pd.DataFrame({
        'ID_Proj': ['PRJ-01'],
        'Nome_Projeto': ['Projeto Teste'],
        'Data_Ref': ['2026-10-01'],
        'CPI': [0.80],
        'SPI': [0.80],
        'AC_Clean': [1000000.0]
    })
    
    df_opt = optimize_resource_allocation(df_dummy, total_budget=1000000.0)
    
    aporte_recebido = df_opt['Aporte_Otimizado'].iloc[0]
    assert aporte_recebido == 300000.0