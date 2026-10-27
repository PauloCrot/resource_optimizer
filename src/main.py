from cleaning import load_and_clean_data
from metrics import calculate_evm_indices, apply_risk_classification, sort_temporal_data
from storage import save_processed_report
from plots import generate_cpi_spi_matrix, generate_evm_trends  # <-- NOVO IMPORT

def run_audit_pipeline():
    print("==================================================")
    print("        RELATORIO DE AUDITORIA DE CAMPO EVM       ")
    print("==================================================")
    
    # 1. Ingestao e Limpeza
    df = load_and_clean_data()
    if df is None:
        return

    # 2. Processamento EVM
    df = calculate_evm_indices(df)
    df = apply_risk_classification(df)
    df = sort_temporal_data(df)
    
    # 3. Persistencia de Dados
    save_processed_report(df)
    
    generate_cpi_spi_matrix(df)
    generate_evm_trends(df)
    
    print(
        df[[
            'ID_Proj',
            'Nome_Projeto',
            'Data_Ref',
            'CPI',
            'SPI',
            'Status_Risco',
        ]].to_string(index=False)
    )
    print("\n[OK] Relatorio exportado para 'data/processed_evm_report.csv'")
    print("[OK] Graficos gerados em 'data/cpi_spi_matrix.png' e 'data/evm_trends.png'")

if __name__ == '__main__':
    run_audit_pipeline()