
SELECT count(1) FROM mytradeassistantdb.tblexchange;
#5
SELECT count(1) FROM mytradeassistantdb.tblindexdailyprice;
#3
SELECT count(1) FROM mytradeassistantdb.tblindexstatic;
#3
SELECT count(1) FROM mytradeassistantdb.tblstockdailyfinanicalstrength;
#4119
SELECT count(1) FROM mytradeassistantdb.tblstockdailymanagementeffectiveness;
#4119
SELECT count(1) FROM mytradeassistantdb.tblstockdailyprice;
#4120
SELECT count(1) FROM mytradeassistantdb.tblstockdailyvaluation;
#4121
SELECT count(1) FROM mytradeassistantdb.tblstockrevenue;
#4121
SELECT count(1) FROM mytradeassistantdb.tblstockstatic;
#2917
SELECT count(1) FROM mytradeassistantdb.tblStockDailySharesHolding;
#4625
SELECT count(1) FROM mytradeassistantdb.tblStockDailyNews;
#22668


##########################################################################################

SELECT count(1) FROM mytradeassistantdb.tblstockdailyfinanicalstrength WHERE IsLatest = 'Y';
#2914
SELECT count(1) FROM mytradeassistantdb.tblstockdailymanagementeffectiveness WHERE IsLatest = 'Y';
#2914
SELECT count(1) FROM mytradeassistantdb.tblstockdailyprice WHERE IsLatest = 'Y';
#2916
SELECT count(1) FROM mytradeassistantdb.tblstockdailyvaluation WHERE IsLatest = 'Y';
#2916
SELECT count(1) FROM mytradeassistantdb.tblstockrevenue WHERE IsLatest = 'Y';
#2916
SELECT count(1) FROM mytradeassistantdb.tblstockstatic WHERE IsLatest = 'Y';
#2917
SELECT count(1) FROM mytradeassistantdb.tblStockDailySharesHolding WHERE IsLatest = 'Y' AND Source = 'Nasdaq';
#2654

SELECT * FROM mytradeassistantdb.tblStockDailySharesHolding WHERE IsLatest = 'Y';




SELECT * FROM mytradeassistantdb.tblstockstatic WHERE IsLatest = 'Y' AND StockTicker = 'PCLN';

SELECT StockTicker, count(1) 
FROM mytradeassistantdb.tblstockstatic 
WHERE IsLatest = 'Y'
GROUP BY StockTicker
HAVING count(1) > 1;

##Delete FROM mytradeassistantdb.tblstockstatic WHERE IsLatest = 'Y' AND StockTicker = 'PCLN' AND CompanyName = 'Booking Holdings Inc ' ;