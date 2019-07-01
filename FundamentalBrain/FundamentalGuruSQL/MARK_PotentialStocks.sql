#Remark: Fundamental Guru uses Revenue and percentage of Shares held by Institutions and Insider as Base
SELECT 
  StockTicker,
  ListedExchCode,
  <-CheckFieldParam->
FROM 
  mytradeassistantdb.tblFundamentalGuru
WHERE
  IsLatest = 'Y'
ORDER BY <-CheckFieldParam-> <-SortParam->
LIMIT <-CheckItems->
  ;