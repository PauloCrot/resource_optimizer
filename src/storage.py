import os

def save_processed_report(df, filepath='data/processed_evm_report.csv'):
    """Salva o DataFrame processado de EVM em CSV."""
    output_dir = os.path.dirname(filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    df.to_csv(filepath, index=False, sep=';', encoding='utf-8')

def save_optimization_report(df_opt, filepath='data/optimized_resource_allocation.csv'):
    """Salva o resultado do modelo de otimizacao em CSV."""
    if df_opt is None or df_opt.empty:
        return
    
    output_dir = os.path.dirname(filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    df_opt.to_csv(filepath, index=False, sep=';', encoding='utf-8')