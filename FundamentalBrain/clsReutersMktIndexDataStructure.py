# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 14:03:44 2018

@author: Carter
"""

import time
import datetime
import mechanicalsoup

import sys
sys.path.append('../')
from GeneralTools import clsDatabaseOper
from GeneralTools import clsGeneralConstants
from GeneralTools import clsGeneralMethods

class ReutersMktIndexDataStructure(object):
    #REUTERS_MKT_IDX_PAGE_NO_PARM = "?pn="
    REUTERS_MKT_IDX_PAGE_NO_PARM = "?sortBy=&sortDir=&pn="
    REUTERS_DATA_TABLE_CLASS = "dataTable sortable" 
    # raw: <div class="timestamp">Data as of&nbsp;Fri Feb 2, 2018 | 4:47pm EST.</div>
    REUTERS_AS_OF_DATE_TAG = "Data as of&nbsp;"
    REUTERS_AS_OF_DATE_END = "|"
    DATA_SOURCE = "Reuters"
    
    # Reuters market indcies constants
    REUTERS_IDX_DATA_RECORD_DATE_COL = 0
    REUTERS_IDX_TICKER_COL = 1
    REUTERS_IDX_RIC_COL = 2
    REUTERS_IDX_COMP_NAME_COL = 3
    REUTERS_IDX_LAST_PRICE_COL = 4
    REUTERS_IDX_LAST_CHG_COL = 5
    REUTERS_IDX_LAST_CHG_PERCENT_COL = 6
    REUTERS_IDX_LAST_VOL_COL = 7
    REUTERS_IDX_DATA_AS_OF_DATE_COL = 8
    
    def __init__(self, _reutersUrl=None, _ric=None):
#        self.generalMethods = clsGeneralMethods.GeneralMethods()
        self.reutersUrl = _reutersUrl
        self.dataRecordDate = time.strftime(clsGeneralConstants.GeneralConstants.DATA_RECORD_DATE_FORMAT)
        self.ric = _ric
        #index daily price
        self.prevClosePrice = 0 #can find from the previous record, more like double check
        self.openPrice = 0
        self.closePrice = 0
        self.dayHighPrice = 0
        self.dayLowPrice = 0
        # index composites
        self.size = 0
        self.name = ""
        self.asOfDate = time.strftime(clsGeneralConstants.GeneralConstants.DATA_RECORD_DATE_FORMAT)
        self.indexComposites = []
        self.reutersIdxPage = None
    #end: __init__
    
    def loadDataFromWeb(self, idxUrl):
        SAFE_GARD_SIZE = 10000
        LABEL_DATA_AS_OF_START = "Data as of"
        LABEL_DATA_AS_OF_END = "|"
        self.indexComposites = []
        
#        self.generalMethods.printLog("Reuters: self.ric = " + self.ric)
        
        # get the web page
        browser = mechanicalsoup.StatefulBrowser()
        browser.open(self.reutersUrl + idxUrl)
        self.reutersIdxPage = browser.get_current_page()
        
        # get index name
        compNameItem = self.reutersIdxPage.find("div", attrs={"id": "sectionTitle"}).find("h1")
        self.name = compNameItem.text.replace("\n", "").strip().split("  ")[-1]
        
        # get index daily price
        headerQuoteLabelItems = self.reutersIdxPage.findAll("div", attrs={"class": "label"})
        for headerQuoteLabelItem in headerQuoteLabelItems:
            if("price" == headerQuoteLabelItem.text.lower()):
                closePriceTxt = headerQuoteLabelItem.findNext("div").text
                if("--" != closePriceTxt):
                    self.closePrice = float(closePriceTxt.replace(",", ""))
                else:
                    self.closePrice = 0
            elif("open" == headerQuoteLabelItem.text.lower()):
                openPriceTxt = headerQuoteLabelItem.findNext("div").text
                if("--" != openPriceTxt):
                    self.openPrice = float(openPriceTxt.replace(",", ""))
                else:
                    self.openPrice = 0
            elif("prev close" == headerQuoteLabelItem.text.lower()):
                prevClosePriceTxt = headerQuoteLabelItem.findNext("div").text
                if("--" != prevClosePriceTxt):
                    self.prevClosePrice = float(prevClosePriceTxt.replace(",", ""))
                else:
                    self.prevClosePrice = 0

                
        idxInfoTblItems = self.reutersIdxPage.findAll("td", attrs={"class": "label"})
        for idxInfoTblItem in idxInfoTblItems:
            if("day's high" == idxInfoTblItem.text.lower()):
                dayHighPriceTxt = idxInfoTblItem.findNext("td").text
                if("--" != dayHighPriceTxt):
                    self.dayHighPrice = float(dayHighPriceTxt.replace(",", ""))
                else:
                    self.dayHighPrice = 0
#                self.dayHighPrice = float(idxInfoTblItem.findNext("td").text.replace(",", ""))
            elif("day's low" == idxInfoTblItem.text.lower()):
                dayLowPriceTxt = idxInfoTblItem.findNext("td").text
                if("--" != dayLowPriceTxt):
                    self.dayLowPrice = float(dayLowPriceTxt.replace(",", ""))
                else:
                    self.dayLowPrice = 0
                
        while( len(self.indexComposites) < SAFE_GARD_SIZE ) :
            # get the Data As Of Date
            if( 0 == len(self.indexComposites) ):
                asOfDateItem = self.reutersIdxPage.find("div", attrs={"class": "timestamp"})
                rawAsOfDateTxt = asOfDateItem.text.strip() #Data as of Fri Feb 2, 2018 | 4:47pm EST.
        
                dateStart = asOfDateItem.text.lower().find(LABEL_DATA_AS_OF_START.lower()) + len(LABEL_DATA_AS_OF_START)
                dateEnd = asOfDateItem.text.lower().find(LABEL_DATA_AS_OF_END.lower())
                rawAsOfDateTxt = rawAsOfDateTxt[dateStart:dateEnd].strip()
                try:
                    self.asOfDate = datetime.datetime.strptime(rawAsOfDateTxt, "%a %b %d, %Y")
                except ValueError as timeError:
                    self.asOfDate = datetime.datetime.now()

                # get the composites instrument header
                compoInstrTblItem = self.reutersIdxPage.find("table", attrs={"class": "dataTable sortable"})
                compoInstrRow = []
                compoInstrRow.append("Data_Record_Date")
                compoInstrRow.append("Ticker")
                compoInstrRow.append("RIC")
                tblHeaderItem = compoInstrTblItem.findAll("th")
                for tblHeader in tblHeaderItem:
                    compoInstrRow.append(tblHeader.text.strip())
                compoInstrRow.append("Date_As_Of_Date")
                self.indexComposites.append(compoInstrRow)

            # get the composites instrument data
            compoInstrTblItem = self.reutersIdxPage.find("table", attrs={"class": "dataTable sortable"})
            tblRowItem = compoInstrTblItem.findAll("tr")
            for tblRow in tblRowItem:
                compoInstrRow = []
                instrName = ""
                instrTicker = ""
                instrRic = ""
                compoInstrRow.append(self.dataRecordDate)
                tblCells = tblRow.findAll("td")
                for tblCell in tblCells:
                    instrLink = tblCell.find("a")
                    if(None != instrLink):
                        instrName = instrLink.text.strip()
                        instrTicker = instrLink.attrs["href"].split("/")[-1].split(".")[0]
                        instrRic = instrLink.attrs["href"].split("/")[-1]
                        compoInstrRow.append(instrTicker)
                        compoInstrRow.append(instrRic)
                        compoInstrRow.append(instrName)
                    else:
                        compoInstrRow.append(tblCell.text.strip())
                if(len(compoInstrRow) == 8):
                    compoInstrRow.append(self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_RECORD_DATE_FORMAT))
                    self.indexComposites.append(compoInstrRow)

            #get the next button
            pageNavItem = self.reutersIdxPage.find("div", attrs={"class": "pageNavigation"})
            nextButItem = pageNavItem.find('li', attrs={"class": "next"})
            if (None != nextButItem):
                nextLinkItem = nextButItem.find("a")
                browser.open(self.reutersUrl + nextLinkItem.attrs["href"])
                self.reutersIdxPage = browser.get_current_page()
            else:
                break
        return None
    #end: loadDataFromWeb

    def writeToCsv(self):
        outFilename = time.strftime("%Y%m%d_%H%M_") + (self.name.replace(" ", "_")) + ".csv"
        outMktIdxFile = open(outFilename, "w", encoding="utf8")
        outMktIdxFile.write(str(self.__str__()))
        outMktIdxFile.close()
    #end: writeToCsv
    
    def writeIndexStaticToDB(self):
        databaseOper = clsDatabaseOper.DatabaseOper()
        tableName = "tblIndexStatic"
        
        listOfKeyCols = ["IndexCode", "DataAsOfDate"]
        listOfKeyVals = [self.ric, self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_RECORD_DATE_FORMAT)]
        listOfInCols = ["Name", "Source"]
        listOfInVals = [self.name, self.DATA_SOURCE]
        databaseOper.insertIfNotExist(tableName, listOfKeyCols, listOfKeyVals, listOfInCols, listOfInVals)

        del databaseOper
        return None 
    #end: writeIndexStaticToDB
    
    def writeIndexDailyPriceToDB(self):
        databaseOper = clsDatabaseOper.DatabaseOper()
        tableName = "tblIndexDailyPrice"
        
        listOfKeyCols = ["IndexCode", "Source", "DataAsOfDate"]
        listOfKeyVals = [self.ric, self.DATA_SOURCE, self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_RECORD_DATE_FORMAT)]
        listOfInCols = ["OpenPrice", "ClosePrice", "DayHighPrice", "DayLowPrice", "PrevClosePrice"]
        listOfInVals = [self.openPrice, self.closePrice, self.dayHighPrice, self.dayLowPrice, self.prevClosePrice]
        databaseOper.insertIfNotExist(tableName, listOfKeyCols, listOfKeyVals, listOfInCols, listOfInVals)

        del databaseOper
        return None 
    #end: writeIndexDailyPriceToDB
    
    def setCompositesList(self, reutersIdxCompositeList):
        self.indexComposites = reutersIdxCompositeList
        return None
    #end: setCompositesList
    
    def getListOfComposites(self):
        return self.indexComposites
    #end: getListOfComposites
    
    def __len__(self):
        return len(self.indexComposites)
    #end: __len__
    
    def __str__(self, colSep=clsGeneralConstants.GeneralConstants.DEFAULT_COLUMN_SEP):
        """ print our Index Information and composite details at defined order
        """
        mktIdxStr = ""
        mktIdxStr += "Record_Date" + colSep + self.dataRecordDate + "\n"
#        mktIdxStr += "Ticker" + colSep + self.ticker + "\n"
        mktIdxStr += "RIC" + colSep + self.ric + "\n"
        mktIdxStr += "Index_Name" + colSep + self.name + "\n"
#        mktIdxStr += "Composites \n"
#        mktIdxStr += ("Record_Date" + colSep + "Company_Name" + colSep + "Ticker" + colSep + "RIC" + colSep + 
#                      "Last_Price" + colSep + "Last_Price_Change" + colSep + "Last_Price_Change_Percentage" + colSep + 
#                      "Last_Traded_Volume" + colSep + "Data_As_Of_Date" + colSep + "\n")
        
        for stock in self.indexComposites:
            mktIdxStr += (stock[self.REUTERS_IDX_DATA_RECORD_DATE_COL].replace(colSep, "") + colSep + 
                          stock[self.REUTERS_IDX_COMP_NAME_COL].replace(colSep, "")  + colSep + 
                          stock[self.REUTERS_IDX_COMP_TICKER_COL].replace(colSep, "")  + colSep + 
                          stock[self.REUTERS_IDX_COMP_RIC_COL].replace(colSep, "")  + colSep + 
                          stock[self.REUTERS_IDX_COMP_LAST_PRICE_COL].replace(colSep, "")  + colSep + 
                          stock[self.REUTERS_IDX_COMP_LAST_CHG_COL].replace(colSep, "")  + colSep + 
                          stock[self.REUTERS_IDX_COMP_LAST_CHG_PERCENT_COL].replace(colSep, "")  + colSep + 
                          stock[self.REUTERS_IDX_COMP_LAST_VOL_COL].replace(colSep, "")  + colSep + 
                          stock[self.REUTERS_IDX_DATA_AS_OF_DATE_COL].replace(colSep, "")  + "\n") 

        return mktIdxStr
    #end: __str__