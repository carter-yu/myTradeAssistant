# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 10:48:59 2018

@author: Carter
"""

import time
import datetime
import mechanicalsoup

import sys
import traceback
sys.path.append('../')
from GeneralTools import clsDatabaseOper
from GeneralTools import clsGeneralConstants
from GeneralTools import clsGeneralMethods
from sklearn import linear_model
#import matplotlib.pyplot as plt


class ReutersUsStockDataStructure(object):
    DB_STOCK_STATIC_TBL = "tblStockStatic"
    DB_EXCH_STATIC = "tblExchange"
    DATA_SOURCE = "Reuters"
    
    def __init__(self, _reutersUrl, _ric):
        self.generalMethods = clsGeneralMethods.GeneralMethods()
        
        self.reutersUrl = _reutersUrl
        # Stock Static (table:tblStockStatic)
        self.compRic = _ric
        self.dataRecordDate = time.strftime(clsGeneralConstants.GeneralConstants.DATA_RECORD_DATE_FORMAT)
        
        if (len(_ric) > 0 ) :
            self.compTicker = _ric.split(".")[0]
        else:
            self.compTicker = ""
        
        self.reutersUsStockPage = None
        self.isConnectionError = False
        self.isSymbolValid = True
        
        self.compName = ""
        self.sector = ""
        self.industry = ""
        self.listedExchName = ""
        self.listedExchCode = ""
        self.asOfDate = datetime.datetime.now()
        self.belongToIndex = ""
        self.isNewIndex = False

        #Quote Section : sectionQuoteDetail, sectionQuote
        #page: Open 
        self.isIntraDayPrice = ""
        self.priceChange = ""
        self.percentChange = "" 
        self.price = ""
        self.openPrice = ""
        #page: Prev Close 
        self.prevClosePrice = ""
        #page: Day's High
        self.dayHighPrice = ""
        #page: Day's Low
        self.dayLowPrice = ""
        #page: Volume 
        self.volume = ""
        self.avgVolume = ""
        
        #page: 52-wk High 
        self.yearHigh = ""
        #page: 52-wk Low 
        self.yearLow = ""
        # moduleHeader: Revenue & Earnings Per Share
        ## 1st Year
        self.quarterMinusOneDate = "Null"
        self.quarterMinusOneRevenue = 0
        self.quarterMinusOneEps = 0
        self.quarterMinusTwoDate = "Null"
        self.quarterMinusTwoRevenue = 0
        self.quarterMinusTwoEps = 0
        self.quarterMinusThreeDate = "Null"
        self.quarterMinusThreeRevenue = 0
        self.quarterMinusThreeEps = 0
        self.quarterMinusFourDate = "Null"
        self.quarterMinusFourRevenue = 0
        self.quarterMinusFourEps = 0
        ## 2nd Year
        self.quarterMinusFiveDate = "Null"
        self.quarterMinusFiveRevenue = 0
        self.quarterMinusFiveEps = 0
        self.quarterMinusSixDate = "Null"
        self.quarterMinusSixRevenue = 0
        self.quarterMinusSixEps = 0
        self.quarterMinusSevenDate = "Null"
        self.quarterMinusSevenRevenue = 0
        self.quarterMinusSevenEps = 0
        self.quarterMinusEightDate = "Null"
        self.quarterMinusEightRevenue = 0
        self.quarterMinusEightEps = 0
        self.quarterOneVsQuarterTwo = 0
        self.quarterTwoVsQuarterThree = 0
        self.quarterThreeVsQuarterFour = 0
        self.quarterFourVsQuarterFive = 0
        self.quarterFiveVsQuarterSix = 0
        self.quarterSixVsQuarterSeven = 0
        self.quarterSevenVsQuarterEight = 0
        
        self.epsRegressGrowth = 0
        
        self.unitOfRevneue = 0
        # moduleHeader: Valuation Ratios
        #page: P/E Ratio (TTM)
        self.peTtmComp = ""
        self.peTtmIndustry = ""
        self.peTtmSector = ""
        #page: P/E High - Last 5 Yrs.
        self.peFiveYrHighComp = ""
        self.peFiveYrHighIndustry = ""
        self.peFiveYrHighSector = ""
        #page: P/E Low - Last 5 Yrs.
        self.peFiveYrLowComp = ""
        self.peFiveYrLowIndustry = ""
        self.peFiveYrLowSector = ""
        #page: Beta
        self.betaComp = ""
        self.betaIndustry = ""
        self.betaSector = ""
        #page: Price to Sales (TTM)
        self.priceToSalesComp = ""
        self.priceToSalesIndustry = ""
        self.priceToSalesSector = ""
        #page: Price to Book (MRQ)
        self.priceToBookComp = ""
        self.priceToBookIndustry = ""
        self.priceToBookSector = ""
        #page: Price to Tangible Book (MRQ)
        self.priceToTangibleBookComp = ""
        self.priceToTangibleBookIndustry = ""
        self.priceToTangibleBookSector = ""
        #page: Price to Cash Flow (TTM)
        self.priceToCashFlowComp = ""
        self.priceToCashFlowIndustry = ""
        self.priceToCashFlowSector = ""
        # moduleHeader: Dividends
        #page: Dividend Yield
        self.divYieldComp = ""
        self.divYieldIndustry = ""
        self.divYieldSector = ""
        #page: Dividend Yield - 5 Year Avg
        self.divFiveYrAvgComp = ""
        self.divFiveYrAvgIndustry = ""
        self.divFiveYrAvgSector = ""
        #page: Dividend 5 Year Growth Rate
        self.divFiveYrGrowthRateComp = ""
        self.divFiveYrGrowthRateIndustry = ""
        self.divFiveYrGrowthRateSector = ""
        #page: Payout Ratio(TTM)
        self.divPayoutRatioComp = ""
        self.divPayoutRatioIndstry = ""
        self.divPayoutRatioSector = ""
        # moduleHeader: Growth Rates
        #page: Sales (MRQ) vs Qtr. 1 Yr. Ago
        self.salesMrqVsPrevYrQtrComp = ""
        self.salesMrqVsPrevYrQtrIndustry = ""
        self.salesMrqVsPrevYrQtrSector = ""
        #page: Sales (TTM) vs TTM 1 Yr. Ago
        self.salesTtmVsPrevYrComp = ""
        self.salesTtmVsPrevYrIndustry = ""
        self.salesTtmVsPrevYrSector = ""
        #page: Sales - 5 Yr. Growth Rate
        self.salesFiveYrGrowthRateComp = ""
        self.salesFiveYrGrowthRateIndustry = ""
        self.salesFiveYrGrowthRateSector = ""
        #page: EPS (MRQ) vs Qtr. 1 Yr. Ago
        self.epsMrqVsPreYrQtrComp = ""
        self.epsMrqVsPreYrQtrIndustry = ""
        self.epsMrqVsPreYrQtrSector = ""
        #page: EPS (TTM) vs TTM 1 Yr. Ago
        self.epsTtmVsPrevYrComp = ""
        self.epsTtmVsPrevYrIndustry = ""
        self.epsTtmVsPrevYrSector = ""
        #page: EPS - 5 Yr. Growth Rate
        self.epsFiveYrGrowthRateComp = ""
        self.epsFiveYrGrowthRateIndustry = ""
        self.epsFiveYrGrowthRateSector = ""
        # moduleHeader: Financial Strength
        #page: Quick Ratio (MRQ)
        self.quickRatioMrqComp = ""
        self.quickRatioMrqIndustry = ""
        self.quickRatioMrqSector = ""
        #page: Current Ratio (MRQ)
        self.currentRatioMrqComp = ""
        self.currentRatioMrqIndustry = ""
        self.currentRatioMrqSector = ""
        #page: LT Debt to Equity (MRQ)
        self.longTermDebtToEquityMrqComp = ""
        self.longTermDebtToEquityMrqIndustry = ""
        self.longTermDebtToEquityMrqSector = ""
        #page: Total Debt to Equity (MRQ)
        self.totalDebtToEquityMrqComp = ""
        self.totalDebtToEquityMrqIndustry = ""
        self.totalDebtToEquityMrqSector = ""
        #page: Interest Coverage (TTM)
        self.interestCoverageTtmComp = ""
        self.interestCoverageTtmIndustry = ""
        self.interestCoverageTtmSector = ""
        # moduleHeader: Profitability Ratios
        #page: Gross Margin (TTM)
        self.grossMarginTtmComp = ""
        self.grossMarginTtmIndustry = ""
        self.grossMarginTtmSector = ""
        #page: Gross Margin - 5 Yr. Avg.
        self.grossMarginFiveYrAvgComp = ""
        self.grossMarginFiveYrAvgIndustry = ""
        self.grossMarginFiveYrAvgSector = ""
        #page: EBITD Margin (TTM)
        self.ebitdMarginTtmComp = ""
        self.ebitdMarginTtmIndustry = ""
        self.ebitdMarginTtmSector = ""
        #page: EBITD - 5 Yr. Avg
        self.ebitdFiveYrAvgComp = ""
        self.ebitdFiveYrAvgIndustry = ""
        self.ebitdFiveYrAvgSector = ""
        #page: Operating Margin (TTM)
        self.operMarginTtmComp = ""
        self.operMarginTtmIndustry = ""
        self.operMarginTtmSector = ""
        #page: Operating Margin - 5 Yr. Avg.
        self.operMarginFiveYrAvgComp = ""
        self.operMarginFiveYrAvgIndustry = ""
        self.operMarginFiveYrAvgSector = ""
        #page: Pre-Tax Margin (TTM)
        self.preTaxMarginTtmComp = ""
        self.preTaxMarginTtmIndustry = ""
        self.preTaxMarginTtmSector = ""
        #page: Pre-Tax Margin - 5 Yr. Avg.
        self.preTaxMarginFiveYrAvgComp = ""
        self.preTaxMarginFiveYrAvgIndustry = ""
        self.preTaxMarginFiveYrAvgSector = ""
        #page: Net Profit Margin (TTM)
        self.netProfitMarginTtmComp = ""
        self.netProfitMarginTtmIndustry = ""
        self.netProfitMarginTtmSector = ""
        #page: Net Profit Margin - 5 Yr. Avg.
        self.netProfitMarginFiveYrAvgComp = ""
        self.netProfitMarginFiveYrAvgIndustry = ""
        self.netProfitMarginFiveYrAvgSector = ""
        #page: Effective Tax Rate (TTM)
        self.effectiveTaxRateTtmComp = ""
        self.effectiveTaxRateTtmIndustry = ""
        self.effectiveTaxRateTtmSector = ""
        #page: Effective Tax Rate - 5 Yr. Avg.
        self.effectiveTaxRateFiveYrAvgComp = ""
        self.effectiveTaxRateFiveYrAvgIndustry = ""
        self.effectiveTaxRateFiveYrAvgSector = ""
        # moduleHeader: Efficiency
        #page:  Revenue/Employee (TTM)
        self.revenuePerEmployeeTtmComp = ""
        self.revenuePerEmployeeTtmIndustry = ""
        self.revenuePerEmployeeTtmSector = ""
        #page: Net Income/Employee (TTM)
        self.netIcomePerEmployeeTtmComp = ""
        self.netIcomePerEmployeeTtmIndustry = ""
        self.netIcomePerEmployeeTtmSector = ""
        #page: Receivable Turnover (TTM)
        self.receivableTurnoverTtmComp = ""
        self.receivableTurnoverTtmIndustry = ""
        self.receivableTurnoverTtmSector = ""
        #page: Inventory Turnover (TTM)
        self.iventoryTurnoverTtmComp = ""
        self.iventoryTurnoverTtmIndustry = ""
        self.iventoryTurnoverTtmSector = ""
        #page: Asset Turnover (TTM)
        self.assetTurnoverTtmComp = ""
        self.assetTurnoverTtmIndustry = ""
        self.assetTurnoverTtmSector = ""
        # moduleHeader: Management Effectiveness
        #page: Return on Assets (TTM)
        self.returnOnAssetsTtmComp = ""
        self.returnOnAssetsTtmIndustry = ""
        self.returnOnAssetsTtmSector = ""
        #page: Return on Assets - 5 Yr. Avg.
        self.returnOnAssetsFiveYrAvgComp = ""
        self.returnOnAssetsFiveYrAvgIndustry = ""
        self.returnOnAssetsFiveYrAvgSector = ""
        #page: Return on Investment (TTM)
        self.returnOnInvestmentTtmComp = ""
        self.returnOnInvestmentTtmIndustry = ""
        self.returnOnInvestmentTtmSector = ""
        #page: Return on Investment - 5 Yr. Avg.
        self.returnOnInvestmentFiveYrAvgComp = ""
        self.returnOnInvestmentFiveYrAvgIndustry = ""
        self.returnOnInvestmentFiveYrAvgSector = ""
        #page: Return on Equity (TTM)
        self.returnOnEquityTtmComp = ""
        self.returnOnEquityTtmIndustry = ""
        self.returnOnEquityTtmSector = ""
        #page: Return on Equity - 5 Yr. Avg.
        self.returnOnEquityFiveYrAvgComp = ""
        self.returnOnEquityFiveYrAvgIndustry = ""
        self.returnOnEquityFiveYrAvgSector = ""
        #
        self.sharesInstitHolderHeld = 0
        self.percentageInstitHolderHeld = 0
        self.netSharesInsiderTradedInThreeMonth = 0 
        
### Major Public methods
### Major Public methods
### Major Public methods
    def getAllStockData(self):
        """ Scrape out Stock Static, Daily Price, Revenue, Valuation, Financial Strength and Stock mangement Effectiveness """
        #scrape the content
        self.scrapeStockStaicAndDailyPrice()
        self.scrapeStockRevenue()
        self.scrapeStockValuation()
        self.scrapeStockFinancialStrength()
        self.scrapeStockManagementEffectiveness()
        self.scrapeStockInstitutionalHolders()
        return None
    #end: getAllStockData
    
    def writeAllStockData(self, belongToIndex):
        """ Write all stock data to DB """
        self.writeUsStockStaticToDB(belongToIndex)
        self.writeUsStockRevenueToDB()
        self.writeUsStockClosePriceToDB()
        self.writeUsStockValuationToDB()
        self.writeUsStockFinanicalStrengthToDB()
        self.writeUsStockManagementEffectivenessToDB()
        self.writeStockInstitutionalHoldersToDB()
        return None
    #end: writeAllStockData
    
    def loadDataFromWeb(self):
        """ Download the Reuters page and check if it contains Stock data. """
        try:
            browser = mechanicalsoup.StatefulBrowser()
            browser.open(self.reutersUrl)
            self.reutersUsStockPage = browser.get_current_page()
            self.checkSymbol()
            self.generalMethods.printLog("Reuters: self.compRic = " + self.compRic + " , self.isSymbolValid = " + str( self.isSymbolValid ))
            self.isConnectionError = False
        except:
            self.isConnectionError = True
            self.generalMethods.printLog("Reuters: self.compRic = " + self.compRic + " , self.isConnectionError = " + str( self.isConnectionError ))
            self.generalMethods.printLog(str(traceback.format_exc()))
        return None
    #end: loadDataFromWeb
    
    def checkSymbol(self):
        """ Check if the downloaded Reuters page contains valid stock data """
        allDivItems = self.reutersUsStockPage.findAll("div")
        for divItem in allDivItems:
            divTxt = divItem.text.lower().strip()
            if(-1 != divTxt.find("no search results match the term")):
                self.isSymbolValid = False
                self.generalMethods.printLog("Invalid Symbol (" + self.compRic + ") : No search results match.")
            compNameDivItem = self.reutersUsStockPage.find("div", attrs={"id": "sectionTitle"})
            if(None == compNameDivItem):
                self.isSymbolValid = False
                self.generalMethods.printLog("Invalid Symbol (" + self.compRic + ") : No Company Name Div Item.")
        return None
    #end: checkSymbol
            
## Web Scrape
## Web Scrape
## Web Scrape
    def scrapeStockStaicAndDailyPrice(self):
        """ Scrape out Stock static and Daily Price """
        if (None == self.reutersUsStockPage):
#            self.generalMethods.printLog( "Load web page" )
            self.loadDataFromWeb()
        
        if (self.isConnectionError):
            secToSleep = 30 
            time.sleep(secToSleep)
            self.generalMethods.printLog("Reuters: Sleep "+ str(secToSleep) + " seconds and then retry Symbol (" + self.compRic + ")")
            self.loadDataFromWeb()
        
        if (self.isSymbolValid):
            # Head section : Name, Sector, Industry, listed Market and Current Price
            compNameDivItem = self.reutersUsStockPage.find("div", attrs={"id": "sectionTitle"})
            self.compName = compNameDivItem.find("h1").text.strip()
            self.compName = self.compName.replace(self.compName.split(" ")[-1], "")
            
            relatedTopicsDivItem = self.reutersUsStockPage.find("div", attrs={"class": "sectionRelatedTopics"})
            relatedTopicsLinks = relatedTopicsDivItem.findAll("a")
            for topicsLink in relatedTopicsLinks:
                if (-1 != topicsLink.attrs["href"].lower().find("sectors")) and (-1 == topicsLink.attrs["href"].lower().find("industries")):
                    self.sector = topicsLink.text.strip()
                if (-1 != topicsLink.attrs["href"].lower().find("industries")):
                    self.industry = topicsLink.text.strip()
    
            headerQuoteItem = self.reutersUsStockPage.find("div", attrs={"id": "headerQuoteContainer"})
            headerQuoteDetailItem = headerQuoteItem.find("div", attrs={"class": "sectionQuoteDetail"})
            headerSpans = headerQuoteDetailItem.findAll("span")
            for headerSpan in headerSpans:
                MKT_NAME_START_TXT = "on "
                mktTextStart = headerSpan.text.strip().lower().find(MKT_NAME_START_TXT)
                if(-1 != mktTextStart):
                    self.listedExchName = headerSpan.text.strip()[(mktTextStart + len(MKT_NAME_START_TXT)):]
                    
                    databaseOper = clsDatabaseOper.DatabaseOper()
                    listOfKeyCols = ["ExchangeName", "Source"]
                    listOfKeyVals = [self.listedExchName, "Reuters"]
                    self.listedExchCode = databaseOper.retrieveSelectSingleValue(self.DB_EXCH_STATIC, "ListedExchCode", listOfKeyCols, listOfKeyVals)
                    del databaseOper
                    
                elif("class" in headerSpan.attrs):
                    asOfDateOrTimeTxt = headerSpan.text.strip() 
#                    self.generalMethods.printLog("asOfDateOrTimeTxt = " + asOfDateOrTimeTxt)
                    if( (-1 != asOfDateOrTimeTxt.lower().find("am")) and (-1 != asOfDateOrTimeTxt.lower().find("pm")) ):
                        self.asOfDate = self.generalMethods.tryParseDate(asOfDateOrTimeTxt, "%d %b %Y")
                        self.isIntraDayPrice = True
                    else:
                        self.asOfDate = datetime.datetime.now() #.strftime("%d %b %Y")
                        self.isIntraDayPrice = False
                elif("style" in headerSpan.attrs):
                    headerSpanTxt = headerSpan.text.strip()
                    self.price = self.generalMethods.tryParseFloat(headerSpanTxt)

            # Head section : Price changed , percent changed
            headerQuoteItem = self.reutersUsStockPage.find("div", attrs={"class": "sectionQuote priceChange"})
            headerQuoteDetailItem = headerQuoteItem.find("div", attrs={"class": "sectionQuoteDetail"})
            priceChgSpans = headerQuoteDetailItem.find("span", attrs={"class": "valueContent"})
            spanTxt = priceChgSpans.text.split("\n")[2].strip()
            self.priceChange = self.generalMethods.tryParseFloat(spanTxt)
            priceChgSpans = headerQuoteDetailItem.find("span", attrs={"class": "valueContentPercent"})
            spanTxt = priceChgSpans.text
            self.percentChange = self.generalMethods.tryParseFloat(spanTxt)
            
            # Head section - Quote Top: Prev Close, Day's High, Volume, 52-wk High
            quoteDetailTopDivs = self.reutersUsStockPage.findAll("div", attrs={"class": "sectionQuoteDetailTop"})
            SPAN_VAL_IDX = 1 
            for quoteDetailTopDiv in quoteDetailTopDivs:
                quoteDetailSpans = quoteDetailTopDiv.findAll("span")
                for quoteDetailSpan in quoteDetailSpans:
                    spanTxt = quoteDetailSpans[SPAN_VAL_IDX].text.strip()
                    spanVal = self.generalMethods.tryParseFloat(spanTxt)
                    if (-1 != quoteDetailSpan.text.lower().strip().find("prev close")):
                        self.prevClosePrice = spanVal
                    elif (-1 != quoteDetailSpan.text.lower().strip().find("day's high")):
                        self.dayHighPrice = spanVal
                    elif (-1 != quoteDetailSpan.text.lower().strip().find("volume")):
                        self.volume = spanVal
                    elif (-1 != quoteDetailSpan.text.lower().strip().find("52-wk high")):
                        self.yearHigh = spanVal
    
            # Head section - Quote Tail: Open, Day's Low, 52-wk Low
            quoteDetailTopDivs = self.reutersUsStockPage.findAll("div", attrs={"class": "sectionQuoteDetail"})
            for quoteDetailTopDiv in quoteDetailTopDivs:
                quoteDetailSpans = quoteDetailTopDiv.findAll("span")
                for quoteDetailSpan in quoteDetailSpans:
                    spanTxt = quoteDetailSpans[SPAN_VAL_IDX].text
                    spanVal = self.generalMethods.tryParseFloat(spanTxt)
                    if (-1 != quoteDetailSpan.text.lower().strip().find("open")):
                        self.openPrice = spanVal
                    elif (-1 != quoteDetailSpan.text.lower().strip().find("day's low")):
                        self.dayLowPrice = spanVal
                    elif (-1 != quoteDetailSpan.text.lower().strip().find("avg. vol")):
                        self.avgVolume = spanVal
                    elif (-1 != quoteDetailSpan.text.lower().strip().find("52-wk low")):
                        self.yearLow = spanVal

        return None
    #end: scrapeStockStaicAndDailyPrice
                
    def scrapeStockRevenue(self):
        """ Scrape out Stock Revenue : EPS """
        if (None == self.reutersUsStockPage):
            self.loadDataFromWeb() 
            
        if (self.isSymbolValid):
            # Financial highlights Table
            financialHighlightsModules = self.reutersUsStockPage.findAll("div", attrs={"class": "module"})
            for financialHighlightsModule in financialHighlightsModules:
                financialHighlightsModuleHeader = financialHighlightsModule.find("div", attrs={"class": "moduleHeader"})
                if( None != financialHighlightsModuleHeader):
                    # # # START: revenue & earnings per share # # #
                    if( -1 != financialHighlightsModuleHeader.text.strip().lower().find("revenue & earnings per share") ):
                        revenueModuleBody = financialHighlightsModule.find("div", attrs={"class": "moduleBody"})
                        EPS_DATE_FORMAT = "%b %Y"
                        revenueDataRows = revenueModuleBody.findAll("tr")
                        
                        revenueFinYear = ""
                        revenueDate = "Null"
                        revenueValue = 0
                        revenueEps = 0
                        REVENUE_NEEDED = 8
                        revenueIdx = 0 
                        epsValues = []
                        epsDates = []
                        for revenueDataRow in revenueDataRows:
                            revenueDataItems = revenueDataRow.findAll("td")
                            if (4 == len(revenueDataItems)):
                                revenueFinYear = revenueDataItems[0].text.strip()[-4:] #e.g. FY 2018
                                revenueDateTxt = revenueDataItems[1].text.strip()[0:4] + " " + revenueFinYear
                                if( self.generalMethods.isDate(revenueDateTxt, EPS_DATE_FORMAT) ):
                                    revenueDate = self.generalMethods.tryParseDate(revenueDateTxt, EPS_DATE_FORMAT)
                                else:
                                    revenueDate = "Null"

                                revenueValueTxt = revenueDataItems[2].text.strip()
                                revenueValue = self.generalMethods.tryParseFloat(revenueValueTxt)
                                revenueEpsTxt = revenueDataItems[3].text.strip()
                                revenueEps = self.generalMethods.tryParseFloat(revenueEpsTxt)

                            elif (3 == len(revenueDataItems)):
#                                revenueFinYear = revenueDataItems[0].text.strip()[-4:] #e.g. FY 2018
                                revenueDateTxt = revenueDataItems[0].text.strip()[0:4] + " " + revenueFinYear
                                if( self.generalMethods.isDate(revenueDateTxt, EPS_DATE_FORMAT) ):
                                    revenueDate = self.generalMethods.tryParseDate(revenueDateTxt, EPS_DATE_FORMAT)
                                else:
                                    revenueDate = "Null"

                                revenueValueTxt = revenueDataItems[1].text.strip()
                                revenueValue = self.generalMethods.tryParseFloat(revenueValueTxt)
                                
                                revenueEpsTxt = revenueDataItems[2].text.strip()
                                revenueEps = self.generalMethods.tryParseFloat(revenueEpsTxt)

                            if(1 == revenueIdx):
                                self.quarterMinusOneDate = revenueDate
                                self.quarterMinusOneRevenue = revenueValue
                                self.quarterMinusOneEps = revenueEps
#                                epsDateList = [self.quarterMinusOneDate.strftime(clsGeneralConstants.GeneralConstants.EPS_GRAPH_DATE_FORMAT)[1:]]
                                epsDateList = ["8"]
                                epsDates.append(epsDateList)
                                epsValues.append(self.quarterMinusOneEps)
                            elif(2 == revenueIdx):
                                self.quarterMinusTwoDate = revenueDate
                                self.quarterMinusTwoRevenue = revenueValue
                                self.quarterMinusTwoEps = revenueEps
#                                epsDateList = [self.quarterMinusTwoDate.strftime(clsGeneralConstants.GeneralConstants.EPS_GRAPH_DATE_FORMAT)[1:]]
                                epsDateList = ["7"]
                                epsDates.append(epsDateList)
                                epsValues.append(self.quarterMinusTwoEps)
                            elif(3 == revenueIdx):
                                self.quarterMinusThreeDate = revenueDate
                                self.quarterMinusThreeRevenue = revenueValue
                                self.quarterMinusThreeEps = revenueEps
#                                epsDateList = [self.quarterMinusThreeDate.strftime(clsGeneralConstants.GeneralConstants.EPS_GRAPH_DATE_FORMAT)[1:]]
                                epsDateList = ["6"]
                                epsDates.append(epsDateList)
                                epsValues.append(self.quarterMinusThreeEps)
                            elif(4 == revenueIdx):
                                self.quarterMinusFourDate = revenueDate
                                self.quarterMinusFourRevenue = revenueValue
                                self.quarterMinusFourEps = revenueEps
#                                epsDateList = [self.quarterMinusFourDate.strftime(clsGeneralConstants.GeneralConstants.EPS_GRAPH_DATE_FORMAT)[1:]]
                                epsDateList = ["5"]
                                epsDates.append(epsDateList)
                                epsValues.append(self.quarterMinusFourEps)
                            elif(5 == revenueIdx):
                                self.quarterMinusFiveDate = revenueDate
                                self.quarterMinusFiveRevenue = revenueValue
                                self.quarterMinusFiveEps = revenueEps
#                                epsDateList = [self.quarterMinusFiveDate.strftime(clsGeneralConstants.GeneralConstants.EPS_GRAPH_DATE_FORMAT)[1:]]
                                epsDateList = ["4"]
                                epsDates.append(epsDateList)
                                epsValues.append(self.quarterMinusFiveEps)
                            elif(6 == revenueIdx):
                                self.quarterMinusSixDate = revenueDate
                                self.quarterMinusSixRevenue = revenueValue
                                self.quarterMinusSixEps = revenueEps
#                                epsDateList = [self.quarterMinusSixDate.strftime(clsGeneralConstants.GeneralConstants.EPS_GRAPH_DATE_FORMAT)[1:]]
                                epsDateList = ["3"]
                                epsDates.append(epsDateList)
                                epsValues.append(self.quarterMinusSixEps)
                            elif(7 == revenueIdx):
                                self.quarterMinusSevenDate = revenueDate
                                self.quarterMinusSevenRevenue = revenueValue
                                self.quarterMinusSevenEps = revenueEps
#                                epsDateList = [self.quarterMinusSevenDate.strftime(clsGeneralConstants.GeneralConstants.EPS_GRAPH_DATE_FORMAT)[1:]]
                                epsDateList = ["2"]
                                epsDates.append(epsDateList)
                                epsValues.append(self.quarterMinusSevenEps)
                            elif(8 == revenueIdx):
                                self.quarterMinusEightDate = revenueDate
                                self.quarterMinusEightRevenue = revenueValue
                                self.quarterMinusEightEps = revenueEps
#                                epsDateList = [self.quarterMinusEightDate.strftime(clsGeneralConstants.GeneralConstants.EPS_GRAPH_DATE_FORMAT)[1:]]
                                epsDateList = ["1"]
                                epsDates.append(epsDateList)
                                epsValues.append(self.quarterMinusEightEps)

                            if(not (revenueIdx < REVENUE_NEEDED)):
                                break
                            else:
                                revenueIdx += 1
                    

#                        self.generalMethods.printLog("epsDates = " + epsDates)
#                        self.generalMethods.printLog("epsValues = " + epsValues)
#                        plt.scatter(epsDates, epsValues,color='black')
#                        plt.xlabel("Date")
#                        plt.ylabel("EPS")
#                        self.generalMethods.printLog("epsDates = " + len(epsDates))
#                        self.generalMethods.printLog("epsValues = " + len(epsValues))
                        if( (len(epsDates) > 0) and (len(epsValues) > 0) and (len(epsDates) == len(epsValues)) ):
                            reg=linear_model.LinearRegression()
                            reg.fit(epsDates, epsValues)
                            self.epsRegressGrowth=reg.coef_[0]
                        #b=reg.intercept_
#                        self.generalMethods.printLog("epsRegressGrowth = " + self.epsRegressGrowth)
                    #Revenue Change
                    try:
                        self.quarterOneVsQuarterTwo = ((self.quarterMinusOneEps/self.quarterMinusTwoEps) -1 ) * 100
                    except (ZeroDivisionError, ValueError) as ex:
                        self.quarterOneVsQuarterTwo = 0
                        
                    try:
                        self.quarterTwoVsQuarterThree = ((self.quarterMinusTwoEps/self.quarterMinusThreeEps) -1 ) * 100
                    except (ZeroDivisionError, ValueError) as ex:
                        self.quarterTwoVsQuarterThree = 0
                        
                    try:
                        self.quarterThreeVsQuarterFour = ((self.quarterMinusThreeEps/self.quarterMinusFourEps) -1 ) * 100
                    except (ZeroDivisionError, ValueError) as ex:
                        self.quarterThreeVsQuarterFour = 0

                    try:
                        self.quarterFourVsQuarterFive = ((self.quarterMinusFourEps/self.quarterMinusFiveEps) -1 ) * 100
                    except (ZeroDivisionError, ValueError) as ex:
                        self.quarterFourVsQuarterFive = 0
                        
                    try:
                        self.quarterFiveVsQuarterSix = ((self.quarterMinusFiveEps/self.quarterMinusSixEps) -1 ) * 100
                    except (ZeroDivisionError, ValueError) as ex:
                        self.quarterFiveVsQuarterSix = 0
                        
                    try:
                        self.quarterSixVsQuarterSeven = ((self.quarterMinusSixEps/self.quarterMinusSevenEps) -1 ) * 100
                    except (ZeroDivisionError, ValueError) as ex:
                        self.quarterSixVsQuarterSeven = 0
                        
                    try:
                        self.quarterSevenVsQuarterEight = ((self.quarterMinusSevenEps/self.quarterMinusEightEps) -1 ) * 100
                    except (ZeroDivisionError, ValueError) as ex:
                        self.quarterSevenVsQuarterEight = 0
                # # # END: revenue & earnings per share # # #
        
            #Revenue Unit
            footnoteModules = self.reutersUsStockPage.findAll("div", attrs={"class": "footnote"})
            #for footnoteModule in footnoteModules:
    #        self.generalMethods.printLog(footnoteModules[0].text.strip())
            unitOfRevneueTxt = footnoteModules[0].text.strip().split("\n")[0].lower()
            if(-1 != unitOfRevneueTxt.find("million")):
                self.unitOfRevneue = 1000000
            elif(-1 != unitOfRevneueTxt.find("billion")):
                self.unitOfRevneue = 1000000000
            elif(-1 != unitOfRevneueTxt.find("trillion")):
                self.unitOfRevneue = 100000000000
        return None
    #end:scrapeStockRevenue

    def scrapeStockValuation(self):
        """ Scrape Stock Valuation : PE """
        if (None == self.reutersUsStockPage):
            self.loadDataFromWeb() 
            
        if (self.isSymbolValid):
            # Financial highlights Table
            financialHighlightsModules = self.reutersUsStockPage.findAll("div", attrs={"class": "module"})
            for financialHighlightsModule in financialHighlightsModules:
                financialHighlightsModuleHeader = financialHighlightsModule.find("div", attrs={"class": "moduleHeader"})
                if( None != financialHighlightsModuleHeader):
                    # # # START: valuation ratios # # #
                    if( -1 != financialHighlightsModuleHeader.text.strip().lower().find("valuation ratios") ):
    #                    self.generalMethods.printLog(financialHighlightsModuleHeader.text.strip())
                        valuationModuleBody = financialHighlightsModule.find("div", attrs={"class": "moduleBody"})
                        valuationDataRows = valuationModuleBody.findAll("tr")
                        for valuationDataRow in valuationDataRows:
                            valuationDataItems = valuationDataRow.findAll("td")
                            if (4 == len(valuationDataItems)):
                                valuationTxt = valuationDataItems[0].text.strip()
                                valuationCompanyTxt = valuationDataItems[1].text.strip()
                                valuationCompany = self.generalMethods.tryParseFloat(valuationCompanyTxt)
                                valuationIndustryTxt = valuationDataItems[2].text.strip() 
                                valuationIndustry = self.generalMethods.tryParseFloat(valuationIndustryTxt)
                                valuationSectorTxt = valuationDataItems[3].text.strip()
                                valuationSector = self.generalMethods.tryParseFloat(valuationSectorTxt)

                                if ("p/e ratio (ttm)" == valuationTxt.lower()):
                                    self.peTtmComp = valuationCompany
                                    self.peTtmIndustry = valuationIndustry
                                    self.peTtmSector = valuationSector
                                elif ("p/e high - last 5 yrs." == valuationTxt.lower()):
                                    self.peFiveYrHighComp = valuationCompany
                                    self.peFiveYrHighIndustry = valuationIndustry
                                    self.peFiveYrHighSector = valuationSector
                                elif ("p/e low - last 5 yrs." == valuationTxt.lower()):
                                    self.peFiveYrLowComp = valuationCompany
                                    self.peFiveYrLowIndustry = valuationIndustry
                                    self.peFiveYrLowSector = valuationSector
                                elif ("beta" == valuationTxt.lower()):
                                    self.betaComp = valuationCompany
                                    self.betaIndustry = valuationIndustry
                                    self.betaSector = valuationSector
                                elif ("price to sales (ttm)" == valuationTxt.lower()):
                                    self.priceToSalesComp = valuationCompany
                                    self.priceToSalesIndustry = valuationIndustry
                                    self.priceToSalesSector = valuationSector
                                elif ("price to book (mrq)" == valuationTxt.lower()):
                                    self.priceToBookComp = valuationCompany
                                    self.priceToBookIndustry = valuationIndustry
                                    self.priceToBookSector = valuationSector
                                elif ("price to tangible book (mrq)" == valuationTxt.lower()):
                                    self.priceToTangibleBookComp = valuationCompany
                                    self.priceToTangibleBookIndustry = valuationIndustry
                                    self.priceToTangibleBookSector = valuationSector
                                elif ("price to cash flow (ttm)" == valuationTxt.lower()):
                                    self.priceToCashFlowComp = valuationCompany
                                    self.priceToCashFlowIndustry = valuationIndustry
                                    self.priceToCashFlowSector = valuationSector
        return None
    #end:scrapeStockValuation
    
    def scrapeStockFinancialStrength(self):
        """ Scrape stock Finanical Strength : Qucik Ratio """
        if (None == self.reutersUsStockPage):
            self.loadDataFromWeb() 
            
        if (self.isSymbolValid):
            # Financial highlights Table
            financialHighlightsModules = self.reutersUsStockPage.findAll("div", attrs={"class": "module"})
            for financialHighlightsModule in financialHighlightsModules:
                financialHighlightsModuleHeader = financialHighlightsModule.find("div", attrs={"class": "moduleHeader"})
                if( None != financialHighlightsModuleHeader):
                    # # # START: valuation ratios # # #
                    if( -1 != financialHighlightsModuleHeader.text.strip().lower().find("financial strength") ):
    #                    self.generalMethods.printLog(financialHighlightsModuleHeader.text.strip())
                        finStrengthModuleBody = financialHighlightsModule.find("div", attrs={"class": "moduleBody"})
                        finStrengthDataRows = finStrengthModuleBody.findAll("tr")
                        for finStrengthDataRow in finStrengthDataRows:
                            finStrengthDataItems = finStrengthDataRow.findAll("td")
                            if (4 == len(finStrengthDataItems)):
                                finStrengthTxt = finStrengthDataItems[0].text.strip()
                                finStrengthCompanyTxt = finStrengthDataItems[1].text.strip()
                                finStrengthCompany = self.generalMethods.tryParseFloat(finStrengthCompanyTxt)               
                                finStrengthIndustryTxt = finStrengthDataItems[2].text.strip() 
                                finStrengthIndustry = self.generalMethods.tryParseFloat(finStrengthIndustryTxt)
                                finStrengthSectorTxt = finStrengthDataItems[3].text.strip()
                                finStrengthSector = self.generalMethods.tryParseFloat(finStrengthSectorTxt)
                                if ("quick ratio (mrq)" == finStrengthTxt.lower()):
                                    self.quickRatioMrqComp = finStrengthCompany
                                    self.quickRatioMrqIndustry = finStrengthIndustry
                                    self.quickRatioMrqSector = finStrengthSector
                                elif ("current ratio (mrq)" == finStrengthTxt.lower()):
                                    self.currentRatioMrqComp = finStrengthCompany
                                    self.currentRatioMrqIndustry = finStrengthIndustry
                                    self.currentRatioMrqSector = finStrengthSector
                                elif ("lt debt to equity (mrq)" == finStrengthTxt.lower()):
                                    self.longTermDebtToEquityMrqComp = finStrengthCompany
                                    self.longTermDebtToEquityMrqIndustry = finStrengthIndustry
                                    self.longTermDebtToEquityMrqSector = finStrengthSector
                                elif ("total debt to equity (mrq)" == finStrengthTxt.lower()):
                                    self.totalDebtToEquityMrqComp = finStrengthCompany
                                    self.totalDebtToEquityMrqIndustry = finStrengthIndustry
                                    self.totalDebtToEquityMrqSector = finStrengthSector
                                elif ("interest coverage (ttm)" == finStrengthTxt.lower()):
                                    self.interestCoverageTtmComp = finStrengthCompany
                                    self.interestCoverageTtmIndustry = finStrengthIndustry
                                    self.interestCoverageTtmSector = finStrengthSector
        return None
    #end:scrapeStockFinancialStrength
    
    
    def scrapeStockManagementEffectiveness(self):
        """ Scrape stock Management Effectiveness : ROE """
        if (None == self.reutersUsStockPage):
            self.loadDataFromWeb() 
            
        if (self.isSymbolValid):
            # Financial highlights Table
            financialHighlightsModules = self.reutersUsStockPage.findAll("div", attrs={"class": "module"})
            for financialHighlightsModule in financialHighlightsModules:
                financialHighlightsModuleHeader = financialHighlightsModule.find("div", attrs={"class": "moduleHeader"})
                if( None != financialHighlightsModuleHeader):
                    # # # START: valuation ratios # # #
                    if( -1 != financialHighlightsModuleHeader.text.strip().lower().find("management effectiveness") ):
    #                    self.generalMethods.printLog(financialHighlightsModuleHeader.text.strip())
                        mgtEffectivenessModuleBody = financialHighlightsModule.find("div", attrs={"class": "moduleBody"})
                        mgtEffectivenessDataRows = mgtEffectivenessModuleBody.findAll("tr")
                        for mgtEffectivenessDataRow in mgtEffectivenessDataRows:
                            mgtEffectivenessDataItems = mgtEffectivenessDataRow.findAll("td")
                            if (4 == len(mgtEffectivenessDataItems)):
                                mgtEffectivenessTxt = mgtEffectivenessDataItems[0].text.strip()
                                mgtEffectivenessCompanyTxt = mgtEffectivenessDataItems[1].text.strip()
                                mgtEffectivenessCompany = self.generalMethods.tryParseFloat(mgtEffectivenessCompanyTxt)              
                                mgtEffectivenessIndustryTxt = mgtEffectivenessDataItems[2].text.strip() 
                                mgtEffectivenessIndustry = self.generalMethods.tryParseFloat(mgtEffectivenessIndustryTxt)
                                mgtEffectivenessSectorTxt = mgtEffectivenessDataItems[3].text.strip()
                                mgtEffectivenessSector = self.generalMethods.tryParseFloat(mgtEffectivenessSectorTxt)

                                if ("return on assets (ttm)" == mgtEffectivenessTxt.lower()):
                                    self.returnOnAssetsTtmComp = mgtEffectivenessCompany
                                    self.returnOnAssetsTtmIndustry = mgtEffectivenessIndustry
                                    self.returnOnAssetsTtmSector = mgtEffectivenessSector
                                elif ("return on assets - 5 yr. avg." == mgtEffectivenessTxt.lower()):
                                    self.returnOnAssetsFiveYrAvgComp = mgtEffectivenessCompany
                                    self.returnOnAssetsFiveYrAvgIndustry = mgtEffectivenessIndustry
                                    self.returnOnAssetsFiveYrAvgSector = mgtEffectivenessSector
                                elif ("return on investment (ttm)" == mgtEffectivenessTxt.lower()):
                                    self.returnOnInvestmentTtmComp = mgtEffectivenessCompany
                                    self.returnOnInvestmentTtmIndustry = mgtEffectivenessIndustry
                                    self.returnOnInvestmentTtmSector = mgtEffectivenessSector
                                elif ("return on investment - 5 yr. avg." == mgtEffectivenessTxt.lower()):
                                    self.returnOnInvestmentFiveYrAvgComp = mgtEffectivenessCompany
                                    self.returnOnInvestmentFiveYrAvgIndustry = mgtEffectivenessIndustry
                                    self.returnOnInvestmentFiveYrAvgSector = mgtEffectivenessSector
                                elif ("return on equity (ttm)" == mgtEffectivenessTxt.lower()):
                                    self.returnOnEquityTtmComp = mgtEffectivenessCompany
                                    self.returnOnEquityTtmIndustry = mgtEffectivenessIndustry
                                    self.returnOnEquityTtmSector = mgtEffectivenessSector
                                elif ("return on equity - 5 yr. avg." == mgtEffectivenessTxt.lower()):
                                    self.returnOnEquityFiveYrAvgComp = mgtEffectivenessCompany
                                    self.returnOnEquityFiveYrAvgIndustry = mgtEffectivenessIndustry
                                    self.returnOnEquityFiveYrAvgSector = mgtEffectivenessSector

        return None
    #end:scrapeStockManagementEffectiveness
    
    
    def scrapeStockInstitutionalHolders(self):
        """ Scrape stock Institutional Holders : % shares owned by institutional """
        if (None == self.reutersUsStockPage):
            self.loadDataFromWeb() 
            
        if (self.isSymbolValid):
            # Financial highlights Table
            financialHighlightsModules = self.reutersUsStockPage.findAll("div", attrs={"class": "module"})
            for financialHighlightsModule in financialHighlightsModules:
                financialHighlightsModuleHeader = financialHighlightsModule.find("div", attrs={"class": "moduleHeader"})
                if( None != financialHighlightsModuleHeader):
                    # # # START: valuation ratios # # #
                    if( -1 != financialHighlightsModuleHeader.text.strip().lower().find("institutional holders") ):
                        institutionalHoldersModuleBody = financialHighlightsModule.find("div", attrs={"class": "moduleBody"})
                        institutionalHoldersDataRows = institutionalHoldersModuleBody.findAll("tr")
                        for institutionalHolderssDataRow in institutionalHoldersDataRows:
                            institutionalHoldersDataItems = institutionalHolderssDataRow.findAll("td")
                            if (2 == len(institutionalHoldersDataItems)):
                                institutionalHoldersTitle = institutionalHoldersDataItems[0].text.strip()
                                institutionalHoldersValTxt = institutionalHoldersDataItems[1].text.strip()
                                institutionalHoldersVal = self.generalMethods.tryParseFloat(institutionalHoldersValTxt)                  

                                if ("% shares owned:" == institutionalHoldersTitle.lower()):
                                    self.percentageInstitHolderHeld = institutionalHoldersVal
                                elif ("total shares held:" == institutionalHoldersTitle.lower()):
                                    self.sharesInstitHolderHeld = institutionalHoldersVal
                                elif ("3 mo. net change:" == institutionalHoldersTitle.lower()):
                                    self.netSharesInsiderTradedInThreeMonth = institutionalHoldersVal
        return None
    #end:scrapeStockInstitutionalHolders
    
## Write to DB     
## Write to DB 
## Write to DB     
    def writeUsStockStaticToDB(self, fromIndex=""):
        """ 1. Update the record if there's record in DB with different BelongToIndex. 
            2. Or Insert new stock record to DB
        """
        if("" != fromIndex):
            tickerDB = ""
            indexBelongDB = ""
            tickerAndBelongIndex = self.getDatabaseTickerAndIndexBelong()
            if(0 != len(tickerAndBelongIndex)):
                tickerDB = tickerAndBelongIndex[0]
                indexBelongDB = tickerAndBelongIndex[1]
#            self.generalMethods.printLog("fromIndex= " + fromIndex + "indexBelongDB = " + tickerAndBelongIndex + " (" + str( len(tickerAndBelongIndex) ) + ")")
#            self.generalMethods.printLog("tickerDB= " + tickerDB + "indexBelongDB = " + indexBelongDB)
            
            if ("" == indexBelongDB):
                self.belongToIndex = fromIndex
                ## not exists --> insert
                if("" == tickerDB):
                    self.insertUsStockStaticToDatabase()
                ## exists, but not belong to any index --> update
                else:
                    self.updateDatabaseIndexBelong(self.belongToIndex)
            elif (-1 == indexBelongDB.find(fromIndex)):
                self.belongToIndex = indexBelongDB + ", " + fromIndex
#                self.generalMethods.printLog("self.belongToIndex = " + self.belongToIndex)
                self.updateDatabaseIndexBelong(self.belongToIndex)
        else:
            self.insertUsStockStaticToDatabase()
        return None 
    #end: writeUsStockStaticToDB
    
    def writeUsStockClosePriceToDB(self):
        """ Insert Stock close price to tblStockDailyPrice (delete duplicate, mark delete old and insert new) """
        stockDailyPriceTable = "tblStockDailyPrice"
        
        if not(self.isIntraDayPrice): 
            # 1. delete duplicate: del record with same Ticker, ListedExch, Source and DataAsOfDate
            databaseOper = clsDatabaseOper.DatabaseOper()
            listDelCols = ["StockTicker", "ListedExchCode", "Source", "DataAsOfDate"]
            listDelVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE, self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)]
            databaseOper.deleteRecord(stockDailyPriceTable, listDelCols, listDelVals)
            del databaseOper
            
            # 2. mark delete old: update IsLatest to 'N' with same Ticker, ListedExch and Source
            databaseOper = clsDatabaseOper.DatabaseOper()
            listUpdCols = ["StockTicker", "ListedExchCode", "Source"]
            listUpdVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE]
            databaseOper.updateSingleValue(stockDailyPriceTable, "IsLatest", "N", listUpdCols, listUpdVals)
            del databaseOper
            
            # 3. insert new record to DB
            databaseOper = clsDatabaseOper.DatabaseOper()
            listInstCols = ["StockTicker", "ListedExchCode", "Source", 
                            "OpenPrice", "ClosePrice", "DayHighPrice", 
                            "DayLowPrice", "prevClosePrice", "Volume", 
                            "AvgVolume", "52WkHigh", "52WkLow", "DataAsOfDate"
                           ]

            listInstVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE, 
                            self.openPrice, self.price, self.dayHighPrice, 
                            self.dayLowPrice, self.prevClosePrice, self.volume,
                            self.avgVolume, self.yearHigh, self.yearLow, 
                            self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)
                            ]
        
            databaseOper.insertListOfData(stockDailyPriceTable, listInstVals, listInstCols)
            del databaseOper
        else:
            self.generalMethods.printLog("clsReutersUsStockSourceOper.writeUsStockClosePriceToDB() >>> Not Day Close price. ")
        return None
    #end: writeUsStockClosePriceToDB
    
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
                        "EpsRegressGrowth",
                        "M1QDate", "M1QRevenue", "M1QEps", 
                        "M2QDate", "M2QRevenue", "M2QEps", 
                        "M3QDate", "M3QRevenue", "M3QEps", 
                        "M4QDate", "M4QRevenue", "M4QEps", 
                        "M5QDate", "M5QRevenue", "M5QEps", 
                        "M6QDate", "M6QRevenue", "M6QEps", 
                        "M7QDate", "M7QRevenue", "M7QEps", 
                        "M8QDate", "M8QRevenue", "M8QEps", 
                        "M1QvsM2Q", "M2QvsM3Q", "M3QvsM4Q",
                        "M4QvsM5Q", "M5QvsM6Q", "M6QvsM7Q",
                        "M7QvsM8Q",
                        "RevenueUnit", "DataAsOfDate"
                        ]

        listInstVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE, 
                        self.epsRegressGrowth, 
                        self.quarterMinusOneDate, self.quarterMinusOneRevenue, self.quarterMinusOneEps, 
                        self.quarterMinusTwoDate, self.quarterMinusTwoRevenue, self.quarterMinusTwoEps,
                        self.quarterMinusThreeDate, self.quarterMinusThreeRevenue, self.quarterMinusThreeEps,
                        self.quarterMinusFourDate, self.quarterMinusFourRevenue, self.quarterMinusFourEps,
                        self.quarterMinusFiveDate, self.quarterMinusFiveRevenue, self.quarterMinusFiveEps,
                        self.quarterMinusSixDate, self.quarterMinusSixRevenue, self.quarterMinusSixEps,
                        self.quarterMinusSevenDate, self.quarterMinusSevenRevenue, self.quarterMinusSevenEps,
                        self.quarterMinusEightDate, self.quarterMinusEightRevenue, self.quarterMinusEightEps,
                        self.quarterOneVsQuarterTwo, self.quarterTwoVsQuarterThree, self.quarterThreeVsQuarterFour,
                        self.quarterFourVsQuarterFive, self.quarterFiveVsQuarterSix, self.quarterSixVsQuarterSeven,
                        self.quarterSevenVsQuarterEight,                        
                        self.unitOfRevneue, self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)
                        ]

        databaseOper.insertListOfData(stockRevenueTable, listInstVals, listInstCols)
        del databaseOper
        
        return None
    #end: writeUsStockRevenueToDB
    
    def writeUsStockValuationToDB(self):
        """ Insert Stock valuation to tblStockDailyValuation (delete duplicate, mark delete old and insert new) """
        stockValuationTable = "tblStockDailyValuation"
        
        # 1. delete duplicate: del record with same Ticker, ListedExch, Source and DataAsOfDate
        databaseOper = clsDatabaseOper.DatabaseOper()
        listDelCols = ["StockTicker", "ListedExchCode", "Source", "DataAsOfDate"]
        listDelVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE, self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)]
        databaseOper.deleteRecord(stockValuationTable, listDelCols, listDelVals)
        del databaseOper
        
        # 2. mark delete old: update IsLatest to 'N' with same Ticker, ListedExch and Source
        databaseOper = clsDatabaseOper.DatabaseOper()
        listUpdCols = ["StockTicker", "ListedExchCode", "Source"]
        listUpdVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE]
        databaseOper.updateSingleValue(stockValuationTable, "IsLatest", "N", listUpdCols, listUpdVals)
        del databaseOper
        
        # 3. insert new record to DB
        databaseOper = clsDatabaseOper.DatabaseOper()
        listInstCols = ["StockTicker", "ListedExchCode", "Source", 
                        "Pe", "IndustryPe", "SectorPe", 
                        "5YrHighPe", "Industry5YrHighPe", "Sector5YrHighPe", 
                        "5YrLowPe", "Industry5YrLowPe", "Sector5YrLowPe", 
                        "Beta", "IndustryBeta", "SectorBeta",
                        "PriceToSale", "IndustryPriceToSale", "SectorPriceToSale", 
                        "PriceToBook", "IndustryPriceToBook", "SectorPriceToBook", 
                        "PriceToTangibleBook", "IndustryPriceToTangibleBook", "SectorPriceToTangibleBook", 
                        "PriceToCashFlow", "IndustryPriceToCashFlow", "SectorPriceToCashFlow", 
                        "DataAsOfDate"
                        ]
        
        listInstVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE, 
                        self.peTtmComp, self.peTtmIndustry, self.peTtmSector, 
                        self.peFiveYrHighComp, self.peFiveYrHighIndustry, self.peFiveYrHighSector, 
                        self.peFiveYrLowComp, self.peFiveYrLowIndustry, self.peFiveYrLowSector, 
                        self.betaComp, self.betaIndustry,self.betaSector, 
                        self.priceToSalesComp, self.priceToSalesIndustry, self.priceToSalesSector, 
                        self.priceToBookComp, self.priceToBookIndustry, self.priceToBookSector, 
                        self.priceToTangibleBookComp, self.priceToTangibleBookIndustry, self.priceToTangibleBookSector, 
                        self.priceToCashFlowComp, self.priceToCashFlowIndustry, self.priceToCashFlowSector, 
                        self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)
                        ]
        
        databaseOper.insertListOfData(stockValuationTable, listInstVals, listInstCols)
        del databaseOper
        
        return None
    #end: writeUsStockValuationToDB
    
    def writeUsStockFinanicalStrengthToDB(self):
        """ Insert Stock finanical strength to tblStockDailyFinanicalStrength (delete duplicate, mark delete old and insert new) """
        stockFinStrengthTable = "tblStockDailyFinanicalStrength"
        
        # 1. delete duplicate: del record with same Ticker, ListedExch, Source and DataAsOfDate
        databaseOper = clsDatabaseOper.DatabaseOper()
        listDelCols = ["StockTicker", "ListedExchCode", "Source", "DataAsOfDate"]
        listDelVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE, self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)]
        databaseOper.deleteRecord(stockFinStrengthTable, listDelCols, listDelVals)
        del databaseOper
        
        # 2. mark delete old: update IsLatest to 'N' with same Ticker, ListedExch and Source
        databaseOper = clsDatabaseOper.DatabaseOper()
        listUpdCols = ["StockTicker", "ListedExchCode", "Source"]
        listUpdVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE]
        databaseOper.updateSingleValue(stockFinStrengthTable, "IsLatest", "N", listUpdCols, listUpdVals)
        del databaseOper
        
        # 3. insert new record to DB
        databaseOper = clsDatabaseOper.DatabaseOper()
        listInstCols = ["StockTicker", "ListedExchCode", "Source", 
                        "QuickRatio", "IndustryQuickRatio", "SectorQuickRatio", 
                        "CurrentRatio", "IndustryCurrentRatio", "SectorCurrentRatio", 
                        "LongTermDebtToEquity", "IndustryLongTermDebtToEquity", "SectorLongTermDebtToEquity", 
                        "TotalDebtToEquity", "IndustryTotalDebtToEquity", "SectorTotalDebtToEquity", 
                        "InterestCoverage", "IndustryInterestCoverage", "SectorInterestCoverage", 
                        "DataAsOfDate"
                        ]
        
        listInstVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE, 
                        self.quickRatioMrqComp, self.quickRatioMrqIndustry, self.quickRatioMrqSector, 
                        self.currentRatioMrqComp, self.currentRatioMrqIndustry, self.currentRatioMrqSector, 
                        self.longTermDebtToEquityMrqComp, self.longTermDebtToEquityMrqIndustry, self.longTermDebtToEquityMrqSector, 
                        self.totalDebtToEquityMrqComp, self.totalDebtToEquityMrqIndustry, self.totalDebtToEquityMrqSector, 
                        self.interestCoverageTtmComp, self.interestCoverageTtmIndustry, self.interestCoverageTtmSector, 
                        self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)
                        ]
        
        databaseOper.insertListOfData(stockFinStrengthTable, listInstVals, listInstCols)
        del databaseOper
        
        return None
    #end: writeUsStockFinanicalStrengthToDB
    
    def writeUsStockManagementEffectivenessToDB(self):
        """ Insert Stock management effectiveness to tblStockDailyManagementEffectiveness (delete duplicate, mark delete old and insert new) """
        stockMgtEffectivenessTable = "tblStockDailyManagementEffectiveness"
        
        # 1. delete duplicate: del record with same Ticker, ListedExch, Source and DataAsOfDate
        databaseOper = clsDatabaseOper.DatabaseOper()
        listDelCols = ["StockTicker", "ListedExchCode", "Source", "DataAsOfDate"]
        listDelVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE, self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)]
        databaseOper.deleteRecord(stockMgtEffectivenessTable, listDelCols, listDelVals)
        del databaseOper
        
        # 2. mark delete old: update IsLatest to 'N' with same Ticker, ListedExch and Source
        databaseOper = clsDatabaseOper.DatabaseOper()
        listUpdCols = ["StockTicker", "ListedExchCode", "Source"]
        listUpdVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE]
        databaseOper.updateSingleValue(stockMgtEffectivenessTable, "IsLatest", "N", listUpdCols, listUpdVals)
        del databaseOper
        
        # 3. insert new record to DB
        databaseOper = clsDatabaseOper.DatabaseOper()
        listInstCols = ["StockTicker", "ListedExchCode", "Source", 
                        "ReturnOnAssets", "IndustryReturnOnAssets", "SectorReturnOnAssets", 
                        "ReturnOnAssets5YrAvg", "IndustryReturnOnAssets5YrAvg", "SectorReturnOnAssets5YrAvg", 
                        "ReturnOnInvestment", "IndustryReturnOnInvestment", "SectorReturnOnInvestment", 
                        "ReturnOnInvestment5YrAvg", "IndustryReturnOnInvestment5YrAvg", "SectorReturnOnInvestment5YrAvg", 
                        "ReturnOnEquity", "IndustryReturnOnEquity", "SectorReturnOnEquity", 
                        "ReturnOnEquity5YrAvg", "IndustryReturnOnEquity5YrAvg", "SectorReturnOnEquity5YrAvg", 
                        "DataAsOfDate"
                        ]
        
        listInstVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE, 
                        self.returnOnAssetsTtmComp, self.returnOnAssetsTtmIndustry, self.returnOnAssetsTtmSector, 
                        self.returnOnAssetsFiveYrAvgComp, self.returnOnAssetsFiveYrAvgIndustry, self.returnOnAssetsFiveYrAvgSector, 
                        self.returnOnInvestmentTtmComp, self.returnOnInvestmentTtmIndustry, self.returnOnInvestmentTtmSector, 
                        self.returnOnInvestmentFiveYrAvgComp, self.returnOnInvestmentFiveYrAvgIndustry, self.returnOnInvestmentFiveYrAvgSector, 
                        self.returnOnEquityTtmComp, self.returnOnEquityTtmIndustry, self.returnOnEquityTtmSector, 
                        self.returnOnEquityFiveYrAvgComp, self.returnOnEquityFiveYrAvgIndustry, self.returnOnEquityFiveYrAvgSector, 
                        self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)
                        ]
        
        databaseOper.insertListOfData(stockMgtEffectivenessTable, listInstVals, listInstCols)
        del databaseOper
        
        return None
    #end: writeUsStockManagementEffectivenessToDB
    
    
    def writeStockInstitutionalHoldersToDB(self):
        stockNewsTable = "tblStockDailySharesHolding"
        # 1. delete duplicate: del record with same Ticker, ListedExch, Source and DataAsOfDate
        databaseOper = clsDatabaseOper.DatabaseOper()
        listDelCols = ["StockTicker", "ListedExchCode", "Source"]
        listDelVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE]
        databaseOper.deleteRecord(stockNewsTable, listDelCols, listDelVals)
        del databaseOper
            
        # 2. mark delete old: update IsLatest to 'N' with same Ticker, ListedExch and Source
        databaseOper = clsDatabaseOper.DatabaseOper()
        listUpdCols = ["StockTicker", "ListedExchCode", "Source"]
        listUpdVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE]
        databaseOper.updateSingleValue(stockNewsTable, "IsLatest", "N", listUpdCols, listUpdVals)
        del databaseOper
            
        # 3. insert new record to DB
        databaseOper = clsDatabaseOper.DatabaseOper()
        listInstCols = ["StockTicker", "ListedExchCode", "Source", 
                        "TotalSharedHeldByInstitutions", "PercentageHeldByInstitutions", "NetSharesTradedByInstitutions",
                        "DataAsOfDate"
                        ]
            
        listInstVals = [self.compTicker, self.listedExchCode, self.DATA_SOURCE, 
                        self.sharesInstitHolderHeld, self.percentageInstitHolderHeld, self.netSharesInsiderTradedInThreeMonth,
                        self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)
                        ]
            
        databaseOper.insertListOfData(stockNewsTable, listInstVals, listInstCols)
        del databaseOper
        
        return None
    #end: writeStockInstitutionalHoldersToDB
    
    def getDatabaseTickerAndIndexBelong(self):
        databaseOper = clsDatabaseOper.DatabaseOper()

        dbColumns = ["StockTicker", "BelongToIndex"]
        listOfKeyCols = ["StockTicker", "ListedExchCode", "CompanyName", "Source", "Sector", "Industry", "IsLatest"]
        listOfKeyVals = [self.compTicker, self.listedExchCode, self.compName.replace('\'', '\\\''), self.DATA_SOURCE, self.sector, self.industry, "Y"]
        
        tickerAndIndexBelongDB = databaseOper.retrieveSelectMultiValues(self.DB_STOCK_STATIC_TBL, dbColumns, listOfKeyCols, listOfKeyVals)
        
        del databaseOper
        return tickerAndIndexBelongDB
    #end: getIndexBelong
    
    def updateDatabaseIndexBelong(self, indexBelong):
        databaseOper = clsDatabaseOper.DatabaseOper()
        
        dbColumn = "BelongToIndex"
        listOfKeyCols = ["StockTicker", "ListedExchCode", "CompanyName", "Source", "Sector", "Industry", "IsLatest"]
        listOfKeyVals = [self.compTicker, self.listedExchCode, self.compName.replace('\'', '\\\''), self.DATA_SOURCE, self.sector, self.industry, "Y"]
        
        indexBelong = databaseOper.updateSingleValue(self.DB_STOCK_STATIC_TBL, dbColumn, indexBelong, listOfKeyCols, listOfKeyVals)
        
        del databaseOper
        return indexBelong
    #end: updateIndexBelong
    
    def insertUsStockStaticToDatabase(self):
        databaseOper = clsDatabaseOper.DatabaseOper()

        listOfKeyCols = ["StockTicker", "ListedExchCode", "DataAsOfDate"]
        listOfKeyVals = [self.compTicker, self.listedExchCode, self.asOfDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)]
        listOfInCols = ["CompanyName", "Ric", "Source", "BelongToIndex", "Sector", "Industry"]
        listOfInVals = [self.compName.replace('\'', '\\\''), self.compRic, self.DATA_SOURCE, self.belongToIndex, self.sector, self.industry]
        
        databaseOper.insertIfNotExist(self.DB_STOCK_STATIC_TBL, listOfKeyCols, listOfKeyVals, listOfInCols, listOfInVals)
            
        del databaseOper
        return None 
    #end: insertIndexStaticToDatabase
    
#    def tryParseFloat(self, toFloat):
#        newFloat = 0 
#        try:
#            newFloat = float(toFloat)
#        except (ZeroDivisionError, ValueError) as ex:
#            newFloat = 0
#        return newFloat
#    #end: tryParseFloat
    
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
        """ print our Reuters Stock Information and composite details at defined order
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