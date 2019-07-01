Drop table mytradeassistantdb.tblIndexDailyPrice;

select * From mytradeassistantdb.tblExchange;

Delete From mytradeassistantdb.tblExchange Where ListedExchCode = 'NYSE';


Delete From mytradeassistantdb.tblIndex Where IndexCode = '.DJI' ;

select * From mytradeassistantdb.tblIndexStatic;
#Update mytradeassistantdb.tblIndexStatic set IsLatest = 'Y' where IndexCode in ('.DJI', '.IXIC', '.SPX');
select * From mytradeassistantdb.tblIndexDailyPrice;

select * From mytradeassistantdb.tblStockStatic;


SELECT count(1) FROM mytradeassistantdb.tblIndex WHERE IndexCode = '.DJI' AND IndexName = 'Dow Jones Industrial Average' AND Source = 'Reuters' AND DataAsOfDate = '2018-02-09 00:00' ; 



SELECT count(1) as rowCount FROM mytradeassistantdb.tblStockStatic WHERE StockTicker = 'GS' AND ListedExchCode = 'New York Stock Exchange' AND DataAsOfDate = '2018-02-09 00:00' ; 
SELECT * FROM mytradeassistantdb.tblStockStatic WHERE StockTicker = 'GS' AND ListedExchCode = 'New York Stock Exchange' AND DataAsOfDate = '2018-02-09 00:00' ; 
Delete FROM mytradeassistantdb.tblStockStatic WHERE StockTicker = 'GS' AND ListedExchCode = ' New York Stock Exchange' AND DataAsOfDate = '2018-02-09 00:00' ; 

INSERT INTO mytradeassistantdb.tblStockStatic(StockTicker, ListedExchCode, DataAsOfDate, CompanyName, Ric, Source, BelongToIndex, Sector, Industry) VALUES ('GS', ' New York Stock Exchange', '2018-02-09 00:00', 'Goldman Sachs Group Inc ', 'GS.N', 'Reuters', '', 'Financials', 'Investment Banking & Brokerage Services');


Select * From mytradeassistantdb.tblExchange;

#Delete from mytradeassistantdb.tblExchange Where ListedExchCode = "NYSE";

INSERT INTO mytradeassistantdb.tblExchange(ListedExchCode, ExchangeName, Source, DataAsOfDate) 
VALUES ('NYSE', 'New York Stock Exchange', 'Reuters', '2018-02-09 00:00');

INSERT INTO mytradeassistantdb.tblExchange(ListedExchCode, ExchangeName, Source, DataAsOfDate) 
VALUES ('IXIC', 'Nasdaq', 'Reuters', '2018-02-09 00:00');

INSERT INTO mytradeassistantdb.tblExchange(ListedExchCode, ExchangeName, Source, DataAsOfDate) 
VALUES ('IXIC', 'NASDAQ Stock Exchange Global Select Market', 'Reuters', '2018-02-09 00:00');


INSERT INTO mytradeassistantdb.tblExchange(ListedExchCode, ExchangeName, Source, DataAsOfDate) 
VALUES ('IXIC', 'NASDAQ Stock Exchange Global Market', 'Reuters', '2018-02-09 00:00');

INSERT INTO mytradeassistantdb.tblExchange(ListedExchCode, ExchangeName, Source, DataAsOfDate) 
VALUES ('IXIC', 'NASDAQ Stock Exchange Capital Market', 'Reuters', '2018-02-09 00:00');



# DELETE FROM mytradeassistantdb.tblStockStatic Where StockTicker = 'GS';

SELECT * FROM mytradeassistantdb.tblStockStatic;

SELECT * FROM mytradeassistantdb.tblStockStatic Where StockTicker = 'NVDA';
SELECT * FROM mytradeassistantdb.tblStockStatic Where StockTicker = 'ANET';
SELECT * FROM mytradeassistantdb.tblStockStatic Where StockTicker = 'MCO';
SELECT * FROM mytradeassistantdb.tblStockStatic Where StockTicker = 'HII' and isLatest = 'Y' and DataAsOfDate < '2018-04-04';
#Update mytradeassistantdb.tblStockStatic Set  isLatest = 'N' Where StockTicker = 'HII' and isLatest = 'Y' and DataAsOfDate < '2018-04-04';
SELECT * FROM mytradeassistantdb.tblStockStatic Where ric = 'CEMI.OQ';
SELECT * FROM mytradeassistantdb.tblStockStatic Where ric = 'DWDP.N';



##truncate mytradeassistantdb.tblStockStatic ;

SELECT BelongToIndex FROM mytradeassistantdb.tblStockStatic ;
SELECT distinct(BelongToIndex) FROM mytradeassistantdb.tblStockStatic ;

Select * From mytradeassistantdb.tblIndexDailyPrice; 

Select * From mytradeassistantdb.tblStockDailyPrice ;
Select * From mytradeassistantdb.tblStockDailyPrice Where IsLatest = 'Y' Order by CreateDate asc;
Select * From mytradeassistantdb.tblStockDailyPrice WHERE StockTicker = 'KBLM';

Select * From mytradeassistantdb.tblStockDailyPrice WHERE StockTicker = 'NVDA';
#DELETE From mytradeassistantdb.tblStockDailyPrice WHERE StockTicker = 'NVDA';

SELECT * FROM mytradeassistantdb.tblStockRevenue;
SELECT * FROM mytradeassistantdb.tblStockRevenue Where IsLatest = 'Y' ;
SELECT * FROM mytradeassistantdb.tblStockRevenue Where CreateDate > '2018-02-18';
SELECT * FROM mytradeassistantdb.tblStockRevenue WHERE M1QvsM2Q > 0 AND M2QvsM3Q > 0 AND M3QvsM4Q > 0 ; 
SELECT * FROM mytradeassistantdb.tblStockRevenue WHERE stockTicker = 'NVDA' ; 
SELECT * FROM mytradeassistantdb.tblStockRevenue WHERE stockTicker = 'ANET' ; 
SELECT * FROM mytradeassistantdb.tblStockRevenue WHERE stockTicker = 'XPLR' ; 
SELECT * FROM mytradeassistantdb.tblStockRevenue WHERE StockTicker = 'QRTEB' ;

##truncate mytradeassistantdb.tblStockRevenue ;

SELECT * FROM mytradeassistantdb.tblStockDailyNews;
SELECT sn.StockTicker, sn.ListedExchCode, count(1) FROM mytradeassistantdb.tblStockDailyNews sn GROUP BY sn.StockTicker, sn.ListedExchCode;

SELECT sn.StockTicker, sn.ListedExchCode, sn.DataAsOfDate, count(1) FROM mytradeassistantdb.tblStockDailyNews sn GROUP BY sn.StockTicker, sn.ListedExchCode, sn.DataAsOfDate;

SELECT * FROM mytradeassistantdb.tblStockDailyValuation Order by CreateDate desc;
SELECT * FROM mytradeassistantdb.tblStockDailyValuation WHERE stockTicker = 'NVDA' Order by CreateDate desc ; 

SELECT * FROM mytradeassistantdb.tblStockDailyFinanicalStrength;
DELETE FROM mytradeassistantdb.tblStockDailyFinanicalStrength WHERE StockTicker = 'KBLM';

SELECT * FROM mytradeassistantdb.tblStockDailyManagementEffectiveness;

SELECT * FROM mytradeassistantdb.tblStockDailySharesHolding;

SELECT * FROM mytradeassistantdb.tblStockDailySharesHolding
order by createdate desc;

SELECT 
sh.SharesOutstanding, sh.TotalSharedHeldByInstitutions, (sh.TotalSharedHeldByInstitutions/sh.SharesOutstanding) as InstitutionsPercentage
,sh.NetSharesTradedByInstitutions, sh.NetNumOfSharsTradedByInsidersIn3M, sh.NetNumOfSharsTradedByInsidersIn12M
,sh.* 
FROM mytradeassistantdb.tblStockDailySharesHolding sh ;
#Where ;

Select * FROM mytradeassistantdb.tblStockDailyNews sn Where sn.DataAsOfDate > '2018-04-01';

SELECT sn.StockTicker
FROM mytradeassistantdb.tblStockDailyNews sn
WHERE 1=1 
#AND sn.DataAsOfDate > '16 Feb 2018'
group by sn.StockTicker;

Select * FROM mytradeassistantdb.tblStockDailyNews sn Where sn.IsLatest = 'Y';

Select * FROM mytradeassistantdb.tblStockDailyNews sn Where sn.IsLatest = 'Y' and StockTicker = 'OMC'
Order by DataAsOfDate desc;

Select * FROM mytradeassistantdb.tblStockDailyNews sn Where sn.IsLatest = 'Y' And StockTicker in ('HII', 'IPCC', 'MBUU', 'SHW', 'UHAL');

Select * FROM mytradeassistantdb.tblStockDailyNews sn Where sn.IsLatest = 'N';

SELECT sn.StockTicker, sn.NewsSource, count(1) 
FROM mytradeassistantdb.tblStockDailyNews sn
WHERE 1=1 
AND sn.DataAsOfDate > '16 Feb 2018'
group by sn.StockTicker, sn.NewsSource
order by sn.StockTicker, sn.NewsSource;

SELECT news.StockTicker, news.NewsSource, count(1) as newsCount
    FROM mytradeassistantdb.tblStockDailyNews news
	WHERE 1=1 
	AND news.DataAsOfDate > '16 Feb 2018'
	GROUP BY news.StockTicker, news.NewsSource
	ORDER BY news.StockTicker, news.NewsSource ;

SELECT sn.NewsSource, count(1) 
FROM mytradeassistantdb.tblStockDailyNews sn
group by sn.NewsSource
order by count(1) desc;

SELECT sn.StockTicker, count(1) 
FROM mytradeassistantdb.tblStockDailyNews sn
group by sn.StockTicker
order by count(1) desc;

SELECT 
StockTicker, Source, NewsSource, NewsText,NewsUrl,
max(CreateDate) as CreateDate
FROM mytradeassistantdb.tblStockDailyNews sn
Where StockTicker in ('NVDA', 'HII', 'MBUU', 'YNDX', 'WM')
group by StockTicker, Source, NewsSource, NewsText,NewsUrl
order by StockTicker, CreateDate ;

SELECT ss.StockTicker, ss.Ric, ss.CompanyName, ss.Sector, ss.Industry,
sr.M1QvsM2Q, sr.M2QvsM3Q , sr.M3QvsM4Q,
sr.M4QvsM5Q, sr.M5QvsM6Q, sr.M6QvsM7Q,
sr.M7QvsM8Q,
sr.M1QEps, sr.M2QEps, sr.M3QEps 
 FROM mytradeassistantdb.tblStockStatic ss
 ,mytradeassistantdb.tblStockRevenue sr
 WHERE 1=1
 AND ss.StockTicker = sr.StockTicker
 AND  sr.M1QvsM2Q >= 0 AND sr.M2QvsM3Q >= 0 AND sr.M3QvsM4Q >= 0 
 AND  sr.M4QvsM5Q >= 0 AND sr.M5QvsM6Q >= 0 AND sr.M6QvsM7Q >= 0 
 AND sr.M7QvsM8Q >= 0 
 AND sr.M1QEps > 0 AND sr.M2QEps > 0 AND sr.M3QEps > 0 
 AND sr.M4QEps > 0 AND sr.M5QEps > 0 
 AND sr.M7QEps > 0 AND sr.M8QEps > 0 ; 
 
SELECT ss.Sector, ss.Industry, count(1)
 FROM mytradeassistantdb.tblStockStatic ss
 ,mytradeassistantdb.tblStockRevenue sr
 WHERE 1=1
 AND ss.StockTicker = sr.StockTicker
 AND  sr.M1QvsM2Q > 0 AND sr.M2QvsM3Q > 0 AND sr.M3QvsM4Q > 0 
 AND sr.M1QEps > 0 AND sr.M2QEps > 0 AND sr.M3QEps > 0 
GROUP BY ss.Sector, ss.Industry; 


select * from mytradeassistantdb.tblStockDailySharesHolding ;
select * from mytradeassistantdb.tblStockDailySharesHolding WHERE StockTicker = 'TCBI';

select * from mytradeassistantdb.tblStockDailySharesHolding Where IsLatest = 'Y' And Source = 'Nasdaq';

SELECT * FROM mytradeassistantdb.tblStockRevenue WHERE StockTicker = 'AAME';
select * from mytradeassistantdb.tblStockDailySharesHolding WHERE StockTicker = 'AAME';

#UPDATE mytradeassistantdb.tblStockDailySharesHolding SET IsLatest = 'N' ; 

Select * From mytradeassistantdb.tblStockNasdaqGuru WHERE IsLatest = 'Y';

SELECT fg.* FROM mytradeassistantdb.tblFundamentalGuru fg ;
SELECT fg.* FROM mytradeassistantdb.tblFundamentalGuru fg WHERE StockTicker in ('ANET', 'HII', 'MBUU', 'NVDA', 'WM', 'YNDX')
Order by StockTicker asc, CreateDate desc;
SELECT fg.* FROM mytradeassistantdb.tblFundamentalGuru fg WHERE IsLatest = 'Y';
#Update mytradeassistantdb.tblFundamentalGuru set EpsRegressGrowth_Nasdaq_rm = 0 ;
SELECT DATE_FORMAT(fg.CreateDate, '%Y_%m_%d'), DATE_FORMAT(now(), '%Y_%m_%d'), fg.* From mytradeassistantdb.tblFundamentalGuru fg ; 


#DELETE From mytradeassistantdb.tblFundamentalGuru;
#UPDATE mytradeassistantdb.tblFundamentalGuru SET IsLatest = 'N' Where StockTicker = '';
