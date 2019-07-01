# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 15:02:02 2018

@author: Carter
"""
from FundamentalBrain import clsReutersUsStockDataStructure

class ReutersUsStockSourceOper(object):
    REUTERS_URL = "https://www.reuters.com"
    ### Reuters specific constants - for instruments
    REUTERS_INSTRUMENT_FINANCIALS = "/finance/stocks/financial-highlights/"
    
    def __init__(self):
#        self.reutersUsStockDataStructure = None
        self.clearDataStruct()
    #end: __init__
    
    def downloadFullUsStockData(self, usStockRic, belongToIndex):
        reutersUsStockUrl = self.REUTERS_URL + self.REUTERS_INSTRUMENT_FINANCIALS + usStockRic
        if None == self.reutersUsStockDataStructure :
            self.reutersUsStockDataStructure = clsReutersUsStockDataStructure.ReutersUsStockDataStructure(reutersUsStockUrl, usStockRic)
        
        self.reutersUsStockDataStructure.getAllStockData()
        self.reutersUsStockDataStructure.writeAllStockData(belongToIndex)
        
        return None
    #end: getUsStockFinanical
    
#    def getDataTest(self, usStockRic):
#        reutersUsStockUrl = self.REUTERS_URL + self.REUTERS_INSTRUMENT_FINANCIALS + usStockRic
#        if None == self.reutersUsStockDataStructure :
#            self.reutersUsStockDataStructure = clsReutersUsStockDataStructure.ReutersUsStockDataStructure(reutersUsStockUrl, usStockRic)
#        self.reutersUsStockDataStructure.scrapeStockRevenue()
#        return None
    #end: getDailyDataTest
            
    def getCoreData(self, usStockRic):
        reutersUsStockUrl = self.REUTERS_URL + self.REUTERS_INSTRUMENT_FINANCIALS + usStockRic
        if None == self.reutersUsStockDataStructure :
            self.reutersUsStockDataStructure = clsReutersUsStockDataStructure.ReutersUsStockDataStructure(reutersUsStockUrl, usStockRic)
        
        self.reutersUsStockDataStructure.scrapeStockStaicAndDailyPrice()
        self.reutersUsStockDataStructure.scrapeStockValuation()
        self.reutersUsStockDataStructure.scrapeStockInstitutionalHolders()
        self.reutersUsStockDataStructure.scrapeStockRevenue()
        self.reutersUsStockDataStructure.scrapeStockFinancialStrength()
        self.reutersUsStockDataStructure.scrapeStockManagementEffectiveness()

        self.reutersUsStockDataStructure.writeUsStockFinanicalStrengthToDB()
        self.reutersUsStockDataStructure.writeUsStockManagementEffectivenessToDB()
        self.reutersUsStockDataStructure.writeUsStockClosePriceToDB()
        self.reutersUsStockDataStructure.writeUsStockValuationToDB()
        self.reutersUsStockDataStructure.writeStockInstitutionalHoldersToDB()
        self.reutersUsStockDataStructure.writeUsStockRevenueToDB()
        
        return None
    #end: getCoreData
    
    def getFullSetData(self, usStockRic, belongToIndex):
        reutersUsStockUrl = self.REUTERS_URL + self.REUTERS_INSTRUMENT_FINANCIALS + usStockRic
        if None == self.reutersUsStockDataStructure :
            self.reutersUsStockDataStructure = clsReutersUsStockDataStructure.ReutersUsStockDataStructure(reutersUsStockUrl, usStockRic)
        
        self.getCoreData(usStockRic)
        self.reutersUsStockDataStructure.writeUsStockStaticToDB(belongToIndex)
        
        return None
    #end: getFullSetData
    
    def clearDataStruct(self):
        self.reutersUsStockDataStructure = None
        return None
    #end: clearDataStruct
    
    def callGuru(self, usStockRic):
        return None
    #end: callGuru
    