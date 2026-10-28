import pandas as pd
from sklearn.linear_model import LogisticRegression

def train_and_predict_risk(df):
    """ 
    Minha ideia aqui foi treinar um modelo de classificacao binaria para calcular
    a probabilidade de um projeto se tornar crítico com base no CPI e SPI
    """

    df_ml = df.copy()

    df_ml['Target_Critico'] = df_ml['Status_Risco'].apply(lambda x: 1 if "CRÍTICO" in str(x) else 0)

    X = df_ml[['CPI', 'SPI']]
    y = df_ml['Target_Critico']

    model = LogisticRegression()
    model.fit(X, y)

    df_latest = df_ml.sort_values('Data_Ref').groupby('ID_Proj').tail(1).copy()
    X_latest = df_latest[['CPI', 'SPI']]
    
    probs = model.predict_proba(X_latest)[:, 1]
    df_latest['Prob_Critico_Futuro'] = (probs * 100).round(2) 

    df_latest['Alerta_Preditivo_IA'] = df_latest['Prob_Critico_Futuro'].apply(
        lambda p: '🔴 ALTA PROBABILIDADE DE RUPTURA' if p >= 65.0 else '🟢 RISCO PREDITIVO CONTROLADO'
    )

    return df_latest[[
        'ID_Proj', 
        'Nome_Projeto', 
        'CPI', 
        'SPI', 
        'Prob_Critico_Futuro', 
        'Alerta_Preditivo_IA' 
    ]]