# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 13:31:41 2018

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

class GoogleStockNewsDataStructure(object):
    DATA_SOURCE = "Google"
    GOOGLE_NEWS_URL = "https://news.google.com/news/"
    GOOGLE_DATE_FORMAT = "%b %d, %Y"
    
    def __init__(self, _stockTicker, _exchangeCode):
        self.generalMethods = clsGeneralMethods.GeneralMethods()
        self.stockTicker = _stockTicker
        self.exchangeCode = _exchangeCode
        self.relatedGoogleStoriesUrls = []
        self.stockNewsList = []
#        self.googleNewsStoryPage = None
    #end: __init__
    
    def loadDataFromWeb(self, googleNewsExploreUrl):
        # get the web page
        self.generalMethods.printLog("Google News: self.stockTicker = " + self.stockTicker + " , self.exchangeCode = " + self.exchangeCode)
        #Scrape the Google Story URL
        self.scrapeNewsStoryUrl(googleNewsExploreUrl)
        self.scrapeNews()
        
        return None
    #end: loadDataFromWeb
    
## Web Scrape
## Web Scrape
## Web Scrape
    def scrapeNewsStoryUrl(self, explorePageUrl):
        browser = mechanicalsoup.StatefulBrowser()
        browser.open(explorePageUrl)
        googleNewsExplorePage = browser.get_current_page()
        
        aLinks = googleNewsExplorePage.findAll("a")
        for aLink in aLinks:
            aLinHref = aLink.attrs["href"]
            if( -1 != aLinHref.lower().find("story") ):
                storyUrl = self.GOOGLE_NEWS_URL + aLink.attrs["href"]
                self.relatedGoogleStoriesUrls.append(storyUrl)

        return None
    #end: scrapeNewsStoryUrl
    
    def scrapeNews(self):
        listOfUrls = []
        for relatedGoogleStoriesUrl in self.relatedGoogleStoriesUrls:
            
            browser = mechanicalsoup.StatefulBrowser()
            browser.open(relatedGoogleStoriesUrl)
            googleNewsPage = browser.get_current_page()
            
            mainContent = googleNewsPage.find("main")
            if ( None != mainContent ):
                contentWizards = mainContent.findAll("c-wiz")
                
                if( None != contentWizards ):
                    for contentWizard in contentWizards:
                        
                        newsLinks = contentWizard.findAll("a")
                        if(None != newsLinks):
                            linkText = ""
                            linkUrl = ""
                            linkSource = ""
                            linkDate = ""
                            for newsLink in newsLinks:
                                sourceSpan = newsLink.findNext("span")
                                if(None != sourceSpan):
                                    dateSpan = sourceSpan.findNext("span")
                                    linkText = newsLink.text
                                    linkUrl = newsLink.attrs["href"]
                                    linkSource = sourceSpan.text.strip()
                                    linkDate = dateSpan.text.strip()
                                    linkDate = linkDate[:-1]
                                    if( (-1 != linkDate.lower().find("ago")) or (-1 != linkDate.lower().find("now")) ):
                                        linkDate = time.strftime(self.GOOGLE_DATE_FORMAT)

                                    if( "http" != linkUrl[0:4].lower() ):
                                        if( ("" != linkText) and ("" != linkUrl) and
                                           ("" != linkSource) and ("" != linkDate) ):
                                            if linkUrl not in listOfUrls:
                                                listOfUrls.append(linkUrl)
                                                newStockNews = [linkDate, linkSource, linkText, linkUrl]
                                                self.stockNewsList.append(newStockNews)
#                                                print("self.stockNewsList", self.stockNewsList)
        return None
    #end: scrapeNews

## Write to DB     
## Write to DB 
## Write to DB     
    def writeUsStockNewsToDB(self):
        stockNewsTable = "tblStockDailyNews"
        
#        print("self.stockNewsList", self.stockNewsList)
        for stockNews in self.stockNewsList:
            try:
                newsDate = datetime.datetime.strptime(stockNews[0], self.GOOGLE_DATE_FORMAT)
            except ValueError as timeError:
                newsDate = datetime.datetime.now()
                
            newsSource = stockNews[1].replace("'", "''")
            newsText = stockNews[2].replace("'", "''")
            newsUrl =stockNews[3].replace("'", "''")
    #        
            # 1. delete duplicate: del record with same Ticker, ListedExch, Source and DataAsOfDate
            databaseOper = clsDatabaseOper.DatabaseOper()
            listDelCols = ["StockTicker", "ListedExchCode", "Source", "DataAsOfDate"]
            listDelVals = [self.stockTicker, self.exchangeCode, self.DATA_SOURCE, newsDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)]
            databaseOper.deleteRecord(stockNewsTable, listDelCols, listDelVals)
            del databaseOper
            
    #        # 2. mark delete old: update IsLatest to 'N' with same Ticker, ListedExch and Source
    #        databaseOper = clsDatabaseOper.DatabaseOper()
    #        listUpdCols = ["StockTicker", "ListedExchCode", "Source"]
    #        listUpdVals = [self.stockTicker, self.exchangeCode, self.DATA_SOURCE]
    #        databaseOper.updateSingleValue(stockNewsTable, "IsLatest", "N", listUpdCols, listUpdVals)
    #        del databaseOper
    #        
            # 3. insert new record to DB
            databaseOper = clsDatabaseOper.DatabaseOper()
            listInstCols = ["StockTicker", "ListedExchCode", "Source", 
                            "NewsSource", "NewsText", "NewsUrl", 
                            "DataAsOfDate"
                            ]
            
            listInstVals = [self.stockTicker, self.exchangeCode, self.DATA_SOURCE, 
                            newsSource, newsText, newsUrl,
                            newsDate.strftime(clsGeneralConstants.GeneralConstants.DATA_AS_OF_DATE_FORMAT)
                            ]
            
#            print("listInstVals=",listInstVals)
            databaseOper.insertListOfData(stockNewsTable, listInstVals, listInstCols)
            del databaseOper
        
        return None
    #end: writeUsStockNewsToDB

    
    def tryParseFloat(self, toFloat):
        newFloat = 0 
        try:
            newFloat = float(toFloat)
        except (ZeroDivisionError, ValueError) as ex:
            newFloat = 0
        return newFloat
    #end: tryParseFloat
