# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 11:22:16 2018

@author: Carter
"""
import datetime

class GeneralConstants(object):
    #Log files variables
    LOG_FILENAME_DATE = "%Y_%m_%d_%H%M_"
    LOG_FILE_PATH = "Logs/" + datetime.datetime.now().strftime(LOG_FILENAME_DATE) + "myTradeAssistant.log"
    LOG_RECORD_DATE = "[%b %d, %Y (%a) %H:%M.%S] "
    # Date Formats
    DATA_RECORD_DATE_FORMAT = "%Y-%m-%d %H:%M"
    DATA_AS_OF_DATE_FORMAT = "%Y_%m_%d"
    EPS_GRAPH_DATE_FORMAT = "%y%m"
    
    DEFAULT_COLUMN_SEP = ","
    
    SQL_DESC_ORDER = "DESC"
    SQL_ASC_ORDER = "ASC"
    SQL_IS_LATEST_TRUE = "Y" 
    
    NUM_OF_ITEMS_TO_RANK = "21"
    TOTAL_RANK_MARKS = 20