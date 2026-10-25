from cleaning import load_and_clean_data
from metrics import calculate_evm_indices, apply_risk_classification, sort_temporal_data
from storage import save_processed_report

def run_pipeline():
    print("INICIANDO PIPELINE DE AUDITORIA EVM")
    
    df = load_and_clean_data()
    if df is None:
        return

    df = calculate_evm_indices(df)
    df = apply_risk_classification(df)
    df = sort_temporal_data(df)

    save_processed_report(df)

    print("\nRESULTADOS PROCESSADOS")
    print(
        df[[
            'ID_Proj',
            'Nome_Projeto',
            'Data_Ref',
            'CPI',
            'SPI',
            'Status_Risco',
            'Obs_Campo',
        ]].to_string(index=False)
    )

if __name__ == '__main__':
    run_pipeline()