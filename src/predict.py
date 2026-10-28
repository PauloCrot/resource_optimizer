from cleaning import load_and_clean_data
from metrics import calculate_evm_indices, apply_risk_classification
from ml import train_and_predict_risk

def run_predictive_pipeline():
    print("==================================================")
    print("     DIAGNOSTICO PREDITIVO DE IA")
    print("==================================================")
    
    # 1. Carga e preparacao do dataset
    df = load_and_clean_data()
    if df is None:
        return
        
    df = calculate_evm_indices(df)
    df = apply_risk_classification(df)
    
    # 2. Execucao da IA Preditiva
    df_ml_results = train_and_predict_risk(df)
    
    # 3. Exibicao do resultado
    print(df_ml_results.to_string(index=False))
    
    # 4. Exportacao do relatorio preditivo
    output_path = 'data/ml_predictive_report.csv'
    df_ml_results.to_csv(output_path, index=False)
    print(f"\n[OK] Relatorio preditivo exportado para '{output_path}'")

if __name__ == '__main__':
    run_predictive_pipeline()