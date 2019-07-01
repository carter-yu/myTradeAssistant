# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 13:27:35 2018

@author: Carter
"""
from StreetBrain import clsGoogleStockNewsDataStructure

class GoogleStockNewsOper(object):
    GOOGLE_URL = "https://news.google.com/news/explore/section/q/{exchangeName}:{stockTicker}/{exchangeName}:{stockTicker}?ned=us&gl=US&hl=en"
        
    def __init__(self):
        pass
    
    def getUsStockNewsDataStruct(self, stockTicker, exchangeCode):
        exchangeName = ""
        
        if 'IXIC' == exchangeCode.upper():
            exchangeName = "NASDAQ"
        else:
            exchangeName = "NYSE"
        
        googleStockNewsUrl = self.GOOGLE_URL.replace("{exchangeName}", exchangeName)
        googleStockNewsUrl = googleStockNewsUrl.replace("{stockTicker}", stockTicker)
#        print("googleStockNewsUrl = ", googleStockNewsUrl)
        
        googleStockNewsDataStructure = clsGoogleStockNewsDataStructure.GoogleStockNewsDataStructure(stockTicker, exchangeCode)
        googleStockNewsDataStructure.loadDataFromWeb(googleStockNewsUrl)
        
        return googleStockNewsDataStructure
    #end: getUsStockNews
    