from __future__ import annotations
import datetime
from time import time
from tkinter import E
import json
import pandas as pd

def connect_binance():
    """Connect to binance and return the client"""
    import binance
    from binance.client import Client
    #import credentaials from credentials.json
    with open ("credentials.json", "r") as f:
        credentials = json.load(f)
    api_key = credentials["api_key"]
    api_secret = credentials["api_secret"]
    client = Client(api_key, api_secret)
    return client

def get_klines(client, symbol, interval, start_str, end_str):
    """Get klines from binance and return the data"""
    klines = client.get_historical_klines(symbol, interval, start_str, end_str)
    return klines

def get_data():
    """Get data from binance and save it to a csv file"""
    client = connect_binance()
    symbol = "BTCUSDT"
    interval = client.KLINE_INTERVAL_4HOUR
    start_str = "1 Jan, 2021"
    end_str = "1 Feb, 2023"
    start = datetime.datetime.strptime(start_str, "%d %b, %Y")
    end = datetime.datetime.strptime(end_str, "%d %b, %Y")
    #get klines
    klines = get_klines(client, symbol, interval, start_str, end_str)
    #Create a dataframe
    df = pd.DataFrame(klines, columns = ["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
    #Convert the time to datetime
    df["Open time"] = pd.to_datetime(df["Open time"], unit = "ms")
    df["Close time"] = pd.to_datetime(df["Close time"], unit = "ms")
    #Save the data to a csv file
    #FORMAT: data/data<timeframe>_<start_date>_<end_date>.csv
    df.to_csv("data/data4H_01_01_21_01_02_23.csv", index = False)
    #Return the dataframe
    print("Data saved to data/data4H_01_01_21_01_02_23.csv")
    return df

def add_simple_indicators(df):
    """Add indicators to the df"""
    #MA
    for i in range(2, 20):
        df[f"MA{i}"] = df["Close"].rolling(window = i).mean()
    #EMA
    for i in range(2, 20):
        df[f"EMA{i}"] = df["Close"].ewm(span = i, adjust = False).mean()
    #MACD
    df["MACD"] = df["Close"].ewm(span = 12, adjust = False).mean() - df["Close"].ewm(span = 26, adjust = False).mean()
    df["Signal"] = df["MACD"].ewm(span = 9, adjust = False).mean()
    #Bollinger Bands
    df["MA20"] = df["Close"].rolling(window = 20).mean()
    df["STD20"] = df["Close"].rolling(window = 20).std()
    df["Upper Band"] = df["MA20"] + (df["STD20"] * 2)
    df["Lower Band"] = df["MA20"] - (df["STD20"] * 2)
    return df

def save_csv(df):
    #FORMAT: data/data<timeframe>_<start_date>_<end_date>.csv
    df.to_csv("data/data12H_01_01_21_01_02_21.csv", index = False)

def normalise_data(df):
    df['Open'] = df['Open'].diff() # get the difference between the current and previous row
    df['Open'] = df['Open'] / df['Open'].max() # normalise the data
    df['High'] = df['High'].diff()
    df['High'] = df['High'] / df['High'].max()
    df['Low'] = df['Low'].diff()
    df['Low'] = df['Low'] / df['Low'].max()
    df['Close'] = df['Close'].diff()
    df['Close'] = df['Close'] / df['Close'].max()
    df['Volume'] = df['Volume'].diff()
    df['Volume'] = df['Volume'] / df['Volume'].max()
    df['Quote asset volume'] = df['Quote asset volume'].diff()
    df['Quote asset volume'] = df['Quote asset volume'] / df['Quote asset volume'].max()
    df['Number of trades'] = df['Number of trades'].diff()
    df['Number of trades'] = df['Number of trades'] / df['Number of trades'].max()
    df['Taker buy base asset volume'] = df['Taker buy base asset volume'].diff()
    df['Taker buy base asset volume'] = df['Taker buy base asset volume'] / df['Taker buy base asset volume'].max()
    df['Taker buy quote asset volume'] = df['Taker buy quote asset volume'].diff()
    df['Taker buy quote asset volume'] = df['Taker buy quote asset volume'] / df['Taker buy quote asset volume'].max()
    for i in range(2, 20):
        df[f"MA{i}"] = df[f"MA{i}"].diff()
        df[f"MA{i}"] = df[f"MA{i}"] / df[f"MA{i}"].max()
    for i in range(2, 20):
        df[f"EMA{i}"] = df[f"EMA{i}"].diff()
        df[f"EMA{i}"] = df[f"EMA{i}"] / df[f"EMA{i}"].max()
    df["MACD"] = df["MACD"].diff()
    df["MACD"] = df["MACD"] / df["MACD"].max()
    df["Signal"] = df["Signal"].diff()
    df["Signal"] = df["Signal"] / df["Signal"].max()
    df["MA20"] = df["MA20"].diff()
    df["MA20"] = df["MA20"] / df["MA20"].max()
    df["STD20"] = df["STD20"].diff()
    df["STD20"] = df["STD20"] / df["STD20"].max()
    df["Upper Band"] = df["Upper Band"].diff()
    df["Upper Band"] = df["Upper Band"] / df["Upper Band"].max()
    df["Lower Band"] = df["Lower Band"].diff()
    df["Lower Band"] = df["Lower Band"] / df["Lower Band"].max()
    df["RSI"] = df["RSI"].diff()
    df["RSI"] = df["RSI"] / df["RSI"].max()
    df["Stochastic Oscillator"] = df["Stochastic Oscillator"].diff()
    df["Stochastic Oscillator"] = df["Stochastic Oscillator"] / df["Stochastic Oscillator"].max()
    df["Williams %R"] = df["Williams %R"].diff()
    df["Williams %R"] = df["Williams %R"] / df["Williams %R"].max()
    df["Upper Band"] = df["Upper Band"].diff()
    df["Upper Band"] = df["Upper Band"] / df["Upper Band"].max()
    df["Lower Band"] = df["Lower Band"].diff()
    df["Lower Band"] = df["Lower Band"] / df["Lower Band"].max()
    return df

def change_to_num_simple(df):
    df['Open'] = pd.to_numeric(df['Open'])
    df['High'] = pd.to_numeric(df['High'])
    df['Low'] = pd.to_numeric(df['Low'])
    df['Close'] = pd.to_numeric(df['Close'])
    df['Volume'] = pd.to_numeric(df['Volume'])
    df['Quote asset volume'] = pd.to_numeric(df['Quote asset volume'])
    df['Number of trades'] = pd.to_numeric(df['Number of trades'])
    df['Taker buy base asset volume'] = pd.to_numeric(df['Taker buy base asset volume'])
    df['Taker buy quote asset volume'] = pd.to_numeric(df['Taker buy quote asset volume'])
    for i in range(2, 20):
        df[f"MA{i}"] = pd.to_numeric(df[f"MA{i}"])
    for i in range(2, 20):
        df[f"EMA{i}"] = pd.to_numeric(df[f"EMA{i}"])
    df["MACD"] = pd.to_numeric(df["MACD"])
    df["Signal"] = pd.to_numeric(df["Signal"])
    df["MA20"] = pd.to_numeric(df["MA20"])
    df["STD20"] = pd.to_numeric(df["STD20"])
    df["Upper Band"] = pd.to_numeric(df["Upper Band"])
    df["Lower Band"] = pd.to_numeric(df["Lower Band"])
    return df

def add_complicated_indicators(df):
    #RSI
    df["RSI"] = df["Close"].diff().apply(lambda x: x if x > 0 else 0).rolling(window = 14).mean() / df["Close"].diff().apply(lambda x: x if x < 0 else 0).rolling(window = 14).mean()
    #Stochastic Oscillator
    df["Stochastic Oscillator"] = (df["Close"] - df["Low"].rolling(window = 14).min()) / (df["High"].rolling(window = 14).max() - df["Low"].rolling(window = 14).min())
    #Williams %R
    df["Williams %R"] = (df["High"].rolling(window = 14).max() - df["Close"]) / (df["High"].rolling(window = 14).max() - df["Low"].rolling(window = 14).min())
    #Bollinger Bands
    df["STD20"] = df["Close"].rolling(window = 20).std()
    df["MA20"] = df["Close"].rolling(window = 20).mean()
    df["Upper Band"] = df["MA20"] + (df["STD20"] * 2)
    df["Lower Band"] = df["MA20"] - (df["STD20"] * 2)
    return df

def get_dataset():
    df = get_data()
    df = df.drop(columns = ["Open time"])
    df = add_simple_indicators(df)
    df = change_to_num_simple(df)
    df = add_complicated_indicators(df)
    df = normalise_data(df)
    df = df.drop(columns = ["Ignore"])
    return df