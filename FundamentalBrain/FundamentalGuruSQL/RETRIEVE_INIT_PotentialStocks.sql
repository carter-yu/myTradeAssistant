#Remark: Fundamental Guru uses Revenue and percentage of Shares held by Institutions and Insider as Base
SELECT 
    rsr.StockTicker, rsr.ListedExchCode
  FROM
    (select * from mytradeassistantdb.tblStockRevenue where Source = 'Reuters' and IsLatest = 'Y') rsr
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockRevenue where Source = 'Nasdaq' and IsLatest = 'Y') nsr
      ON (rsr.StockTicker = nsr.StockTicker and rsr.ListedExchCode = nsr.ListedExchCode)
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockDailySharesHolding where Source = 'Reuters' and IsLatest = 'Y') rsh
      ON (rsr.StockTicker = rsh.StockTicker and rsr.ListedExchCode = rsh.ListedExchCode)
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockDailySharesHolding where Source = 'Nasdaq' and IsLatest = 'Y') nsh
      ON (rsr.StockTicker = nsh.StockTicker and rsr.ListedExchCode = nsh.ListedExchCode)
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockDailyValuation where IsLatest = 'Y') sv
      ON (rsr.StockTicker = sv.StockTicker and rsr.ListedExchCode = sv.ListedExchCode)
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockDailyManagementEffectiveness where IsLatest = 'Y') sm
      ON (rsr.StockTicker = sm.StockTicker and rsr.ListedExchCode = sm.ListedExchCode)
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockDailyPrice where IsLatest = 'Y') sp
      ON (rsr.StockTicker = sp.StockTicker and rsr.ListedExchCode = sp.ListedExchCode)
    LEFT OUTER JOIN (select * from mytradeassistantdb.tblStockDailyFinanicalStrength where IsLatest = 'Y') se
      ON (rsr.StockTicker = se.StockTicker and rsr.ListedExchCode = se.ListedExchCode)
 WHERE 1=1
## Applied Strategic filtering 
   AND rsr.EpsRegressGrowth > 0 
   AND rsr.M1QEps > 0 AND rsr.M2QEps > 0 AND rsr.M3QEps > 0 AND rsr.M4QEps > 0 
   AND rsr.M5QEps > 0 AND rsr.M7QEps > 0 AND rsr.M8QEps > 0 
   AND rsh.NetSharesTradedByInstitutions > 0 
   AND (
        # as Fair_Price_PE_vs_Close_Price
        ( (( sp.ClosePrice * ((25.179 * sv.Beta) / sv.Pe) ) / sp.ClosePrice) - 1 ) > 0
        OR
        # as Fair_Price_PEG_Reuters_vs_Close_Price,
        (( (sp.ClosePrice * ( ((25.179 / 11.6) * sv.Beta / ( sv.Pe / (rsr.EpsRegressGrowth * 100) )) )) / sp.ClosePrice ) - 1)  > 0
        OR
        # as Fair_Price_PEG_Nasdaq_vs_Close_Price,
        (( (sp.ClosePrice * ( ((25.179 / 11.6) * sv.Beta / ( sv.Pe / (nsr.EpsRegressGrowth) )) )) / sp.ClosePrice ) - 1)  > 0
       )
## Strategic filtering - Good Earning
   #AND rsr.M1QvsM2Q >= 0 AND rsr.M2QvsM3Q >= 0 AND rsr.M3QvsM4Q >= 0 AND rsr.M4QvsM5Q >= 0 
   #AND rsr.M5QvsM6Q >= 0 AND rsr.M6QvsM7Q >= 0 AND rsr.M7QvsM8Q >= 0 
   #AND rsr.EpsRegressGrowth > 0 
   #AND rsr.M1QEps > 0 AND rsr.M2QEps > 0 AND rsr.M3QEps > 0 AND rsr.M4QEps > 0 
   #AND rsr.M5QEps > 0 AND rsr.M7QEps > 0 AND rsr.M8QEps > 0 
## Strategic filtering - Shares in good hands
   #AND (rsh.PercentageHeldByInstitutions > 90 or rsh.PercentageHeldByInstitutions is null)
   #AND rsh.NetSharesTradedByInstitutions > 0 
   #AND (nsh.NetNumOfSharesTradedByInsidersIn3M >= 0 or nsh.NetNumOfSharesTradedByInsidersIn3M is null)
## Strategic filtering - Good valuation
   #AND sv.PE <> 0 AND ((sv.Pe/sv.IndustryPe) - 1) < 0 AND ((sv.Pe/sv.SectorPe) - 1) < 0 
## Strategic filtering - Technical 
   #AND ((sp.Volume / sp.AvgVolume) - 1) > 0
ORDER BY rsr.StockTicker ASC
   ; 