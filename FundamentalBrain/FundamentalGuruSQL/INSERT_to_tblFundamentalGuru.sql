# 1. Mark Delete Old Stock Static Records 
UPDATE mytradeassistantdb.tblStockStatic ss_up 
  INNER JOIN ( 
			 select 
             StockTicker, ListedExchCode, CompanyName, 
             Ric, Sector, Industry, 
             BelongToIndex , count(1) as stock_count, max(DataAsOfDate) as max_DataAsOfDate 
             from mytradeassistantdb.tblStockStatic 
             where Source = 'Reuters' and IsLatest = 'Y' 
             group by StockTicker, ListedExchCode 
             having count(1) > 1 ) ss_d 
ON (ss_up.StockTicker = ss_d.StockTicker  
AND ss_up.ListedExchCode = ss_d.ListedExchCode 
AND ss_up.DataAsOfDate <> ss_d.max_DataAsOfDate) 
SET ss_up.isLatest = 'N' 
; 

# 2. Delete Same date records for re-run
DELETE FROM mytradeassistantdb.tblFundamentalGuru WHERE DATE_FORMAT(CreateDate, '%Y_%m_%d') = DATE_FORMAT(now(), '%Y_%m_%d'); 

# 3. Delete Duplicated with same "As of Date"
CREATE TEMPORARY TABLE IF NOT EXISTS mytradeassistantdb.TEMP_DUP_AS_OF_DATE AS 
( 
  SELECT StockTicker, DataAsOfDate 
  FROM mytradeassistantdb.tblFundamentalGuru 
  WHERE IsLatest = 'Y' 
  AND ROW(StockTicker, DataAsOfDate) in 
  ( 
    select fg.StockTicker, fg.DataAsOfDate 
    from mytradeassistantdb.tblFundamentalGuru fg 
    where fg.IsLatest = 'N' 
  ) 
) 
;
DELETE FROM mytradeassistantdb.tblFundamentalGuru 
WHERE IsLatest = 'Y' 
AND ROW(StockTicker, DataAsOfDate) IN 
(
  select tdd.StockTicker, tdd.DataAsOfDate 
  from mytradeassistantdb.TEMP_DUP_AS_OF_DATE tdd 
); 
DROP TABLE mytradeassistantdb.TEMP_DUP_AS_OF_DATE; 

# 4. Mark Delete other Old records
UPDATE mytradeassistantdb.tblFundamentalGuru SET IsLatest = 'N'; 

# 5. Insert the New Potential records
INSERT INTO mytradeassistantdb.tblFundamentalGuru 
 (StockTicker, ListedExchCode, CompanyName, Ric, Sector, Industry, BelongToIndex, 
  EpsRegressGrowth_Reuters, 
  EpsRegressGrowth_Nasdaq, 
  M1QEps, M2QEps, M3QEps, M4QEps, M5QEps, M6QEps, M7QEps, M8QEps, 
  M1QvsM2Q, M2QvsM3Q, M3QvsM4Q, M4QvsM5Q, M5QvsM6Q, M6QvsM7Q, M7QvsM8Q, 
  NASDAQ_IDX_PEG, 
  PEG_Reuters, 
  PEG_Nasdaq, 
  Pe, PEvsIndustry, PEvsSector, IndustryPe, SectorPe, 
  Beta, IndustryBeta, SectorBeta, 
  5YrHighPe, Industry5YrHighPe, Sector5YrHighPe, 5YrLowPe, Industry5YrLowPe, Sector5YrLowPe, 
  ReturnOnEquity, IndustryReturnOnEquity, SectorReturnOnEquity, ReturnOnEquity5YrAvg, 
  IndustryReturnOnEquity5YrAvg, SectorReturnOnEquity5YrAvg, 
  PercentageHeldByInstitutions_Reuters, 
  PercentageHeldByInstitutions_Nasdaq, NetSharesTradedByInstitutions, NetNumOfSharesTradedByInsidersIn3M, 
  Fair_Price_PE, 
  Fair_Price_PE_vs_Close_Price, 
  Fair_Price_PEG_Reuters, 
  Fair_Price_PEG_Reuters_vs_Close_Price, 
  Fair_Price_PEG_Nasdaq, 
  Fair_Price_PEG_Nasdaq_vs_Close_Price, 
  ClosePrice, 52WkHigh, 52WkLow, VolumeChange, Volume, AvgVolume, 
  QuickRatio, IndustryQuickRatio, SectorQuickRatio, TotalDebtToEquity, IndustryTotalDebtToEquity, SectorTotalDebtToEquity, 
  InterestCoverage, IndustryInterestCoverage, SectorInterestCoverage, 
  PeterLynchAnalysis, BenjaminGarhamAnalysis, MomentumStrategyAnalysis, JamesOShaughnessyAnalysis, 
  MotleyFoolAnalysis, DavidDremanAnalysis, MartinZweigAnalysis, KennethFisherAnalysis, 
  DataAsOfDate, CreateDate, IsLatest 
 )  
<-potentialSQL->