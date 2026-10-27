import os
import matplotlib.pyplot as plt
import seaborn as sns

def _ensure_dir(filepath):
    output_dir = os.path.dirname(filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

def generate_cpi_spi_matrix(df, filepath='data/cpi_spi_matrix.png'):
    _ensure_dir(filepath)
    
    # Adiciona .copy() para evitar warnings do Pandas
    df_latest = df.sort_values('Data_Ref').groupby('ID_Proj').tail(1).copy()

    # Cria uma coluna temporária sem emojis para a legenda do gráfico
    mapa_limpo = {
        "🟢 SAUDÁVEL (No Prazo/Orçamento)": "SAUDÁVEL", 
        "🟡 ATENÇÃO (Desvio Leve)": "ATENÇÃO", 
        "🔴 CRÍTICO (Ação Imediata)": "CRÍTICO"
    }
    df_latest['Status_Legenda'] = df_latest['Status_Risco'].map(mapa_limpo)

    plt.figure(figsize=(8,6))

    cores = {"SAUDÁVEL": "green", "ATENÇÃO": "orange", "CRÍTICO": "red"}

    sns.scatterplot(
        data=df_latest, x='SPI', y='CPI',
        hue='Status_Legenda', palette=cores, s=120, edgecolor='black'
    )

    plt.axhline(1.0, color='gray', linestyle='--', alpha=0.7)
    plt.axvline(1.0, color='gray', linestyle='--', alpha=0.7)

    plt.title('Matriz de Desempenho de Projetos', fontsize=14, weight='bold')
    plt.xlabel('SPI (Desempenho de Cronograma)', fontsize=11)
    plt.ylabel('CPI (Desempenho de Custo)', fontsize=11)
    
    plt.legend(title="Status do Risco", bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()

def generate_evm_trends(df, filepath='data/evm_trends.png'):
    _ensure_dir(filepath)
    
    df_trend = df.groupby('Data_Ref')[['CPI', 'SPI']].mean().reset_index()

    plt.figure(figsize=(10, 5))
    
    sns.lineplot(data=df_trend, x='Data_Ref', y='CPI', marker='o', label='CPI Médio', linewidth=2)
    sns.lineplot(data=df_trend, x='Data_Ref', y='SPI', marker='s', label='SPI Médio', linewidth=2)
    
    plt.axhline(1.0, color='red', linestyle='--', alpha=0.5, label='Linha Base (1.0)')
    
    plt.title('Tendência Histórica de Desempenho do Portfólio', fontsize=14, weight='bold')
    plt.xlabel('Data de Medição', fontsize=11)
    plt.ylabel('Índice', fontsize=11)
    plt.xticks(rotation=45)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()