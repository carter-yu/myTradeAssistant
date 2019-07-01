SELECT 
   #Static
   ss.StockTicker, ss.Ric, ss.CompanyName, ss.Sector, ss.Industry, 
   # Google News
   sn.NewsSource, sn.NewsText, sn.DataAsOfDate, sn.CreateDate, sn.NewsUrl,
   #Reveue - Reuters,
   (rsr.EpsRegressGrowth * 100) EpsRegressGrowth_Reuters, 
   #Reveue - Nasdaq
   nsr.EpsRegressGrowth as EpsRegressGrowth_Nasdaq,
   #Reveue - Reuters
   rsr.M1QEps, rsr.M2QEps, rsr.M3QEps, rsr.M4QEps, rsr.M5QEps, rsr.M6QEps, rsr.M7QEps, rsr.M8QEps,
   #rsr.M1QvsM2Q, rsr.M2QvsM3Q , rsr.M3QvsM4Q, rsr.M4QvsM5Q, rsr.M5QvsM6Q, rsr.M6QvsM7Q,rsr.M7QvsM8Q,   
   #Valuation
   (sv.Pe / (rsr.EpsRegressGrowth * 100)) as PEG_Reuters,
   (sv.Pe / (nsr.EpsRegressGrowth)) as PEG_Nasdaq
 FROM 
   mytradeassistantdb.tblStockStatic ss 
      LEFT JOIN mytradeassistantdb.tblStockRevenue rsr ON ss.StockTicker = rsr.StockTicker
      LEFT JOIN mytradeassistantdb.tblStockRevenue nsr ON ss.StockTicker = nsr.StockTicker
      LEFT JOIN mytradeassistantdb.tblStockDailyValuation sv ON ss.StockTicker = sv.StockTicker
      LEFT JOIN mytradeassistantdb.tblStockDailyManagementEffectiveness se ON ss.StockTicker = se.StockTicker
      LEFT JOIN mytradeassistantdb.tblStockDailySharesHolding rsh ON ss.StockTicker = rsh.StockTicker
      LEFT JOIN mytradeassistantdb.tblStockDailySharesHolding nsh ON ss.StockTicker = nsh.StockTicker
      LEFT JOIN mytradeassistantdb.tblStockDailyPrice sp ON ss.StockTicker = sp.StockTicker
      LEFT JOIN mytradeassistantdb.tblStockDailyFinanicalStrength sf ON ss.StockTicker = sf.StockTicker
	  LEFT JOIN mytradeassistantdb.tblStockDailyNews sn ON ss.StockTicker = sn.StockTicker
 WHERE 1=1
   AND (rsr.IsLatest = 'Y' or rsr.IsLatest is null)
   AND (rsr.Source = 'Reuters' or rsr.IsLatest is null)
   AND (nsr.IsLatest = 'Y' or nsr.IsLatest is null)
   AND (nsr.Source = 'Nasdaq' or nsr.IsLatest is null)
   AND (sv.IsLatest = 'Y' or sv.IsLatest is null)
   AND (se.IsLatest = 'Y' or se.IsLatest is null)
   AND (rsh.IsLatest = 'Y' or rsh.IsLatest is null) 
   AND (rsh.Source = 'Reuters' or rsh.Source is null) 
   AND (nsh.IsLatest = 'Y' or nsh.IsLatest is null) 
   AND (nsh.Source = 'Nasdaq' or nsh.Source is null) 
   AND (sp.IsLatest = 'Y' or sp.IsLatest is null)
   AND (sf.IsLatest = 'Y' or sf.IsLatest is null)
   AND (sn.IsLatest = 'Y' or sn.IsLatest is null)
## Strategic filtering - Good Earning
   #AND rsr.M1QvsM2Q >= 0 AND rsr.M2QvsM3Q >= 0 AND rsr.M3QvsM4Q >= 0 AND rsr.M4QvsM5Q >= 0 
   #AND rsr.M5QvsM6Q >= 0 AND rsr.M6QvsM7Q >= 0 AND rsr.M7QvsM8Q >= 0 
   AND rsr.EpsRegressGrowth > 0 
   AND nsr.EpsRegressGrowth > 0 
   AND rsr.M1QEps > 0 AND rsr.M2QEps > 0 AND rsr.M3QEps > 0 AND rsr.M4QEps > 0 
   AND rsr.M5QEps > 0 AND rsr.M7QEps > 0 AND rsr.M8QEps > 0 
## Strategic filtering - Shares in good hands
   #AND (nsh.PercentageHeldByInstitutions > 0.8 or nsh.PercentageHeldByInstitutions is null)
   #AND nsh.NetSharesTradedByInstitutions > 0 
   AND (nsh.NetNumOfSharesTradedByInsidersIn3M >= 0 or nsh.NetNumOfSharesTradedByInsidersIn3M is null)
## Strategic filtering - Good valuation
   #AND sv.PE <> 0 AND ((sv.Pe/sv.IndustryPe) - 1) < 0 AND ((sv.Pe/sv.SectorPe) - 1) < 0 
## Strategic filtering - Technical 
   AND ((sp.Volume / sp.AvgVolume) - 1) > 0
ORDER BY PEG_Nasdaq ASC, PEG_Reuters ASC, sn.DataAsOfDate DESC
   ; 