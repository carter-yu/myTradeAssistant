# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 15:13:24 2018

@author: Carter
"""

import sys
import traceback
import datetime

from GeneralTools import clsGeneralConstants
from GeneralTools import clsGeneralMethods

from FundamentalBrain import clsReutersMktIndexSourceOper
from FundamentalBrain import clsReutersMktIndexDataStructure
from FundamentalBrain import clsReutersUsStockSourceOper
from FundamentalBrain import clsNasdaqUsStockSourceOper
from StreetBrain import clsGoogleStockNewsOper
from FundamentalBrain import clsUsStockFundamentalGuru


#Start: Constatns
generalMethods = clsGeneralMethods.GeneralMethods()
NUM_OF_ITEMS = clsGeneralConstants.GeneralConstants.NUM_OF_ITEMS_TO_RANK
NUM_OF_ITEMS_HALF = int(generalMethods.tryParseFloat(NUM_OF_ITEMS)/2)

LIST_OF_FILES_TO_RANK= [ ["EpsRegressGrowth_Reuters",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "EpsRegressGrowth_Reuters_rm"],
                           ["EpsRegressGrowth_Nasdaq",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "EpsRegressGrowth_Nasdaq_rm"],
                           ["M1QEps",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "M1QEps_rm"],
                           ["M2QEps",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "M2QEps_rm"],
                           ["M3QEps",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "M3QEps_rm"],
                           ["M4QEps",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "M4QEps_rm"],
                           ["M1QvsM2Q",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "M1QvsM2Q_rm"],
                           ["M2QvsM3Q",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "M2QvsM3Q_rm"],
                           ["M3QvsM4Q",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "M3QvsM4Q_rm"],
                           ["PEG_Reuters",clsGeneralConstants.GeneralConstants.SQL_ASC_ORDER, NUM_OF_ITEMS, "PEG_Reuters_rm"],
                           ["PEG_Nasdaq",clsGeneralConstants.GeneralConstants.SQL_ASC_ORDER, NUM_OF_ITEMS, "PEG_Nasdaq_rm"],
                           ["PEvsIndustry",clsGeneralConstants.GeneralConstants.SQL_ASC_ORDER, NUM_OF_ITEMS, "PEvsIndustry_rm"],
                           ["PEvsSector",clsGeneralConstants.GeneralConstants.SQL_ASC_ORDER, NUM_OF_ITEMS, "PEvsSector_rm"],
                           ["ReturnOnEquity",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "ReturnOnEquity_rm"],
#                           ["PercentageHeldByInstitutions_Reuters",clsGeneralConstants.GeneralConstants.NUM_OF_ITEMS_HALF, NUM_OF_ITEMS, "PercentageHeldByInstitutions_Reuters_rm"],
                           ["PercentageHeldByInstitutions_Nasdaq",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "PercentageHeldByInstitutions_Nasdaq_rm"],
                           ["NetSharesTradedByInstitutions",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "NetSharesTradedByInstitutions_rm"],
                           ["NetNumOfSharesTradedByInsidersIn3M",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "NetNumOfSharesTradedByInsidersIn3M_rm"],
                           ["Fair_Price_PE_vs_Close_Price",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "Fair_Price_PE_vs_Close_Price_rm"],
                           ["Fair_Price_PEG_Reuters_vs_Close_Price",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "Fair_Price_PEG_Reuters_vs_Close_Price_rm"],
                           ["Fair_Price_PEG_Nasdaq_vs_Close_Price",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS, "Fair_Price_PEG_Nasdaq_vs_Close_Price_rm"],
                           ["PeterLynchAnalysis",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS_HALF, "PeterLynchAnalysis_rm"],
                           ["BenjaminGarhamAnalysis",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS_HALF, "BenjaminGarhamAnalysis_rm"],
                           ["MomentumStrategyAnalysis",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS_HALF, "MomentumStrategyAnalysis_rm"],
                           ["JamesOShaughnessyAnalysis",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS_HALF, "JamesOShaughnessyAnalysis_rm"],
                           ["MotleyFoolAnalysis",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS_HALF, "MotleyFoolAnalysis_rm"],
                           ["DavidDremanAnalysis",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS_HALF, "DavidDremanAnalysis_rm"],
                           ["MartinZweigAnalysis",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS_HALF, "MartinZweigAnalysis_rm"],
                           ["KennethFisherAnalysis",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS_HALF, "KennethFisherAnalysis_rm"],
                           ["VolumeChange",clsGeneralConstants.GeneralConstants.SQL_DESC_ORDER, NUM_OF_ITEMS_HALF, "VolumeChange_rm"]
                       ]
## end: Param for Ranking
ARGV_DAILY_PRICE = "DAILY_PRICE"
ARGV_NASDAQ_INFO = "NASDAQ_INFO"
ARGV_GOOGLE_NEWS = "GOOG_NEWS" 
PROGRESS_MILESTONE = 100
#End: Constatns


#Start: variables
startDateTime = datetime.datetime.now()
usStockFundamentalGuru = clsUsStockFundamentalGuru.UsStockFundamentalGuru() #for get Nasdaq, get Google, Set and Rank Potential
reutersSourceOper = None
reutersUsStockSourceOper = None
googleStockNewsOper = None

isDailyPrice = False
isNasdaqInfo = False
isGoogleNews = False
progressIdx = 1
#End: variables

googleStockNewsOper = clsGoogleStockNewsOper.GoogleStockNewsOper() #for Google News
googleStockNewsDataStructure = googleStockNewsOper.getUsStockNewsDataStruct("AAPL", "IXIC")
googleStockNewsDataStructure.writeUsStockNewsToDB()