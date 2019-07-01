# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 18:04:56 2018

@author: Carter
"""

import mysql.connector
from mysql.connector import errorcode

from GeneralTools import clsGeneralMethods

class DatabaseOper(object):
    
    def __init__(self):
        self.generalMethods = clsGeneralMethods.GeneralMethods()
        
        self.USER = "carter"
        self.PASSWORD = "98118241"
        self.HOST = "127.0.0.1"
        self.PORT = "8241"
        self.DATABASE = "myTradeAssistantDB"
        
        self.dbConn = None
        self.cursor = None
        try:

            self.dbConn = mysql.connector.connect(user=self.USER, password=self.PASSWORD,
                                                  host=self.HOST, port=self.PORT, database=self.DATABASE)
            self.cursor = self.dbConn.cursor()
        except mysql.connector.Error as dbErr:
            if dbErr.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.generalMethods.printLog("Something is wrong with your user name or password")
            elif dbErr.errno == errorcode.ER_BAD_DB_ERROR:
                self.generalMethods.printLog("Database does not exist")
            else:
                self.generalMethods.printLog("DatabaseOper.__init__() >>> " + str( dbErr ))
#        finally:
            ## finally
    #end: __init__

    def __del__(self):
        if (None != self.dbConn):
            self.dbConn.close()
#            self.generalMethods.printLog("Destructor: Close DB connection")
    #end: __del__
    
    def retrieveSelectSingleValue(self, tableName, selectCol, listOfKeyCols, listOfKeyValues):
        retrievedValue = "" 
        if (len(listOfKeyCols) == len(listOfKeyValues)):
            selectStatement = "SELECT " + selectCol + " FROM " + tableName + " WHERE "
            for listIdx in range(0, len(listOfKeyCols)):
                selectStatement += listOfKeyCols[listIdx] + " = '" + str(listOfKeyValues[listIdx]) + "' AND "
            selectStatement = selectStatement[:-4]
#            
#            if (LimitRow.isdigit()):
#                selectStatement += "LIMIT " + str(LimitRow)
                
            selectStatement += "; "
#            self.generalMethods.printLog("selectStatement = ", selectStatement)
            try:
                self.cursor.execute(selectStatement)
                selectResult = self.cursor.fetchone()
                if None == selectResult:
                    retrievedValue = ""
                else:
                    retrievedValue = str(selectResult[0])
                self.cursor.close()
            except mysql.connector.Error as dbErr:
                self.generalMethods.printLog("DatabaseOper.retrieveSelectSingleValue(SQL:" + selectStatement + ") >>> " + str( dbErr ))
                
        return retrievedValue
    #end: retrieveSelectSingleValue
    
    def retrieveSelectMultiValues(self, tableName, selectCols, listOfKeyCols, listOfKeyValues):
        retrievedValues = "" 
        if (len(listOfKeyCols) == len(listOfKeyValues)):
            selectStatement = "SELECT " 
            for selectCol in selectCols:
                selectStatement +=  selectCol + ", "
            selectStatement = selectStatement[:-2]
            selectStatement +=  " FROM " + tableName + " WHERE "
            for listIdx in range(0, len(listOfKeyCols)):
                selectStatement += listOfKeyCols[listIdx] + " = '" + str(listOfKeyValues[listIdx]) + "' AND "
            selectStatement = selectStatement[:-4]
            selectStatement += "; "
#            self.generalMethods.printLog("selectStatement = " + selectStatement)
            try:
                self.cursor.execute(selectStatement)
                selectResult = list(self.cursor)
                if 0 == len(selectResult):
                    retrievedValues = ""
                else:
                    retrievedValues = selectResult[0]
                self.cursor.close()
            except mysql.connector.Error as dbErr:
                self.generalMethods.printLog("DatabaseOper.retrieveSelectMultiValues(SQL:" + selectStatement + ") >>> " + str( dbErr ))
                
        return retrievedValues
    #end: retrieveSelectSingleValue
    
    def retrieveSelectMultiValuesSQL(self, selectStatement):
        selectResult = "" 
        selectStatement = selectStatement.strip()    
#            self.generalMethods.printLog("selectStatement = " + selectStatement)
        try:
            self.cursor.execute(selectStatement)
            selectResult = list(self.cursor)
            if 0 == len(selectResult):
                selectResult = ""
#            else:
#                retrievedValues = selectResult[0]
            self.cursor.close()
        except mysql.connector.Error as dbErr:
            self.generalMethods.printLog("DatabaseOper.retrieveSelectMultiValues(SQL:" + selectStatement + ") >>> " + str( dbErr ))
                
        return selectResult
    #end: retrieveSelectSingleValue
    
    def deleteRecord(self, tableName, listOfKeyCols, listOfKeyValues):
        ''' delete record if not exist: table name, List of Column, List of Values
        '''
        if (len(listOfKeyCols) == len(listOfKeyValues)):
            deleteStatement = "DELETE FROM " + tableName + " WHERE "
            for listIdx in range(0, len(listOfKeyCols)):
                deleteStatement += listOfKeyCols[listIdx] + " = '" + str(listOfKeyValues[listIdx]) + "' AND "
            deleteStatement = deleteStatement[:-4]
            deleteStatement += "; "
            
#            self.generalMethods.printLog("deleteStatement = " + deleteStatement)
            
        try:
            self.cursor.execute(deleteStatement)
            for dbOut in self.cursor:
                self.generalMethods.printLog(dbOut)
            self.dbConn.commit()
            self.cursor.close()
        except mysql.connector.Error as dbErr:
            self.generalMethods.printLog("DatabaseOper.deleteRecord(SQL:" + deleteStatement + ") >>> " + str( dbErr )) 
        return None
    #end: deleteRecord
    
    def updateSingleValue(self, tableName, updateCol, updateVal, listOfKeyCols, listOfKeyValues):
        retrievedValue = "" 
        if (len(listOfKeyCols) == len(listOfKeyValues)):
            updateStatement = "UPDATE " + tableName + " SET " + updateCol + " = '" + updateVal + "' WHERE "
            for listIdx in range(0, len(listOfKeyCols)):
                updateStatement += listOfKeyCols[listIdx] + " = '" + str(listOfKeyValues[listIdx]) + "' AND "
            updateStatement = updateStatement[:-4]
            updateStatement += "; "
#            self.generalMethods.printLog("updateStatement = " + updateStatement)
            
        try:
            self.cursor.execute(updateStatement)
            for dbOut in self.cursor:
                self.generalMethods.printLog(dbOut)
            self.dbConn.commit()
            self.cursor.close()
        except mysql.connector.Error as dbErr:
            self.generalMethods.printLog("DatabaseOper.updateSingleValue(SQL:" + updateStatement + ") >>> " + str( dbErr ))
                
        return retrievedValue
    #end: updateSingleValue
    
    def insertSelectRecords(self, insertSelectStatement):
        ''' execute the input SQL to Insert Selected records
        '''
#        self.generalMethods.printLog("insertSelectStatement =" + insertSelectStatement)
        try:
            for result in self.cursor.execute(insertSelectStatement, multi=True):
                for dbOut in self.cursor:
                    self.generalMethods.printLog(str(dbOut))
            self.dbConn.commit()
            self.cursor.close()
        except mysql.connector.Error as dbErr:
            self.generalMethods.printLog("DatabaseOper.insertSelectRecords(SQL:" + insertSelectStatement + ") >>> " + str( dbErr ))
        return None
    #end: insertSelectRecords
    
    def insertIfNotExist(self, tableName, listOfKeyCols, listOfKeyValues, listOfCols, listOfValues):
        ''' insert record if not exist: table name, List of Column, List of Values
        '''
        if (len(listOfKeyCols) == len(listOfKeyValues)):
            countExistStatement = "SELECT count(1) as rowCount FROM " + tableName + " WHERE "
            for listIdx in range(0, len(listOfKeyCols)):
                countExistStatement += listOfKeyCols[listIdx] + " = '" + str(listOfKeyValues[listIdx]) + "' AND "
            countExistStatement = countExistStatement[:-4]
            countExistStatement += "; "
            #self.generalMethods.printLog(countExistStatement)
            
            try:
                self.cursor.execute(countExistStatement)
                countResult = self.cursor.fetchone()
                rowCount = int(countResult[0])
                #self.generalMethods.printLog(countResult[0])
                if 0 == rowCount:
                    self.insertListOfData(tableName, (listOfKeyValues + listOfValues), (listOfKeyCols + listOfCols))
                self.cursor.close()
            except mysql.connector.Error as dbErr:
                self.generalMethods.printLog("DatabaseOper.insertIfNotExist( SQL:" + countExistStatement + ") >>> " + str( dbErr ))
            
        else:
            self.generalMethods.printLog("DatabaseOper.insertIfNotExist - Length of Key Columns and Key Values does Not match")
        return None 
    #end: insertIfNotExist
    
    def insertListOfData(self, tableName, listOfValues, listOfCols=None):
        ''' insert record: table name, List of Values, List of Column
        '''
        insertStatement = "INSERT INTO " + tableName + " "
        cols = ""
        vals = ""
        
        if None != listOfCols:
            cols = "("
            for col in listOfCols:
                cols += col + ", "
            cols = cols[:-2]
            cols += ")"
            
        vals = "("
        for val in listOfValues:
            #if( "NULL" != val):
            if(str == type(val)):
                if( (-1 != val.lower().find("null")) or (0 == len(val)) ):
                    vals += " NULL, "
                else:
                    vals += "'" + val + "', "
            else:
                vals += "'" + str(val) + "', "
        vals = vals[:-2]
        vals += ")"
            
        #INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...);
        #INSERT INTO table_name VALUES (value1, value2, value3, ...);
        insertStatement = "INSERT INTO " + tableName + cols + " VALUES " + vals + ";"
#        self.generalMethods.printLog("insertStatement = " + insertStatement)
        try:
            self.cursor.execute(insertStatement)
            for dbOut in self.cursor:
                self.generalMethods.printLog(str(dbOut))
            self.dbConn.commit()
            self.cursor.close()
        except mysql.connector.Error as dbErr:
            self.generalMethods.printLog("DatabaseOper.insertListOfData. (SQL: " + insertStatement + ") >>> " + str( dbErr ))
        return None
    #end: insertListOfData