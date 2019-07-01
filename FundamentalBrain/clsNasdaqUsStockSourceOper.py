# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 15:02:02 2018

@author: Carter
"""

from FundamentalBrain import clsNasdaqUsStockDataStructure

class NasdaqUsStockSourceOper(object):
    
    ### Reuters specific constants - for instruments
#    REUTERS_INSTRUMENT_FINANCIALS = "/finance/stocks/financial-highlights/"
    
    def __init__(self):
        self.clearDataStruct()
    #end: __init__
    
    def getNasdaqStockDataStruct(self, stockTicker, exchangeCode):
        self.nasdaqUsStockDataStructure = clsNasdaqUsStockDataStructure.NasdaqUsStockDataStructure(stockTicker, exchangeCode)
        self.nasdaqUsStockDataStructure.loadDataFromWeb()
        
        return self.nasdaqUsStockDataStructure
    #end: getNasdaqStockDataStruct
    
    def getFullSetData(self, stockTicker, exchangeCode):
        if None == self.nasdaqUsStockDataStructure :
            self.nasdaqUsStockDataStructure = clsNasdaqUsStockDataStructure.NasdaqUsStockDataStructure(stockTicker, exchangeCode)
        
        self.nasdaqUsStockDataStructure.loadDataFromWeb()
        self.nasdaqUsStockDataStructure.writeUsStockHoldingInfoToDB()
        self.nasdaqUsStockDataStructure.writeUsStockRevenueToDB()
        self.nasdaqUsStockDataStructure.writeUsStockGuruAnalysisToDB()
        
        return None
    #end: getDailyData
    
    def clearDataStruct(self):
        self.nasdaqUsStockDataStructure = None
        return None
    #end: clearDataStruct