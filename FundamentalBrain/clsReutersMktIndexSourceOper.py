# -*- coding: utf-8 -*-
"""
Operator class to get data from web source like SFC, Reuters, etc.

Created on Sat Feb  3 15:04:59 2018

@author: Carter
"""

from FundamentalBrain import clsReutersMktIndexDataStructure

class ReutersMktIndexSourceOper(object):
    REUTERS_URL = "https://www.reuters.com"
    ### Reuters specific constants - for Market Indices
    REUTERS_MKT_IDX = "/finance/markets/index/"
    
    DOW_JONES_RIC = ".DJI"
    #DOW_JONES_SIZE = 30 
    #REUTERS_DJI_URL = REUTERS_URL + REUTERS_MKT_IDX+ DOW_JONES_RIC
    NASDAQ_RIC = ".IXIC"
    #NASDAQ_SIZE = 3000 #85 pages
    #REUTERS_NASDAQ_URL = REUTERS_URL + REUTERS_MKT_IDX + NASDAQ_RIC
    STAND_AND_POOR_RIC = ".SPX"
    #STAND_AND_POOR_SIZE = 500 #17 pages
    #REUTERS_StandAndPoor_URL = REUTERS_URL + REUTERS_MKT_IDX + StandAndPoor_RIC
    HANG_SENG_RIC = ".HSI"
    #HANG_SENG_SIZE = 2000
    #REUTERS_HANG_SENG_URL = REUTERS_URL + REUTERS_MKT_IDX + HANG_SENG_RIC
    IBEX_RIC = ".IBEX"
    #IBEX_SIZE = 40
    #REUTERS_IBEX_URL = REUTERS_URL + REUTERS_MKT_IDX + IBEX_RIC
    # raw: GS.N
#    REUTERS_TICKER_SEP = "."


    def __init__(self):
        pass
    
    def getReutersStandAndPoorComposites(self):
        reutersStandAndPoorUrl = self.REUTERS_MKT_IDX + self.STAND_AND_POOR_RIC
        
        reutersMktIndexDataStructure = clsReutersMktIndexDataStructure.ReutersMktIndexDataStructure(self.REUTERS_URL, self.STAND_AND_POOR_RIC)
        reutersMktIndexDataStructure.loadDataFromWeb(reutersStandAndPoorUrl)
        
        return reutersMktIndexDataStructure
    #end: getReutersDowJonesStocks
    
    def getReutersNasdaqComposites(self):
        reutersNasdaqUrl = self.REUTERS_MKT_IDX + self.NASDAQ_RIC
        
        reutersMktIndexDataStructure = clsReutersMktIndexDataStructure.ReutersMktIndexDataStructure(self.REUTERS_URL, self.NASDAQ_RIC)
        reutersMktIndexDataStructure.loadDataFromWeb(reutersNasdaqUrl)
        
        return reutersMktIndexDataStructure
    #end: getReutersDowJonesStocks
    
    def getReutersDowJonesComposites(self):
        reutersDjiUrl = self.REUTERS_MKT_IDX + self.DOW_JONES_RIC
        
        reutersMktIndexDataStructure = clsReutersMktIndexDataStructure.ReutersMktIndexDataStructure(self.REUTERS_URL, self.DOW_JONES_RIC)
        reutersMktIndexDataStructure.loadDataFromWeb(reutersDjiUrl)
        
        return reutersMktIndexDataStructure
    #end: getReutersDowJonesStocks
    
    def getReutersHangSengIndexComposites(self):
        reutersHsiUrl = self.REUTERS_MKT_IDX + self.HANG_SENG_RIC
        
        reutersMktIndexDataStructure = clsReutersMktIndexDataStructure.ReutersMktIndexDataStructure(self.REUTERS_URL, self.HANG_SENG_RIC)
        reutersMktIndexDataStructure.loadDataFromWeb(reutersHsiUrl)
        
        return reutersMktIndexDataStructure
    #end: getReutersHangSengIndexComposites
    
    def getReutersIbexComposites(self):
        reutersIbexUrl = self.REUTERS_MKT_IDX + self.IBEX_RIC
        
        reutersMktIndexDataStructure = clsReutersMktIndexDataStructure.ReutersMktIndexDataStructure(self.REUTERS_URL, self.IBEX_RIC)
        reutersMktIndexDataStructure.loadDataFromWeb(reutersIbexUrl)
        
        return reutersMktIndexDataStructure
    #end: getReutersHangSengIndexComposites