import os
import pandas as pd

def clean_currency(val):
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)

    val_str = str(val).replace('R$', '').strip()

    if '.' in val_str and ',' in val_str:
        val_str = val_str.replace('.', '').replace(',', '.')
    elif ',' in val_str and '.' not in val_str:
        val_str = val_str.replace(',', '.')
    elif val_str.count('.') > 1 or (
        val_str.count('.') == 1 and len(val_str.split('.')[1]) == 3
    ):
        val_str = val_str.replace('.', '')

    try:
        return float(val_str)
    except ValueError:
        return 0.0

def load_and_clean_data(filepath='data/raw_field_data.csv'):
    if not os.path.exists(filepath):
        print(f"Arquivo não encontrado em {filepath}")
        return None

    df = pd.read_csv(filepath, sep=';', engine='python', on_bad_lines='skip')

    df['PV_Clean'] = df['PV_Planejado'].apply(clean_currency)
    df['EV_Clean'] = df['EV_Agregado'].apply(clean_currency)
    df['AC_Clean'] = df['AC_Custo_Real'].apply(clean_currency)

    df['Data_Ref'] = pd.to_datetime(
        df['Data_Ref'].str.replace('-', '/'), format='%d/%m/%Y', errors='coerce'
    )

    return df