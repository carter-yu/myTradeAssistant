# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 10:48:59 2018

@author: Carter
"""

#import time
import datetime
import mechanicalsoup

import sys
sys.path.append('../')
from GeneralTools import clsDatabaseOper
from GeneralTools import clsGeneralConstants
from GeneralTools import clsGeneralMethods

class NasdaqUsStockDataStructure(object):
    NASDAQ_URL = "https://www.nasdaq.com/symbol/{stockTicker}/"
    #Stock Report
    NASDAQ_STOCK_REPORT_URL = "stock-report/"
    #Ownership summary
#    NASDAQ_OWNERSHIP_SUMMARY_URL = "ownership-summary/"
    #Institutional Holdings
    NASDAQ_INSTITUTIONAL_HOLDINGS_URL = "institutional-holdings/"
    #Insider Trades
    NASDAQ_INSIDER_TRADES_URL = "insider-trades/"
    #Earning Growth
    NASDAQ_EARNING_GROWTH_URL = "earnings-growth/"
    #Guru Analysis
    NASDAQ_GURU_ANALYSIS_URL = "guru-analysis/"

    DATA_SOURCE = "Nasdaq"
    NASDAQ_DATE_FORMAT = "%b. %d, %Y"

    def __init__(self, _stockTicker, _exchangeCode):
        self.generalMethods = clsGeneralMethods.GeneralMethods()
        
        self.compTicker = _stockTicker
        self.listedExchCode = _exchangeCode
        self.asOfDate = datetime.datetime.now()
        self.isSymbolValid = True
        self.stockNasdaqUrl = self.NASDAQ_URL.replace("{stockTicker}", self.compTicker.lower())
        #Stock Report
        self.sharesOutstanding = 0 
        #Institutional Holdings
#        self.totalInstitutionalSharsHeld = 0
#        self.totalInstitutionalNetActivity = 0
#        self.numberOfInstitHolderIncreasedPos = 0
#        self.numberOfSharesInstitHolderIncreased = 0
#        self.numberOfInstitHolderDecreasedPos = 0
#        self.numberOfSharesInstitHolderDecreased = 0
        self.numberOfInstitHolderHeldPos = 0
        self.sharesInstitHolderHeld = 0
        self.percentageHeldByInstit = 0
        
        self.numberOfInstitHolderBoughtNewPos = 0
        self.numberOfInstitHolderSoldOutPos = 0
        self.netNumberOfInstitHolderTradedOutPos = 0
        
        self.sharesInstitHolderBoughtNew = 0
        self.sharesInstitHolderSoldOut = 0
        self.netSharesInstitHolderTradedNew = 0
        #Insider Trades
        self.numberOfInsiderBoughtInThreeMonth = 0
        self.numberOfInsiderSoldInThreeMonth = 0
        self.netNumberOfInsiderHoldingInThreeMonth = 0
        self.numberOfInsiderBoughtInTwelveMonth = 0
        self.numberOfInsiderSoldInTwelveMonth = 0
        self.netNumberOfInsiderHoldingInTwelveMonth = 0
        
        self.sharesInsiderBoughtInThreeMonth = 0
        self.sharesInsiderSoldInThreeMonth = 0
        self.netSharesInsiderTradedInThreeMonth = 0
        self.sharesInsiderBoughtInTwelveMonth = 0
        self.sharesInsiderSoldInTwelveMonth = 0
        self.netSharesInsiderTradedInTwelveMonth = 0
        
        self.forecastEarningsGrowth = 0
        
        ## Guru Analysis
        self.guruPeterLynchVerdict = ""
        self.guruPeterLynchValue = 0
        self.guruBenjaminGarhamVerdict = ""
        self.guruBenjaminGarhamValue = 0
        self.guruPMomentumStrategyVerdict = ""
        self.guruPMomentumStrategyValue = 0  
        self.guruJamesOShaughnessyVerdict = ""
        self.guruJamesOShaughnessyValue = 0
        self.guruMotleyFoolVerdict = ""
        self.guruMotleyFoolValue = 0
        self.guruDavidDremanVerdict = ""
        self.guruDavidDremanValue = 0
        self.guruMartinZweigVerdict = ""
        self.guruMartinZweigValue = 0
        self.guruKennethFisherVerdict = ""
        self.guruKennethFisherValue = 0
        
    #end: __init__
    
    def loadDataFromWeb(self):
        #check symbole
        self.checkSymbol()
        #scrape the content
        self.generalMethods.printLog("Nasdaq: self.compTicker = " + self.compTicker + " , self.isSymbolValid = " + str( self.isSymbolValid ))
        if (self.isSymbolValid):
            self.scrapeStockReport()
            self.scrapeInstitutionalHoldings()
            self.scrapeInsiderTrades()
            self.scrapeEarningGrowth()
            self.scrapeGuruAnalysis()
            
            try:
                self.percentageHeldByInstit = self.sharesInstitHolderHeld / self.sharesOutstanding 
            except (ZeroDivisionError, ValueError) as ex:
                self.percentageHeldByInstit = 0

        return None
    #end: loadDataFromWeb
    
## Web Scrape
## Web Scrape
## Web Scrape    
    def checkSymbol(self):
        checkSymbolUrl = self.stockNasdaqUrl + self.NASDAQ_STOCK_REPORT_URL
        # get the web page
        browser = mechanicalsoup.StatefulBrowser()
        browser.open(checkSymbolUrl)
        checkSymbolPage = browser.get_current_page()
        
        allDivItems = checkSymbolPage.findAll("div")
        for divItem in allDivItems:
            divTxt = divItem.text.lower().strip()
            if(-1 != divTxt.find("it is an unknown symbol")):
                self.generalMethods.printLog("Invalid Symbol (" + self.compTicker + ") : It is an unknown symbol.")
                self.isSymbolValid = False
        return None
    #checkSymbol
    
    def scrapeStockReport(self):
        stockReportUrl = self.stockNasdaqUrl + self.NASDAQ_STOCK_REPORT_URL
        # get the web page
        browser = mechanicalsoup.StatefulBrowser()
        browser.open(stockReportUrl)
        stockReportPage = browser.get_current_page()
        stockReportHeaders = stockReportPage.findAll("h3")
        
        for stockReportHeader in stockReportHeaders:
            stockReportHeaderTxt = stockReportHeader.text.strip().lower()
            if("stock report details" == stockReportHeaderTxt):
                stockReportDetailTbl = stockReportHeader.findNext("table")
                stockReportDetailDataHeads = stockReportDetailTbl.findAll("th")
                for stockReportDetailDataHead in stockReportDetailDataHeads:
                    stockReportDetailDataHeadTxt = stockReportDetailDataHead.text.strip().lower()
                    if( "shares outstanding" == stockReportDetailDataHeadTxt ):
                        sharesOutstandingDataItem = stockReportDetailDataHead.findNext("td")
                        sharesOutstandingTxt = sharesOutstandingDataItem.text.strip().lower()
                        self.sharesOutstanding = self.generalMethods.tryParseFloat(sharesOutstandingTxt)
                        
        # get Data as of date
        dataAsOfTextItem = stockReportPage.find("span", attrs={"id": "qwidget_markettime"})
        if (None != dataAsOfTextItem):
            dataAsOfText = dataAsOfTextItem.text.strip().lower()
            
            try:
                self.asOfDate = datetime.datetime.strptime(dataAsOfText, self.NASDAQ_DATE_FORMAT)
            except ValueError as timeError:
                self.asOfDate = datetime.datetime.now()
        else:
            self.asOfDate = datetime.datetime.now()
    
        return None
    #end:scrapeStockReport

    def scrapeInstitutionalHoldings(self):
        institutionalHoldingsUrl = self.stockNasdaqUrl + self.NASDAQ_INSTITUTIONAL_HOLDINGS_URL
        # get the web page
        browser = mechanicalsoup.StatefulBrowser()
        browser.open(institutionalHoldingsUrl)
        institutionalHoldingsPage = browser.get_current_page()
        
        institutionalHoldingsHeaders = institutionalHoldingsPage.findAll("h4") 
        for institutionalHoldingsHeader in institutionalHoldingsHeaders:
            institutionalHoldingHeaderTxt = institutionalHoldingsHeader.text.strip().lower()
#            self.generalMethods.printLog("institutionalHoldingHeaderTxt = ", institutionalHoldingHeaderTxt)
            if("active positions" == institutionalHoldingHeaderTxt):
                activePosTbl = institutionalHoldingsHeader.findNext("table")
                activePosDataHeads = activePosTbl.findAll("th")
                for activePosDataHead in activePosDataHeads:
                    activePosDataHeadTxt = activePosDataHead.text.strip().lower()
#                    self.generalMethods.printLog("stockReportDetailDataHeadTxt =", stockReportDetailDataHeadTxt)
                    if( "total institutional shares" == activePosDataHeadTxt ):
                        activePosHolderDataItem = activePosDataHead.findNext("td")
                        numberOfInstitHolderHeldPosTxt = activePosHolderDataItem.text.strip().lower()
                        activePosSharesDataItem = activePosHolderDataItem.findNext("td")
                        sharesInstitHolderHeldTxt = activePosSharesDataItem.text.strip().lower()
                        self.numberOfInstitHolderHeldPos = self.generalMethods.tryParseFloat(numberOfInstitHolderHeldPosTxt)
                        self.sharesInstitHolderHeld = self.generalMethods.tryParseFloat(sharesInstitHolderHeldTxt)
                        
            if("new and sold out positions" == institutionalHoldingHeaderTxt):
                boughtAndSoldPosTbl = institutionalHoldingsHeader.findNext("table")
                boughtAndSoldPosDataHeads = boughtAndSoldPosTbl.findAll("th")
                for boughtAndSoldPosDataHead in boughtAndSoldPosDataHeads:
                    boughtAndSoldPosDataHeadTxt = boughtAndSoldPosDataHead.text.strip().lower()
                    if( "new positions" == boughtAndSoldPosDataHeadTxt ):
                        boughtAndSoldPosDataItem = boughtAndSoldPosDataHead.findNext("td")
                        numberOfHolderBoughtNewPosTxt = boughtAndSoldPosDataItem.text.strip().lower()
                        sharesHolderBoughtNewDataItem = boughtAndSoldPosDataItem.findNext("td")
                        sharesHolderBoughtNewTxt = sharesHolderBoughtNewDataItem.text.strip().lower()
                        self.numberOfInstitHolderBoughtNewPos = self.generalMethods.tryParseFloat(numberOfHolderBoughtNewPosTxt)
                        self.sharesInstitHolderBoughtNew = self.generalMethods.tryParseFloat(sharesHolderBoughtNewTxt)
                    elif( "sold out positions" == boughtAndSoldPosDataHeadTxt ):
                        boughtAndSoldPosDataItem = boughtAndSoldPosDataHead.findNext("td")
                        numberOfHolderBoughtNewPosTxt = boughtAndSoldPosDataItem.text.strip().lower()
                        sharesHolderBoughtNewDataItem = boughtAndSoldPosDataItem.findNext("td")
                        sharesHolderBoughtNewTxt = sharesHolderBoughtNewDataItem.text.strip().lower()
                        self.numberOfInstitHolderSoldOutPos = self.generalMethods.tryParseFloat(numberOfHolderBoughtNewPosTxt)
                        self.sharesInstitHolderSoldOut = self.generalMethods.tryParseFloat(sharesHolderBoughtNewTxt)
                        
        self.netNumberOfInstitHolderTradedOutPos = self.numberOfInstitHolderBoughtNewPos - self.numberOfInstitHolderSoldOutPos
        self.netSharesInstitHolderTradedNew = self.sharesInstitHolderBoughtNew - self.sharesInstitHolderSoldOut
        
        return None
    #end:scrapeInstitutionalHoldings
    
    def scrapeInsiderTrades(self):
        insiderTradesUrl = self.stockNasdaqUrl + self.NASDAQ_INSIDER_TRADES_URL
        # get the web page
        browser = mechanicalsoup.StatefulBrowser()
        browser.open(insiderTradesUrl)
        insiderTradesPage = browser.get_current_page()
        
        insiderTradesHeaders = insiderTradesPage.findAll("h2") 
        for insiderTradesHeader in insiderTradesHeaders:
            insiderTradesHeaderTxt = insiderTradesHeader.text.strip().lower()
            if("number of insider trades" == insiderTradesHeaderTxt):
                insiderTradesTbl = insiderTradesHeader.findNext("table")
                insiderTradesDataHeads = insiderTradesTbl.findAll("th")
                for insiderTradesDataHead in insiderTradesDataHeads:
                    insiderTradesDataHeadTxt = insiderTradesDataHead.text.strip().lower()
                    if( "# of open market buys" == insiderTradesDataHeadTxt ):
                        insiderTradesDataItem = insiderTradesDataHead.findNext("td")
                        insiderTrades3MTxt = insiderTradesDataItem.text.strip().lower()
                        insiderTrades3MDataItem = insiderTradesDataItem.findNext("td")
                        insiderTrades12MTxt = insiderTrades3MDataItem.text.strip().lower()
                        self.numberOfInsiderBoughtInThreeMonth = self.generalMethods.tryParseFloat(insiderTrades3MTxt)
                        self.numberOfInsiderBoughtInTwelveMonth = self.generalMethods.tryParseFloat(insiderTrades12MTxt)
                    elif( "# of sells" == insiderTradesDataHeadTxt ):
                        insiderTradesDataItem = insiderTradesDataHead.findNext("td")
                        insiderTrades3MTxt = insiderTradesDataItem.text.strip().lower()
                        insiderTrades3MDataItem = insiderTradesDataItem.findNext("td")
                        insiderTrades12MTxt = insiderTrades3MDataItem.text.strip().lower()
                        self.numberOfInsiderSoldInThreeMonth = self.generalMethods.tryParseFloat(insiderTrades3MTxt)
                        self.numberOfInsiderSoldInTwelveMonth = self.generalMethods.tryParseFloat(insiderTrades12MTxt)
            elif("number of insider shares traded" == insiderTradesHeaderTxt):
                insiderTradesTbl = insiderTradesHeader.findNext("table")
                insiderTradesDataHeads = insiderTradesTbl.findAll("th")
                for insiderTradesDataHead in insiderTradesDataHeads:
                    insiderTradesDataHeadTxt = insiderTradesDataHead.text.strip().lower()
                    if( "# of shares bought" == insiderTradesDataHeadTxt ):
                        insiderTradesDataItem = insiderTradesDataHead.findNext("td")
                        insiderTrades3MTxt = insiderTradesDataItem.text.strip().lower()
                        insiderTrades3MDataItem = insiderTradesDataItem.findNext("td")
                        insiderTrades12MTxt = insiderTrades3MDataItem.text.strip().lower()
                        self.sharesInsiderBoughtInThreeMonth = self.generalMethods.tryParseFloat(insiderTrades3MTxt)
                        self.sharesInsiderBoughtInTwelveMonth = self.generalMethods.tryParseFloat(insiderTrades12MTxt)
                    elif( "# of shares sold" == insiderTradesDataHeadTxt ):
                        insiderTradesDataItem = insiderTradesDataHead.findNext("td")
                        insiderTrades3MTxt = insiderTradesDataItem.text.strip().lower()
                        insiderTrades3MDataItem = insiderTradesDataItem.findNext("td")
                        insiderTrades12MTxt = insiderTrades3MDataItem.text.strip().lower()
                        self.sharesInsiderSoldInThreeMonth = self.generalMethods.tryParseFloat(insiderTrades3MTxt)
                        self.sharesInsiderSoldInTwelveMonth = self.generalMethods.tryParseFloat(insiderTrades12MTxt)
                        
        self.netNumberOfInsiderHoldingInThreeMonth = self.numberOfInsiderBoughtInThreeMonth - self.numberOfInsiderSoldInThreeMonth
        self.netNumberOfInsiderHoldingInTwelveMonth = self.numberOfInsiderBoughtInTwelveMonth - self.numberOfInsiderSoldInTwelveMonth
        
        self.netSharesInsiderTradedInThreeMonth = self.sharesInsiderBoughtInThreeMonth - self.sharesInsiderSoldInThreeMonth
        self.netSharesInsiderTradedInTwelveMonth = self.sharesInsiderBoughtInTwelveMonth - self.sharesInsiderSoldInTwelveMonth

        return None
    #end:scrapeInsiderTrades
    
    def scrapeEarningGrowth(self):
        earningGrowthUrl = self.stockNasdaqUrl + self.NASDAQ_EARNING_GROWTH_URL
        # get the web page
        browser = mechanicalsoup.StatefulBrowser()
        browser.open(earningGrowthUrl)
        earningGrowthPage = browser.get_current_page()
        
        earningGrowthHeaders = earningGrowthPage.findAll("h2") 
        for earningGrowthHeader in earningGrowthHeaders:
            earningGrowthHeaderTxt = earningGrowthHeader.text.strip().lower()
            if("forecast earnings growth" == earningGrowthHeaderTxt):
                forecastEarningsGrowthTxt = earningGrowthHeader.findNext("span").text.strip().lower()
                #Analysts expect earnings growth next year of 25.26% over this year's forecasted earnings.
                growthTxtStartTxt = "analysts expect earnings growth next year of "
                growthTxtStartPos = forecastEarningsGrowthTxt.find(growthTxtStartTxt ) 
                if(-1 != growthTxtStartPos):
                    growthTxtStartPos ++ len(growthTxtStartTxt)
                    growthTxtEndPos = forecastEarningsGrowthTxt.find("%", growthTxtStartPos)
                    
                    self.forecastEarningsGrowth = self.generalMethods.tryParseFloat(forecastEarningsGrowthTxt[growthTxtStartPos:growthTxtEndPos])

        return None
    #end:scrapeEarningGrowth
    
    def scrapeGuruAnalysis(self):
        guruAnalysisUrl = self.stockNasdaqUrl + self.NASDAQ_GURU_ANALYSIS_URL
#        self.generalMethods.printLog("earningGrowth=", analystResearchUrl)
        # get the web page
        browser = mechanicalsoup.StatefulBrowser()
        browser.open(guruAnalysisUrl)
        guruAnalysisPage = browser.get_current_page()
        
        guruAnalysisHeaders = guruAnalysisPage.findAll("h2") 
        for guruAnalysisHeader in guruAnalysisHeaders:
            guruAnalysisTxt = guruAnalysisHeader.text.strip().lower()
            if("p/e growth investor peter lynch" == guruAnalysisTxt):
                guruAnalysisResult = guruAnalysisHeader.findNext("p").text.strip()
                guruAnalysisResult = guruAnalysisResult.replace("'", "''")
                guruAnalysisValue = guruAnalysisHeader.findNext("b").text.strip()
                guruAnalysisValue = guruAnalysisValue.replace("%", "")
                self.guruPeterLynchVerdict = guruAnalysisResult
                self.guruPeterLynchValue = guruAnalysisValue  
            elif("value investor benjamin graham" == guruAnalysisTxt):
                guruAnalysisResult = guruAnalysisHeader.findNext("p").text.strip()
                guruAnalysisResult = guruAnalysisResult.replace("'", "''")
                guruAnalysisValue = guruAnalysisHeader.findNext("b").text.strip()
                guruAnalysisValue = guruAnalysisValue.replace("%", "")
                self.guruBenjaminGarhamVerdict = guruAnalysisResult
                self.guruBenjaminGarhamValue = guruAnalysisValue
            elif("momentum strategy investor validea" == guruAnalysisTxt):
                guruAnalysisResult = guruAnalysisHeader.findNext("p").text.strip()
                guruAnalysisResult = guruAnalysisResult.replace("'", "''")
                guruAnalysisValue = guruAnalysisHeader.findNext("b").text.strip()
                guruAnalysisValue = guruAnalysisValue.replace("%", "")
                self.guruPMomentumStrategyVerdict = guruAnalysisResult
                self.guruPMomentumStrategyValue = guruAnalysisValue
            elif("growth/value investor james o'shaughnessy" == guruAnalysisTxt):
                guruAnalysisResult = guruAnalysisHeader.findNext("p").text.strip()
                guruAnalysisResult = guruAnalysisResult.replace("'", "''")
                guruAnalysisValue = guruAnalysisHeader.findNext("b").text.strip()
                guruAnalysisValue = guruAnalysisValue.replace("%", "")
                self.guruJamesOShaughnessyVerdict = guruAnalysisResult
                self.guruJamesOShaughnessyValue = guruAnalysisValue
            elif("small cap growth investor motley fool" == guruAnalysisTxt):
                guruAnalysisResult = guruAnalysisHeader.findNext("p").text.strip()
                guruAnalysisResult = guruAnalysisResult.replace("'", "''")
                guruAnalysisValue = guruAnalysisHeader.findNext("b").text.strip()
                guruAnalysisValue = guruAnalysisValue.replace("%", "")
                self.guruMotleyFoolVerdict = guruAnalysisResult
                self.guruMotleyFoolValue = guruAnalysisValue
            elif("contrarian investor david dreman" == guruAnalysisTxt):
                guruAnalysisResult = guruAnalysisHeader.findNext("p").text.strip()
                guruAnalysisResult = guruAnalysisResult.replace("'", "''")
                guruAnalysisValue = guruAnalysisHeader.findNext("b").text.strip()
                guruAnalysisValue = guruAnalysisValue.replace("%", "")
                self.guruDavidDremanVerdict = guruAnalysisResult
                self.guruDavidDremanValue = guruAnalysisValue
            elif("growth/value investor martin zweig" == guruAnalysisTxt):
                guruAnalysisResult = guruAnalysisHeader.findNext("p").text.strip()
                guruAnalysisResult = guruAnalysisResult.replace("'", "''")
                guruAnalysisValue = guruAnalysisHeader.findNext("b").text.strip()
                guruAnalysisValue = guruAnalysisValue.replace("%", "")
                self.guruMartinZweigVerdict = guruAnalysisResult
                self.guruMartinZweigValue = guruAnalysisValue
            elif("price/sales investor kenneth fisher" == guruAnalysisTxt):
                guruAnalysisResult = guruAnalysisHeader.findNext("p").text.strip()
                guruAnalysisResult = guruAnalysisResult.replace("'", "''")
                guruAnalysisValue = guruAnalysisHeader.findNext("b").text.strip()
                guruAnalysisValue = guruAnalysisValue.replace("%", "")
                self.guruKennethFisherVerdict = guruAnalysisResult
                self.guruKennethFisherValue = guruAnalysisValue

        return None
    #end:scrapeGuruAnalysis

## Write to DB     
## Write to DB 
## Write to DB     
    def writeUsStockHoldingInfoToDB(self):
        stockShareHoldingTable = "tblStockDailySharesHolding"
        # 1. delete duplicate: del record with same Ticker, ListedExch, Source and DataAsOfDate
        databaseOper = clsDatabaseOper.DatabaseOper()
        listDelCols = ["StockTicker", "ListedExchCode", "Source", "DataAsOfDate"]
        listDelVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE, self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)]
        databaseOper.deleteRecord(stockShareHoldingTable, listDelCols, listDelVals)
        del databaseOper
            
        # 2. mark delete old: update IsLatest to 'N' with same Ticker, ListedExch and Source
        databaseOper = clsDatabaseOper.DatabaseOper()
        listUpdCols = ["StockTicker", "ListedExchCode", "Source"]
        listUpdVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE]
        databaseOper.updateSingleValue(stockShareHoldingTable, "IsLatest", "N", listUpdCols, listUpdVals)
        del databaseOper

        # 3. insert new record to DB
        databaseOper = clsDatabaseOper.DatabaseOper()
        listInstCols = ["StockTicker", "ListedExchCode", "Source", 
                        "SharesOutstanding", 
                        "TotalNumOfInstitutionalHolders", "TotalSharedHeldByInstitutions", "PercentageHeldByInstitutions",
                        "NumOfInstitutionsBoughtNewPosition", "NumOfInstitutionsSoldOutPosition", "NetNumOfInstitutionsTraded", 
                        "SharesBoughtByInstitutions", "SharesSoldByInstitutions", "NetSharesTradedByInstitutions", 
                        "NumOfInsidersBoughtIn3M", "NumOfInsidersSoldIn3M", "NetNumOfInsidersTradedIn3M", 
                        "SharesBoughtByInsidersIn3M", "SharesSoldByInsidersIn3M", "NetNumOfSharesTradedByInsidersIn3M", 
                        "NumOfInsidersBoughtIn12M", "NumOfInsidersSoldIn12M", "NetNumOfInsidersTradedIn12M", 
                        "SharesBoughtByInsidersIn12M", "SharesSoldByInsidersIn12M", "NetNumOfSharesTradedByInsidersIn12M", 
                        "DataAsOfDate"
                        ]

        listInstVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE, 
                        self.sharesOutstanding, 
                        self.numberOfInstitHolderHeldPos, self.sharesInstitHolderHeld, self.percentageHeldByInstit,
                        self.numberOfInstitHolderBoughtNewPos, self.numberOfInstitHolderSoldOutPos, self.netNumberOfInstitHolderTradedOutPos,
                        self.sharesInstitHolderBoughtNew, self.sharesInstitHolderSoldOut, self.netSharesInstitHolderTradedNew,
                        self.numberOfInsiderBoughtInThreeMonth, self.numberOfInsiderSoldInThreeMonth, self.netNumberOfInsiderHoldingInThreeMonth,
                        self.sharesInsiderBoughtInThreeMonth, self.sharesInsiderSoldInThreeMonth, self.netSharesInsiderTradedInThreeMonth,
                        self.numberOfInsiderBoughtInTwelveMonth, self.numberOfInsiderSoldInTwelveMonth, self.netNumberOfInsiderHoldingInTwelveMonth,
                        self.sharesInsiderBoughtInTwelveMonth, self.sharesInsiderSoldInTwelveMonth, self.netSharesInsiderTradedInTwelveMonth,
                        self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)
                        ]
            
        databaseOper.insertListOfData(stockShareHoldingTable, listInstVals, listInstCols)
        del databaseOper
        
        return None
    #end: writeUsStockHoldingInfoToDB
    
    def writeUsStockRevenueToDB(self):
        """ Insert Stock Revenue to tblStockRevenue (delete duplicate, mark delete old and insert new) """
        stockRevenueTable = "tblStockRevenue"

        # 1. delete duplicate: del record with same Ticker, ListedExch, Source and DataAsOfDate
        databaseOper = clsDatabaseOper.DatabaseOper()
        listDelCols = ["StockTicker", "ListedExchCode", "Source", "DataAsOfDate"]
        listDelVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE, self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)]
        databaseOper.deleteRecord(stockRevenueTable, listDelCols, listDelVals)
        del databaseOper
        
        # 2. mark delete old: update IsLatest to 'N' with same Ticker, ListedExch and Source
        databaseOper = clsDatabaseOper.DatabaseOper()
        listUpdCols = ["StockTicker", "ListedExchCode", "Source"]
        listUpdVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE]
        databaseOper.updateSingleValue(stockRevenueTable, "IsLatest", "N", listUpdCols, listUpdVals)
        del databaseOper
        
        # 3. insert new record to DB
        databaseOper = clsDatabaseOper.DatabaseOper()
        listInstCols = ["StockTicker", "ListedExchCode", "Source", 
                        "EpsRegressGrowth","DataAsOfDate"
                        ]

        listInstVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE, 
                        self.forecastEarningsGrowth, self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)
                        ]

        databaseOper.insertListOfData(stockRevenueTable, listInstVals, listInstCols)
        del databaseOper
        
        return None
    #end: writeUsStockRevenueToDB
    
    def writeUsStockGuruAnalysisToDB(self):
        """ Insert Stock Revenue to tblStockNasdaqGuru (delete duplicate, mark delete old and insert new) """
        stockNasdaqGurueTable = "tblStockNasdaqGuru"

        # 1. delete duplicate: del record with same Ticker, ListedExch, Source and DataAsOfDate
        databaseOper = clsDatabaseOper.DatabaseOper()
        listDelCols = ["StockTicker", "ListedExchCode", "DataAsOfDate"]
        listDelVals = [self.compTicker, self.listedExchCode, self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)]
        databaseOper.deleteRecord(stockNasdaqGurueTable, listDelCols, listDelVals)
        del databaseOper
        
        # 2. mark delete old: update IsLatest to 'N' with same Ticker, ListedExch and Source
        databaseOper = clsDatabaseOper.DatabaseOper()
        listUpdCols = ["StockTicker", "ListedExchCode"]
        listUpdVals = [self.compTicker, self.listedExchCode]
        databaseOper.updateSingleValue(stockNasdaqGurueTable, "IsLatest", "N", listUpdCols, listUpdVals)
        del databaseOper
        
        # 3. insert new record to DB
        databaseOper = clsDatabaseOper.DatabaseOper()
        listInstCols = ["StockTicker", "ListedExchCode", 
                        "PeterLynchVerdict","PeterLynchAnalysis",
                        "BenjaminGarhamVerdict","BenjaminGarhamAnalysis",
                        "MomentumStrategyVerdict","MomentumStrategyAnalysis",
                        "JamesOShaughnessyVerdict","JamesOShaughnessyAnalysis",
                        "MotleyFoolVerdict","MotleyFoolAnalysis",
                        "DavidDremanVerdict","DavidDremanAnalysis",
                        "MartinZweigVerdict","MartinZweigAnalysis",
                        "KennethFisherVerdict","KennethFisherAnalysis",
                        "DataAsOfDate"
                        ]

        listInstVals = [self.compTicker, self.listedExchCode, 
                        self.guruPeterLynchVerdict, self.guruPeterLynchValue, 
                        self.guruBenjaminGarhamVerdict, self.guruBenjaminGarhamValue, 
                        self.guruPMomentumStrategyVerdict, self.guruPMomentumStrategyValue, 
                        self.guruJamesOShaughnessyVerdict, self.guruJamesOShaughnessyValue, 
                        self.guruMotleyFoolVerdict, self.guruMotleyFoolValue, 
                        self.guruDavidDremanVerdict, self.guruDavidDremanValue, 
                        self.guruMartinZweigVerdict, self.guruMartinZweigValue, 
                        self.guruKennethFisherVerdict, self.guruKennethFisherValue, 
                        self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)
                        ]

        databaseOper.insertListOfData(stockNasdaqGurueTable, listInstVals, listInstCols)
        del databaseOper

        return None
    #end: writeUsStockGuruAnalysisToDB
    
    def stockStaticToStr(self, colSep=clsGeneralConstants.GeneralConstants.DEFAULT_COLUMN_SEP):
        usStockStr = ""
        usStockStr += "StockTicker" + colSep + self.compTicker + "\n"
        usStockStr += "ListedExchCode" + colSep + self.listedExchName + "(" + self.listedExchName + ") \n"
        usStockStr += "CompanyName" + colSep + self.compName + "\n"
        usStockStr += "RIC" + colSep + self.compRic + "\n"
        usStockStr += "Source" + colSep + self.DATA_SOURCE + "\n"
        usStockStr += "BelongToIndex" + colSep + self.belongToIndex + "\n"
        usStockStr += "Sector" + colSep + self.sector + "\n"
        usStockStr += "Industry" + colSep + self.industry + "\n"
        usStockStr += "As_Of_Date" + colSep + self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT) + "\n"
        
        return usStockStr
    #end: stockStaticToStr

    def __str__(self, colSep=clsGeneralConstants.GeneralConstants.DEFAULT_COLUMN_SEP):
        """ print our Index Information and composite details at defined order
        """
        usStockStr = ""
        usStockStr += "Record_Date" + colSep + self.dataRecordDate + "\n"
        usStockStr += "Company_Name" + colSep + self.compName + "\n"
        usStockStr += "Ticker" + colSep + self.compTicker + "\n"
        usStockStr += "RIC" + colSep + self.compRic + "\n"
        usStockStr += "Sector" + colSep + self.sector + "\n"
        usStockStr += "Industry" + colSep + self.industry + "\n"
        usStockStr += "Listed_Market" + colSep + self.listedExchCode + "\n"
        usStockStr += "As_Of_Date" + colSep + self.asOfDate + "\n"
        usStockStr += "Price" + colSep + self.price + "\n"
        usStockStr += "Price Change" + colSep + self.priceChange + "\n"
        usStockStr += "Percent Change" + colSep + self.percentChange + "\n"
        
        usStockStr += "Open Price" + colSep + self.openPrice + "\n"
        usStockStr += "Prev Close" + colSep + self.prevClosePrice + "\n"
        usStockStr += "Day's High" + colSep + self.dayHighPrice + "\n"
        usStockStr += "Day's Low" + colSep + self.dayLowPrice + "\n"
        usStockStr += "Volumn" + colSep + self.volume + "\n"
        usStockStr += "52-wk High" + colSep + self.yearHigh + "\n"
        usStockStr += "52-wk Low" + colSep + self.yearLow + "\n"
        
        return usStockStr 
    #end: __str__