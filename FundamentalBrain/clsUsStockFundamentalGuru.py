# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 15:02:02 2018

@author: Carter
"""
from GeneralTools import clsDatabaseOper
from GeneralTools import clsGeneralConstants
from GeneralTools import clsGeneralMethods
#from FundamentalBrain import clsReutersUsStockDataStructure

class UsStockFundamentalGuru(object):
    
    INSERT_POTENTIAL_SQL_FILE_PATH = "FundamentalBrain/FundamentalGuruSQL/INSERT_to_tblFundamentalGuru.sql"
    SOURCE_POTENTIAL_SQL_FILE_PATH = "FundamentalBrain/FundamentalGuruSQL/SOURCE_PotentialStocks.sql"
    MARK_POTENTIAL_SQL_FILE_PATH = "FundamentalBrain/FundamentalGuruSQL/MARK_PotentialStocks.sql"
    
    RETRIEVE_INIT_POTENTIAL_SQL_FILE_PATH = "FundamentalBrain/FundamentalGuruSQL/RETRIEVE_INIT_PotentialStocks.sql"
    
    
    FUNDAMENTAL_GURU_TABLE = "mytradeassistantdb.tblFundamentalGuru" #table contains potential stocks
    LIST_OF_FUNDAMENTAL_GURU_UPDATE_FIELD = ["StockTicker", "ListedExchCode", "IsLatest"]  
    
    def __init__(self):
        pass
    #end: __init__

    def retrievePotentialStocks(self):
        ''' Retrieve List of Potential Stock from DB. 
            First column is Stock Code; Second column is listed exchange code; Third column is company name.
        '''
        listOfPotentialStocks = []
        potentialSQL = ""
        generalMethods = clsGeneralMethods.GeneralMethods()
        potentialSQL = generalMethods.getSqlFromFile(self.RETRIEVE_INIT_POTENTIAL_SQL_FILE_PATH)
            
        if ("" != potentialSQL):
            databaseOper = clsDatabaseOper.DatabaseOper()
            listOfPotentialStocks = databaseOper.retrieveSelectMultiValuesSQL(potentialSQL)
            del databaseOper
        return listOfPotentialStocks
    #end: retrievePotentialStocks

    def setPotentialStocksAsRankBase(self):
        ''' Retrieve List of Potential Stock and insert to the Fundamental Guru table as ranking base.
        '''
        generalMethods = clsGeneralMethods.GeneralMethods()
        insertPotentialSQL = generalMethods.getSqlFromFile(self.INSERT_POTENTIAL_SQL_FILE_PATH)
        potentialSQL = generalMethods.getSqlFromFile(self.SOURCE_POTENTIAL_SQL_FILE_PATH)
        insertPotentialSQL = insertPotentialSQL.replace("<-potentialSQL->", potentialSQL)
        if ("" != insertPotentialSQL):
            databaseOper = clsDatabaseOper.DatabaseOper()
            databaseOper.insertSelectRecords(insertPotentialSQL)
            del databaseOper
        return None
    #end: setPotentialStocksAsRankBase
    
    def markPotentialStocks(self, sqlField, sqlSort, sqlNumOfItems, updateCol):
        ''' Rank Stocks by Revenues figures (EPS, ) from DB. 
            First column is Stock Code; Second column is listed exchange code; Third column is company name.
        '''
#        PLACEHOLDER_LIST = ["<-CheckFieldParam->", "<-SortParam->", "<-CheckItems->"]
#        SQL_VALUES_LIST = ["EpsRegressGrowth_Reuters", REVENUE_SQL_SORT, clsGeneralConstants.GeneralConstants.NUM_OF_ITEMS_TO_RANK]
        listOfMarkedStocks = []
        markSQL = ""

        generalMethods = clsGeneralMethods.GeneralMethods()
        markSQL = generalMethods.getSqlFromFile(self.MARK_POTENTIAL_SQL_FILE_PATH)
            
        if ("" != markSQL):
            #format the SQL
            markSQL = markSQL.replace("<-CheckFieldParam->", sqlField)
            markSQL = markSQL.replace("<-SortParam->", sqlSort)
            markSQL = markSQL.replace("<-CheckItems->", str(sqlNumOfItems))

            listOfPotentialStocks = []
            databaseOper = clsDatabaseOper.DatabaseOper()
            listOfPotentialStocks = databaseOper.retrieveSelectMultiValuesSQL(markSQL)
            del databaseOper
            
            listOfMarkedStocks = generalMethods.putRankingMarksToList(listOfPotentialStocks, sqlSort)
            
            for markedStock in listOfMarkedStocks:
                #databaseOper.updateSingleValue(self, tableName, updateCol, updateVal, listOfKeyCols, listOfKeyValues):
                listOfKeyValues = []
                listOfKeyValues.append(markedStock[0])
                listOfKeyValues.append(markedStock[1])
                listOfKeyValues.append(clsGeneralConstants.GeneralConstants.SQL_IS_LATEST_TRUE)
                updateVal = "{:10.6f}".format(markedStock[-1]).strip()
                databaseOper = clsDatabaseOper.DatabaseOper()
                databaseOper.updateSingleValue(self.FUNDAMENTAL_GURU_TABLE, updateCol, updateVal, self.LIST_OF_FUNDAMENTAL_GURU_UPDATE_FIELD, listOfKeyValues)
                del databaseOper
        return listOfMarkedStocks
    #end: markPotentialStocks