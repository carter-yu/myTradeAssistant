SELECT 
  fg.StockTicker, 
  fg.ListedExchCode,
  replace(fg.CompanyName, '''', '"') as CompanyName,
  fg.Sector,
  fg.Industry,
  (fg.EpsRegressGrowth_Reuters_rm + fg.EpsRegressGrowth_Nasdaq_rm + fg.M1QEps_rm + 
   fg.M2QEps_rm + fg.M3QEps_rm + fg.M4QEps_rm + 
   fg.M1QvsM2Q_rm + fg.M2QvsM3Q_rm + fg.M3QvsM4Q_rm + 
   fg.PEG_Reuters_rm + fg.PEG_Nasdaq_rm + fg.PEvsIndustry_rm + 
   fg.PEvsSector_rm + fg.ReturnOnEquity_rm + fg.PercentageHeldByInstitutions_Reuters_rm + 
   fg.PercentageHeldByInstitutions_Nasdaq_rm + fg.NetSharesTradedByInstitutions_rm + 
   fg.NetNumOfSharesTradedByInsidersIn3M_rm + 
   fg.Fair_Price_PE_vs_Close_Price_rm + fg.Fair_Price_PEG_Reuters_vs_Close_Price_rm + fg.Fair_Price_PEG_Nasdaq_vs_Close_Price_rm + 
   fg.PeterLynchAnalysis_rm + fg.BenjaminGarhamAnalysis_rm + fg.MomentumStrategyAnalysis_rm + fg.JamesOShaughnessyAnalysis_rm + 
   fg.MotleyFoolAnalysis_rm + fg.DavidDremanAnalysis_rm + fg.MartinZweigAnalysis_rm + fg.KennethFisherAnalysis_rm + 
   fg.VolumeChange_rm
  ) as Total_Mark,
  (fg.Fair_Price_PE_vs_Close_Price_rm + fg.Fair_Price_PEG_Reuters_vs_Close_Price_rm + fg.Fair_Price_PEG_Nasdaq_vs_Close_Price_rm 
  ) as Total_Price_Valuation_Mark,
  (fg.PercentageHeldByInstitutions_Reuters_rm + fg.PercentageHeldByInstitutions_Nasdaq_rm + fg.NetSharesTradedByInstitutions_rm 
  ) as Total_Stock_Holder_Mark,
  (
    fg.PeterLynchAnalysis_rm + fg.BenjaminGarhamAnalysis_rm + fg.MomentumStrategyAnalysis_rm + fg.JamesOShaughnessyAnalysis_rm + 
    fg.MotleyFoolAnalysis_rm + fg.DavidDremanAnalysis_rm + fg.MartinZweigAnalysis_rm + fg.KennethFisherAnalysis_rm 
  ) as Total_Analyst_Mark,
   fg.EpsRegressGrowth_Reuters, fg.EpsRegressGrowth_Reuters_rm,
   fg.EpsRegressGrowth_Nasdaq, fg.EpsRegressGrowth_Nasdaq_rm,
   fg.M1QEps, fg.M1QEps_rm,
   fg.M2QEps, fg.M2QEps_rm,
   fg.M3QEps, fg.M3QEps_rm,
   fg.M4QEps, fg.M4QEps_rm,
   fg.M1QvsM2Q, fg.M1QvsM2Q_rm,
   fg.M2QvsM3Q, fg.M2QvsM3Q_rm,
   fg.M3QvsM4Q, fg.M3QvsM4Q_rm,
   fg.Pe,
   fg.PEG_Reuters, fg.PEG_Reuters_rm,
   fg.PEG_Nasdaq, fg.PEG_Nasdaq_rm,
   fg.PEvsIndustry, fg.PEvsIndustry_rm,
   fg.PEvsSector, fg.PEvsSector_rm,
   fg.ReturnOnEquity, fg.ReturnOnEquity_rm,
   fg.PercentageHeldByInstitutions_Nasdaq, fg.PercentageHeldByInstitutions_Nasdaq_rm,
   fg.NetSharesTradedByInstitutions, fg.NetSharesTradedByInstitutions_rm,
   fg.NetNumOfSharesTradedByInsidersIn3M, fg.NetNumOfSharesTradedByInsidersIn3M_rm,
   fg.ClosePrice, fg.Beta,
   fg.Fair_Price_PE, fg.Fair_Price_PE_vs_Close_Price_rm, 
   fg.Fair_Price_PEG_Reuters, fg.Fair_Price_PEG_Reuters_vs_Close_Price_rm, 
   fg.Fair_Price_PEG_Nasdaq, fg.Fair_Price_PEG_Nasdaq_vs_Close_Price_rm, 
   fg.PeterLynchAnalysis_rm, fg.BenjaminGarhamAnalysis_rm, fg.MomentumStrategyAnalysis_rm, fg.JamesOShaughnessyAnalysis_rm, 
   fg.MotleyFoolAnalysis_rm, fg.DavidDremanAnalysis_rm, fg.MartinZweigAnalysis_rm, fg.KennethFisherAnalysis_rm, 
   fg.VolumeChange, fg.VolumeChange_rm
FROM 
  mytradeassistantdb.tblFundamentalGuru fg 
WHERE
  IsLatest = 'Y'
ORDER BY Total_Mark desc
  ;
  
SELECT 
StockTicker, Source, NewsSource, NewsText,NewsUrl,
max(CreateDate) as CreateDate
FROM mytradeassistantdb.tblStockDailyNews sn
Where StockTicker in ('NVDA', 'HII', 'MBUU', 'YNDX', 'WM')
group by StockTicker, Source, NewsSource, NewsText,NewsUrl
order by StockTicker, CreateDate ;