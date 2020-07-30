# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 09:14:27 2020

@author: angad
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd

tickers = ["MSFT","GOOG","AAPL"]
fin_info = {}

for ticker in tickers:
    temp = {}
    
    url="https://in.finance.yahoo.com/quote/"+ticker+"/financials?p="+ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content,"html.parser")
    tabl = soup.find_all("div",{"class":"D(tbrg)"})
    for t in tabl:
        rows = t.find_all("div",{"class":"rw-expnded"})
        for row in rows:
            if len(row.get_text('|').split('|')[0:2])>1:
                temp[row.get_text('|').split('|')[0]]=row.get_text('|').split('|')[1]
                
    url="https://in.finance.yahoo.com/quote/"+ticker+"/balance-sheet?p="+ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content,"html.parser")
    tabl = soup.find_all("div",{"class":"D(tbrg)"})
    for t in tabl:
        rows = t.find_all("div",{"class":"rw-expnded"})
        for row in rows:
            if len(row.get_text('|').split('|')[0:2])>1:
                temp[row.get_text('|').split('|')[0]]=row.get_text('|').split('|')[1] 
                
    url="https://in.finance.yahoo.com/quote/"+ticker+"/cash-flow?p="+ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content,"html.parser")
    tabl = soup.find_all("div",{"class":"D(tbrg)"})
    for t in tabl:
        rows = t.find_all("div",{"class":"rw-expnded"})
        for row in rows:
            if len(row.get_text('|').split('|')[0:2])>1:
                temp[row.get_text('|').split('|')[0]]=row.get_text('|').split('|')[1]
                
    url="https://in.finance.yahoo.com/quote/"+ticker+"/key-statistics?p="+ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content,"html.parser")
    tabl = soup.find_all("div",{"class":"Mstart(a) Mend(a)"})
    for t in tabl:
        rows = t.find_all("tr")
        for row in rows:
            if len(row.get_text('|').split('|')[0:2])>1:
                temp[row.get_text('|').split('|')[0]]=row.get_text('|').split('|')[-1]      
                
    fin_info[ticker]=temp   

combined_info = pd.DataFrame(fin_info)    
tickers = combined_info.columns
for ticker in tickers:
    combined_info = combined_info[~combined_info[ticker].str.contains("[a-z]").fillna(False)]