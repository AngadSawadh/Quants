# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 20:16:03 2020

@author: angad
"""

import yfinance as yf
import numpy as np
import statsmodels.api as sn
msft = yf.download("MSFT",start="2019-07-27",end="2020-07-25")
df1 = msft.copy()
df2 = msft.copy()
df3 = msft.copy()

def MACD(data,fast_period=12,slow_period=26,signal_period=9,method="exponential"):
    
    if method=="exponential":
        data['MA_Fast'] = data['Adj Close'].ewm(span=fast_period,min_periods=fast_period).mean()
        data['MA_Slow'] = data['Adj Close'].ewm(span=slow_period,min_periods=slow_period).mean()
        data['MACD'] = data['MA_Fast']-data['MA_Slow']
        data['Signal'] = data['MACD'].ewm(span=signal_period,min_periods=signal_period).mean()
        data.dropna(inplace=True)
        data.drop(['MA_Fast','MA_Slow'],axis=1,inplace=True)
        return data
        
    elif method=="simple":
        data['MA_Fast'] = data['Adj Close'].rolling(window=fast_period,min_periods=fast_period).mean()
        data['MA_Slow'] = data['Adj Close'].rolling(window=slow_period,min_periods=slow_period).mean()
        data['MACD'] = data['MA_Fast']-data['MA_Slow']
        data['Signal'] = data['MACD'].rolling(window=signal_period,min_periods=signal_period).mean()
        data.dropna(inplace=True)
        data.drop(['MA_Fast','MA_Slow'],axis=1,inplace=True)
        return data
        
    else:
        print("Invalid Method")
        

def ATR(data,period,tr_methods="max",atr_method="simple"):
    
    data["H-L"] = abs(data["High"]-data['Low'])
    data["H-PC"] = abs(data["High"]-data['Adj Close'].shift(1))
    data["L-PC"] = abs(data["Low"]-data['Adj Close'].shift(1))
    data["TR"] = data[["H-L","H-PC","L-PC"]].max(axis=1,skipna=False)
    if atr_method=="simple":
        data["ATR"] = data['TR'].rolling(window=period,min_periods=period).mean()
        data.dropna(inplace=True)
        data.drop(["H-L","H-PC","L-PC","TR"],axis=1,inplace=True)
        return data
    elif atr_method=="exponential":
        data["ATR"] = data["TR"].ewm(span=period,min_periods=period).mean()
        data.dropna(inplace=True)
        data.drop(["H-L","H-PC","L-PC","TR"],axis=1,inplace=True)
        return data
    else:
        print("Invalid Method for ATR")
                  
def BollingerBands(data,period,std_multiplier=2):
    
    data["MA"] = data['Adj Close'].rolling(window=period,min_periods=period).mean()
    data["STD"] = std_multiplier*data['MA'].rolling(period).std()
    data["Band_Up"] = data["MA"] + data["STD"]
    data["Band_Down"] = data["MA"] - data["STD"]
    data["Band_Width"] = data["Band_Up"]-data["Band_Down"]
    data.dropna(inplace=True)
    data.drop(["STD"],axis=1,inplace=True)
    return data

def RSI(data,period):
    
    data["Diff"] = data["Adj Close"] - data["Adj Close"].shift(1)
    data["Gain"] = np.where(data["Diff"]>0,data["Diff"],0)
    data["Loss"] = np.where(data["Diff"]<0,abs(data["Diff"]),0)
    avg_gain = []
    avg_loss = []
    gain = data["Gain"].tolist()
    loss = data["Loss"].tolist()
    for i in range(len(data)):
        if i<period:
            avg_gain.append(np.nan)
            avg_loss.append(np.nan)
        elif i==period:
            avg_gain.append(data["Gain"].rolling(window=period).mean()[period])
            avg_loss.append(data['Loss'].rolling(window=period).mean()[period])
        else:
            avg_gain.append(((period-1)*avg_gain[i-1]+gain[i])/period)
            avg_loss.append(((period-1)*avg_loss[i-1]+loss[i])/period)
    
    data["Avg Gain"] = np.array(avg_gain)
    data["Avg Loss"] = np.array(avg_loss)
    data["RS"] = data["Avg Gain"]/data["Avg Loss"]
    data["RSI"] = (100-(100/(1+data["RS"])))
    data.dropna(inplace=True)
    data.drop(["Diff","Gain","Loss","Avg Gain","Avg Loss","RS"],axis=1,inplace=True)
    return data

def ADX(data,period):
    data["H-L"] = abs(data["High"]-data['Low'])
    data["H-PC"] = abs(data["High"]-data['Adj Close'].shift(1))
    data["L-PC"] = abs(data["Low"]-data['Adj Close'].shift(1))
    data["TR"] = data[["H-L","H-PC","L-PC"]].max(axis=1,skipna=False)
    data['DMplus'] = np.where((data['High']-data['High'].shift(1))>(data['Low'].shift(1)-data['Low']),data['High']-data['High'].shift(1),0)
    data['DMplus'] = np.where(data['DMplus']<0,0,data['DMplus'])
    data['DMminus'] = np.where((data['Low'].shift(1)-data['Low'])>(data['High']-data['High'].shift(1)),data['Low'].shift(1)-data['Low'],0)
    data['DMminus'] = np.where(data['DMminus']<0,0,data['DMminus'])
    TR = data["TR"].tolist()
    DMplus = data["DMplus"].tolist()
    DMminus = data["DMminus"].tolist()
    TRn = []
    DMnplus = []
    DMnminus = []
    for i in range(len(data)):
        if i<period:
            TRn.append(np.nan)
            DMnplus.append(np.nan)
            DMnminus.append(np.nan)
        elif i==period:
            TRn.append(data["TR"].rolling(window=period).sum()[period])
            DMnplus.append(data["DMplus"].rolling(window=period).sum()[period])
            DMnminus.append(data["DMminus"].rolling(window=period).sum()[period])
        else:
            TRn.append((TRn[i-1]-(TRn[i-1]/period)+TR[i]))
            DMnplus.append((DMnplus[i-1]-(DMnplus[i-1]/period)+DMplus[i]))
            DMnminus.append((DMnminus[i-1]-(DMnminus[i-1]/period)+DMminus[i]))
    
    data["TRn"] = np.array(TRn)
    data["DMnplus"] = np.array(DMnplus)
    data["DMnminus"] = np.array(DMnminus)
    data["DIplus"] = 100*data["DMnplus"]/data["TRn"] 
    data["DIminus"] = 100*data["DMnminus"]/data["TRn"]
    data["Sum"] = data["DIplus"]+data["DIminus"]
    data["Diff"] = abs(data["DIplus"]-data["DIminus"])
    data["DX"] = 100*data["Diff"]/data["Sum"]
    DX = data["DX"].tolist()
    ADX = []
    
    for i in range(len(data)):
        if i<2*period-1:
            ADX.append(np.nan)
        elif i==2*period-1:
            ADX.append(data["DX"][period:2*period].mean())
        else:
            ADX.append(((period-1)*ADX[i-1]+DX[i])/period)
    
    data["ADX"] = np.array(ADX)
    data.dropna(inplace=True)
    data.drop(["H-L","H-PC","L-PC","TR","DMplus","DMminus","TRn","DMnplus","DMnminus","DIplus","DIminus","Sum","Diff","DX"],axis=1,inplace=True)
    return data
  
def OBV(data):
    data["Direction"] = np.where(data["Adj Close"]-data["Adj Close"].shift(1)>=0,1,-1)
    data["Direction"][0] = 0
    data["Sum"] = data["Direction"]*data["Volume"]
    data["OBV"] = data["Sum"].cumsum()
    data.dropna(inplace=True)
    data.drop(["Direction","Sum"],axis=1,inplace=True)
    return data

def slope(data,period):
    data1 = data["Adj Close"]
    m = np.empty(len(data1))
    angle = np.empty(len(data1))
    m[0:period-1] = 0
    for i in range(period-1,len(data1)):
        Y = data1[i-period+1:i+1]
        X = np.array(range(period))
        Y_scaled = (Y - Y.min())/(Y.max()-Y.min())
        X_scaled = (X -X.min())/(X.max()-X.min())
        X_scaled = sn.add_constant(X_scaled)
        model = sn.OLS(Y_scaled,X_scaled)
        results = model.fit()
        m[i] = (results.params[-1])  
    angle = np.rad2deg(np.arctan(m))
    data["Angles"] = angle
    return data

def RENKO():
    
        