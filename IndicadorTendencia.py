import yfinance as yf
import pandas as pd
import ta
import time

while True:
    # Obter dados históricos do par de moedas EUR/USD
    dados = yf.download("GBPUSD=X", period="1d", interval="5m")

    # Calcular a média móvel simples (SMA) de 5 períodos
    dados['SMA'] = dados['Close'].rolling(window=5).mean()

    # Calcular o indicador de Índice de Força Relativa (RSI)
    dados['RSI'] = ta.momentum.rsi(dados['Close'], window=14)

    # Calcular o indicador de Moving Average Convergence Divergence (MACD)
    dados['MACD'] = ta.trend.macd_diff(dados['Close'], window_slow=26, window_fast=12, window_sign=9)

    # Calcular o indicador de Bandas de Bollinger
    bb_bands = ta.volatility.BollingerBands(dados['Close'], window=20, window_dev=2)
    dados['BB_upper'] = bb_bands.bollinger_hband()
    dados['BB_lower'] = bb_bands.bollinger_lband()

    # Calcular o indicador de Média Móvel Exponencial (EMA)
    dados['EMA'] = ta.trend.ema_indicator(dados['Close'], window=20)

    # Calcular o indicador de Índice de Força Relativa Estocástico (Stochastic RSI)
    dados['StochRSI'] = ta.momentum.stochrsi(dados['Close'], window=14)

    # Calcular o indicador de Volume Médio
    dados['VolumeMA'] = dados['Volume'].rolling(window=10).mean()

    # Verificar a tendência com base na comparação entre os indicadores e os valores
    ultimo_preco = dados['Close'].iloc[-1]
    ultimo_sma = dados['SMA'].iloc[-1]
    ultimo_rsi = dados['RSI'].iloc[-1]
    ultimo_macd = dados['MACD'].iloc[-1]
    ultimo_bb_upper = dados['BB_upper'].iloc[-1]
    ultimo_bb_lower = dados['BB_lower'].iloc[-1]
    ultimo_ema = dados['EMA'].iloc[-1]
    ultimo_stoch_rsi = dados['StochRSI'].iloc[-1]
    ultimo_volume_ma = dados['VolumeMA'].iloc[-1]

    if (
        ultimo_preco > ultimo_sma and
        ultimo_rsi > 50 and
        ultimo_macd > 0 and
        ultimo_preco < ultimo_bb_upper and
        ultimo_preco > ultimo_ema and
        ultimo_stoch_rsi > 0.8 and
        ultimo_volume_ma > dados['Volume'].mean()
    ):
        tendencia = "Tendência de alta."
    elif (
        ultimo_preco < ultimo_sma and
        ultimo_rsi < 50 and
        ultimo_macd < 0 and
        ultimo_preco > ultimo_bb_lower and
        ultimo_preco < ultimo_ema and
        ultimo_stoch_rsi < 0.2 and
        ultimo_volume_ma < dados['Volume'].mean()
    ):
        tendencia = "Tendência de baixa."
    else:
        tendencia = "Não há tendência definida."

    # Imprimir a
    #tendência
    print(tendencia)
    time.sleep(5)