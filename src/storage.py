import os

def save_processed_report(df, filepath='data/processed_evm_report.csv'):
    """Salva o DataFrame processado e ordenado em um arquivo CSV de saída."""
    output_dir = os.path.dirname(filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    df.to_csv(filepath, index=False, sep=';', encoding='utf-8')
    print(f"Relatório processado exportado com sucesso para {filepath}")