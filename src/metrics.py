def calculate_evm_indices(df):
    df['CPI'] = df.apply(
        lambda row: row['EV_Clean'] / row['AC_Clean'] if row['AC_Clean'] > 0 else 0,
        axis=1,
    )
    df['SPI'] = df.apply(
        lambda row: row['EV_Clean'] / row['PV_Clean'] if row['PV_Clean'] > 0 else 0,
        axis=1,
    )
    return df

def classify_status(cpi, spi):
    if cpi < 0.9 or spi < 0.9:
        return '🔴 CRÍTICO (Ação Imediata)'
    elif cpi < 1.0 or spi < 1.0:
        return '🟡 ATENÇÃO (Desvio Leve)'
    else:
        return '🟢 SAUDÁVEL (No Prazo/Orçamento)'

def apply_risk_classification(df):
    df['Status_Risco'] = df.apply(
        lambda row: classify_status(row['CPI'], row['SPI']), axis=1
    )
    return df

def sort_temporal_data(df):
    df['ID_Proj'] = df['ID_Proj'].str.strip()
    return df.sort_values(by=['ID_Proj', 'Data_Ref'])