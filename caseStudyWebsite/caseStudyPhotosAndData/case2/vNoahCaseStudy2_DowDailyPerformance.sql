CREATE VIEW vNoahCaseStudy2_DowDailyPerformance
AS
SELECT S1.yyyymmdd,S1.LastClose 
--, S2.LastClose lastClose_first_value
, CAST (100 * (S1.LastClose - S2.LastClose)/S2.LastClose AS decimal(10,2)) capitalGainPercentage
FROM 
(
	SELECT OS.yyyymmdd, OS.LastClose
	, MIN (OS.yyyymmdd) OVER (ORDER BY OS.yyyymmdd) yyyymmdd_first_date
	FROM 
	(
		SELECT yyyymmdd, LastClose
		FROM stk.StockProperties
		WHERE StockIDPK = 4684
		AND yyyymmdd >= (SELECT MIN(yyyymmd_Offset) from vNoahCaseStudy2_simulationDailyPerformance)
	) OS
) S1
JOIN 
(
	SELECT yyyymmdd, LastClose
	FROM stk.StockProperties
	WHERE StockIDPK = 4684
) S2 
ON S1.yyyymmdd_first_date = S2.yyyymmdd
