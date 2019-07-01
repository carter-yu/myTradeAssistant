# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 11:22:16 2018

@author: Carter
"""
#import time
import datetime
from GeneralTools import clsGeneralConstants

class GeneralMethods(object):
    
    def __init__(self):
        pass 
    
    def printLog(self, logRecord):
        LOG_FILE_PATH = clsGeneralConstants.GeneralConstants.LOG_FILE_PATH
        logLine = datetime.datetime.now().strftime(clsGeneralConstants.GeneralConstants.LOG_RECORD_DATE) + logRecord.strip()
        
        print(logLine)
        try:
            logFile = open(LOG_FILE_PATH,"a")
            logFile.write(logLine + "\n")
            logFile.close()
        except IOError:
            print("Could Not write to log file at: ", LOG_FILE_PATH)
        return None
    #end: printLog
    
    def isDate(self, possDateStr, dateFormat):
        """ Check if the input String matches with the date format string """
        isDate = False
        try:
            datetime.datetime.strptime(possDateStr, dateFormat)
            isDate = True
        except ValueError as valErr:
            isDate = False
#            print("value Error:", valErr)
        return isDate
    #end: isDate
    
    def tryParseDate(self, toDateTxt, dateFormat):
        """ Parse the input String to date object, bases on the date format provided. Return datetime.now if invalid. """
        newDate = datetime.datetime.now()
        if datetime.datetime == type(toDateTxt):
            newDate = toDateTxt
        else:
            try:
                newDate  = datetime.datetime.strptime(toDateTxt, dateFormat)
            except ValueError as timeError:
                newDate  = datetime.datetime.now()
        return newDate 
    #end: tryParseDate
    
    def tryParseFloat(self, toFloatTxt):
        """ Parse the input String to Float. Return 0 if invalid. """
        newFloat = 0 
        if ( (int == type(toFloatTxt)) or (float == type(toFloatTxt)) ):
            newFloat = toFloatTxt
        elif ( type(None) == type(toFloatTxt) ):
            newFloat = 0
        else:
            try:
                toFloatTxt = toFloatTxt.strip()
                toFloatTxt = toFloatTxt.replace(",", "")
                if ( (len(toFloatTxt) > 1) and ("%" == toFloatTxt[-1]) ):
                    toFloatTxt = toFloatTxt[0:-1]
                floatStartIdx = 0 
                while ( floatStartIdx < len(toFloatTxt) ) :
                    chkChar = toFloatTxt[floatStartIdx]
    #                print(floatStartIdx, ", chkChar=", chkChar, " chkChar.isdigit()=", chkChar.isdigit())
                    if ( not(chkChar.isdigit()) and ("-" != chkChar) ):
                        floatStartIdx += 1
                    else:
                        break;
    
                if ( len(toFloatTxt) < (floatStartIdx+1) ):
                    newFloat = 0
                else:
                    newFloat = float(toFloatTxt[floatStartIdx:])
            except (ZeroDivisionError, ValueError) as ex:
                newFloat = 0
        return newFloat
    #end: tryParseFloat
    
    def putRankingMarksToList(self, itemsToMark, sorting):
        """ Get a list of item with the last column is the figure for Rank
        """
        listWithRankMarks = []
        totalMarks = self.tryParseFloat(clsGeneralConstants.GeneralConstants.TOTAL_RANK_MARKS)
#        print("Number of items to Mark :", len(itemsToMark))
#        print(itemsToMark)
        
        numOfItemsToRank = len(itemsToMark)
        if (numOfItemsToRank > 1):
            nextItemIdx = 1
            totalDiff = 0
            anyFloatDiff = False
            itemsWithDiff = []
            for item in itemsToMark:
                if(nextItemIdx < numOfItemsToRank):
                    diffBetween = abs( self.tryParseFloat(item[-1]) - self.tryParseFloat(itemsToMark[nextItemIdx][-1]) )
                    if(diffBetween < 1):
                        anyFloatDiff = True
                    totalDiff += diffBetween
                    itemWithMark = list(item)
                    itemWithMark.append(diffBetween)
                    itemsWithDiff.append(itemWithMark)
                    nextItemIdx += 1
            
            if anyFloatDiff :
                totalDiff = 0 
                for item in itemsWithDiff:
                    item[-1] += 1
                    totalDiff += item[-1]

            marksPerDiff = totalMarks / totalDiff
            startMark = (numOfItemsToRank - 1)
            for item in itemsWithDiff:
                itemDiff = item[-1]
                item.append( startMark + (itemDiff * marksPerDiff) )
                listWithRankMarks.append(item)
                startMark -= 1

        return listWithRankMarks
    #end: getSqlFromFile
    
    def getSqlFromFile(self, filePath):
        strSql = ""
        
        try:
            potentialSQLfile = open(filePath,"r")
            
            for sqlLine in potentialSQLfile:
                sqlLine = sqlLine.strip()
                if( (len(sqlLine) > 0 ) and ("#" != sqlLine[0]) ):
                   otherHashPos = sqlLine.find("#")
                   if(-1 == otherHashPos):
                       strSql += sqlLine + " "
                   else:
                       strSql += sqlLine[0:otherHashPos]
    
            potentialSQLfile.close()
#            print(strSql)
        except IOError:
            print("Could Not read file at: ", filePath)
        
        if ( (";" != strSql[-1]) or (";\n" != strSql[-2:-1]) ):
            strSql += ";"
        strSql = strSql.replace(";", ";\n")
        return strSql
    #end: getSqlFromFile