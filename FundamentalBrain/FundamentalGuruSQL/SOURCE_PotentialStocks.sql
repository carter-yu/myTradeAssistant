#Remark: Fundamental Guru uses Revenue and percentage of Shares held by Institutions and Insider
SELECT DISTINCT
   #Static
   ss.StockTicker, ss.ListedExchCode, ss.CompanyName, ss.Ric, ss.Sector, ss.Industry, ss.BelongToIndex,
   #Reveue - Reuters,
   (rsr.EpsRegressGrowth * 100) EpsRegressGrowth_Reuters, 
   #Reveue - Nasdaq
   nsr.EpsRegressGrowth as EpsRegressGrowth_Nasdaq,
   #Reveue - Reuters
   rsr.M1QEps, rsr.M2QEps, rsr.M3QEps, rsr.M4QEps, rsr.M5QEps, rsr.M6QEps, rsr.M7QEps, rsr.M8QEps,
   rsr.M1QvsM2Q, rsr.M2QvsM3Q , rsr.M3QvsM4Q, rsr.M4QvsM5Q, rsr.M5QvsM6Q, rsr.M6QvsM7Q,rsr.M7QvsM8Q,   
   #Valuation   
   #nasdaq_benchmark_pe / nasdaq_benchmark_g
   (29.961 / 11.6) as NASDAQ_IDX_PEG,
   (sv.Pe / (rsr.EpsRegressGrowth * 100)) as PEG_Reuters,
   (sv.Pe / (nsr.EpsRegressGrowth)) as PEG_Nasdaq,
   sv.Pe, ((sv.Pe/sv.IndustryPe) - 1) as PEvsIndustry, ((sv.Pe/sv.SectorPe) - 1)  as PEvsSector, sv.IndustryPe, sv.SectorPe, 
   sv.Beta, sv.IndustryBeta, sv.SectorBeta,
   sv.5YrHighPe, sv.Industry5YrHighPe, sv.Sector5YrHighPe, sv.5YrLowPe, sv.Industry5YrLowPe, sv.Sector5YrLowPe, 
   #Mgt Effectivness
   se.ReturnOnEquity, se.IndustryReturnOnEquity, se.SectorReturnOnEquity, se.ReturnOnEquity5YrAvg, se.IndustryReturnOnEquity5YrAvg, se.SectorReturnOnEquity5YrAvg, 
   #Holding - Reuters
   rsh.PercentageHeldByInstitutions as PercentageHeldByInstitutions_Reuters, 
   #Holding - Nasdaq
   nsh.PercentageHeldByInstitutions as PercentageHeldByInstitutions_Nasdaq, nsh.NetSharesTradedByInstitutions, nsh.NetNumOfSharesTradedByInsidersIn3M,
   #Price
   #CASE WHEN ('IXIC' = ss.BelongToIndex) Then "Nasdaq" END,
   #price * ((benchmark_pe * compBeta) / compPe)
   ( sp.ClosePrice * ((29.961 * sv.Beta) / sv.Pe) ) as Fair_Price_PE,
   ( (( sp.ClosePrice * ((29.961 * sv.Beta) / sv.Pe) ) / sp.ClosePrice) - 1 ) as Fair_Price_PE_vs_Close_Price,
   #price * ((benchmark_peg * compBeta) / PEG_Reuters)
   (sp.ClosePrice * ( ((29.961 / 11.6) * sv.Beta / ( sv.Pe / (rsr.EpsRegressGrowth * 100) )) )) as Fair_Price_PEG_Reuters,
   (( (sp.ClosePrice * ( ((29.961 / 11.6) * sv.Beta / ( sv.Pe / (rsr.EpsRegressGrowth * 100) )) )) / sp.ClosePrice ) - 1) as Fair_Price_PEG_Reuters_vs_Close_Price,
   (sp.ClosePrice * ( ((29.961 / 11.6) * sv.Beta / ( sv.Pe / (nsr.EpsRegressGrowth) )) )) as Fair_Price_PEG_Nasdaq,
   (( (sp.ClosePrice * ( ((29.961 / 11.6) * sv.Beta / ( sv.Pe / (nsr.EpsRegressGrowth) )) )) / sp.ClosePrice ) - 1)  as Fair_Price_PEG_Nasdaq_vs_Close_Price,
   sp.ClosePrice, sp.52WkHigh, sp.52WkLow, ((sp.Volume / sp.AvgVolume) - 1) as VolumeChange, sp.Volume, sp.AvgVolume, 
   #Cash Flow
   sf.QuickRatio, sf.IndustryQuickRatio, sf.SectorQuickRatio, sf.TotalDebtToEquity, sf.IndustryTotalDebtToEquity, sf.SectorTotalDebtToEquity,
   sf.InterestCoverage, sf.IndustryInterestCoverage, sf.SectorInterestCoverage, 
   sng.PeterLynchAnalysis, sng.BenjaminGarhamAnalysis, sng.MomentumStrategyAnalysis, sng.JamesOShaughnessyAnalysis, 
   sng.MotleyFoolAnalysis, sng.DavidDremanAnalysis, sng.MartinZweigAnalysis, sng.KennethFisherAnalysis, 
   sp.DataAsOfDate, now() as CreateDate, 'Y' as IsLatest
 FROM 
    (select * from mytradeassistantdb.tblStockStatic where Source = 'Reuters' and IsLatest = 'Y') ss
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockRevenue where Source = 'Reuters' and IsLatest = 'Y') rsr
      ON (ss.StockTicker = rsr.StockTicker and ss.ListedExchCode = ss.ListedExchCode)
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockRevenue where Source = 'Nasdaq' and IsLatest = 'Y') nsr
      ON (ss.StockTicker = nsr.StockTicker and ss.ListedExchCode = nsr.ListedExchCode)
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockDailySharesHolding where Source = 'Reuters' and IsLatest = 'Y') rsh
      ON (ss.StockTicker = rsh.StockTicker and ss.ListedExchCode = rsh.ListedExchCode)
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockDailySharesHolding where Source = 'Nasdaq' and IsLatest = 'Y') nsh
      ON (ss.StockTicker = nsh.StockTicker and ss.ListedExchCode = nsh.ListedExchCode)
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockDailyValuation where IsLatest = 'Y') sv
      ON (ss.StockTicker = sv.StockTicker and ss.ListedExchCode = sv.ListedExchCode)
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockDailyManagementEffectiveness where IsLatest = 'Y') se
      ON (ss.StockTicker = se.StockTicker and ss.ListedExchCode = se.ListedExchCode)
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockDailyPrice where IsLatest = 'Y') sp
      ON (ss.StockTicker = sp.StockTicker and ss.ListedExchCode = sp.ListedExchCode)
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockDailyFinanicalStrength where IsLatest = 'Y') sf
      ON (ss.StockTicker = sf.StockTicker and ss.ListedExchCode = sf.ListedExchCode)
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockNasdaqGuru sng where IsLatest = 'Y') sng
      ON (ss.StockTicker = sng.StockTicker and ss.ListedExchCode = sng.ListedExchCode)
 WHERE 1=1
## Applied Strategic filtering 
   AND rsr.EpsRegressGrowth > 0 
   AND rsr.M1QEps > 0 AND rsr.M2QEps > 0 AND rsr.M3QEps > 0 AND rsr.M4QEps > 0 
   AND rsr.M5QEps > 0 AND rsr.M7QEps > 0 AND rsr.M8QEps > 0 
   AND rsh.NetSharesTradedByInstitutions > 0 
   AND (
        # as Fair_Price_PE_vs_Close_Price
        ( (( sp.ClosePrice * ((29.961 * sv.Beta) / sv.Pe) ) / sp.ClosePrice) - 1 ) > 0
        OR
        # as Fair_Price_PEG_Reuters_vs_Close_Price,
        (( (sp.ClosePrice * ( ((29.961 / 11.6) * sv.Beta / ( sv.Pe / (rsr.EpsRegressGrowth * 100) )) )) / sp.ClosePrice ) - 1)  > 0
        OR
        # as Fair_Price_PEG_Nasdaq_vs_Close_Price,
        (( (sp.ClosePrice * ( ((29.961 / 11.6) * sv.Beta / ( sv.Pe / (nsr.EpsRegressGrowth) )) )) / sp.ClosePrice ) - 1)  > 0
       )
## Strategic filtering - Good Earning
   #AND rsr.EpsRegressGrowth > 0 
   #AND rsr.M1QEps > 0 AND rsr.M2QEps > 0 AND rsr.M3QEps > 0 AND rsr.M4QEps > 0 
   #AND rsr.M5QEps > 0 AND rsr.M7QEps > 0 AND rsr.M8QEps > 0 
### Commented Out
## Strategic filtering - Good valuation
   #AND sv.PE <> 0 AND ((sv.Pe/sv.IndustryPe) - 1) < 0 AND ((sv.Pe/sv.SectorPe) - 1) < 0 
## Strategic filtering - Technical 
   #AND ((sp.Volume / sp.AvgVolume) - 1) > 0
## Strategic filtering - Shares in good hands
   #AND (nsh.PercentageHeldByInstitutions > 0.8 or nsh.PercentageHeldByInstitutions is null)
   #AND nsh.NetSharesTradedByInstitutions > 0 
ORDER BY PEG_Nasdaq ASC, PEG_Reuters ASC, sp.DataAsOfDate DESC