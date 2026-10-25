import pandas as pd
from storage import save_optimization_report

def optimize_resource_allocation(df, total_budget=2500000.0):
    """
    Otimiza a alocacao de recursos utilizando a logica do Fractional Knapsack.
    """
    df_latest = df.sort_values('Data_Ref').groupby('ID_Proj').tail(1).copy()
    df_target = df_latest[(df_latest['CPI'] < 1.0) | (df_latest['SPI'] < 1.0)].copy()
    
    if df_target.empty:
        print("Nenhum projeto em estado critico ou de atencao para otimizacao.")
        return None

    results = []
    
    for idx, row in df_target.iterrows():
        cpi = row['CPI']
        spi = row['SPI']
        ac = row['AC_Clean']
        
        peso = max(0.1, 2.0 - (cpi + spi) / 2.0)
        demanda_max = ac * 0.30
        
        results.append({
            'ID_Proj': row['ID_Proj'],
            'Nome_Projeto': row['Nome_Projeto'],
            'Custo_Atual_AC': ac,
            'Demanda_Max': demanda_max,
            'Fator_Urgencia_Peso': round(peso, 4),
            'Aporte_Otimizado': 0.0
        })
        
    df_opt = pd.DataFrame(results)
    df_opt = df_opt.sort_values(by='Fator_Urgencia_Peso', ascending=False).reset_index(drop=True)
    
    orcamento_restante = total_budget
    
    for idx, row in df_opt.iterrows():
        if orcamento_restante <= 0:
            break
            
        aporte = min(row['Demanda_Max'], orcamento_restante)
        df_opt.at[idx, 'Aporte_Otimizado'] = round(aporte, 2)
        orcamento_restante -= aporte
        
    df_opt = df_opt.drop(columns=['Demanda_Max'])
    return df_opt

if __name__ == '__main__':
    print("==================================================")
    print("    OTIMIZACAO DE ALOCACAO DE ORCAMENTO EXTRA     ")
    print("==================================================")
    
    try:
        df_processed = pd.read_csv('data/processed_evm_report.csv', sep=';')
        df_opt = optimize_resource_allocation(df_processed, total_budget=2500000.0)
        
        if df_opt is not None:
            save_optimization_report(df_opt)
            print(df_opt.to_string(index=False))
            print("\n[OK] Resultado salvo em 'data/optimized_resource_allocation.csv'")
    except FileNotFoundError:
        print("Erro: O arquivo 'data/processed_evm_report.csv' nao foi encontrado.")
        print("Execute primeiro 'python src/main.py' para gerar os dados de auditoria.")