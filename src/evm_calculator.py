import os
import pandas as pd


def clean_currency(val):
  """Função para limpar valores monetários do campo

  (ex: '1.250.000,00', '980000', 'R$ 2.800.000,00') e converter para float.
  """
  if pd.isna(val):
    return 0.0
  # Se já for número, retorna float
  if isinstance(val, (int, float)):
    return float(val)

  # Remove 'R$', espaços em branco
  val_str = str(val).replace('R$', '').strip()

  # Se o formato for br com pontos e vírgula
  if '.' in val_str and ',' in val_str:
    val_str = val_str.replace('.', '').replace(',', '.')
  # Se tiver apenas vírgula decimal (ex: 980000,00)
  elif ',' in val_str and '.' not in val_str:
    val_str = val_str.replace(',', '.')
  # Se tiver apenas pontos
  elif val_str.count('.') > 1 or (
      val_str.count('.') == 1 and len(val_str.split('.')[1]) == 3
  ):
    val_str = val_str.replace('.', '')

  try:
    return float(val_str)
  except ValueError:
    return 0.0


def process_evm_data(filepath='data/raw_field_data.csv'):
  if not os.path.exists(filepath):
    print(f'Arquivo não encontrado em {filepath}')
    return None

  df = pd.read_csv(filepath, sep=';')
  print('DADOS BRUTOS CARREGADOS DO CAMPO')
  print(df.head(3))
  print('\n' + '=' * 50 + '\n')

  df['PV_Clean'] = df['PV_Planejado'].apply(clean_currency)
  df['EV_Clean'] = df['EV_Agregado'].apply(clean_currency)
  df['AC_Clean'] = df['AC_Custo_Real'].apply(clean_currency)

  df['Data_Ref'] = pd.to_datetime(
      df['Data_Ref'].str.replace('-', '/'), format='%d/%m/%Y', errors='coerce'
  )

  df['CPI'] = df.apply(
      lambda row: row['EV_Clean'] / row['AC_Clean']
      if row['AC_Clean'] > 0
      else 0,
      axis=1,
  )
  df['SPI'] = df.apply(
      lambda row: row['EV_Clean'] / row['PV_Clean']
      if row['PV_Clean'] > 0
      else 0,
      axis=1,
  )

  def classify_status(cpi, spi):
    if cpi < 0.9 or spi < 0.9:
      return '🔴 CRÍTICO (Ação Imediata)'
    elif cpi < 1.0 or spi < 1.0:
      return '🟡 ATENÇÃO (Desvio Leve)'
    else:
      return '🟢 SAUDÁVEL (No Prazo/Orçamento)'

  df['Status_Risco'] = df.apply(
      lambda row: classify_status(row['CPI'], row['SPI']), axis=1
  )

  return df


if __name__ == '__main__':
  resultado = process_evm_data()
  if resultado is not None:
    print('RESULTADOS PROCESSADOS E LIMPOS')
    print(
        resultado[[
            'ID_Proj',
            'Nome_Projeto',
            'CPI',
            'SPI',
            'Status_Risco',
            'Obs_Campo',
        ]].to_string(index=False)
    )