CREATE VIEW vNoahCaseStudy2_simulationDailyPerformance
AS
SELECT S1.yyyymmd_Offset, S1.TradingBalance
,CAST (100 * (S1.TradingBalance - S2.TradingBalance)/S2.TradingBalance AS decimal(10,2)) capitalGainPercentage
FROM (
	SELECT yyyymmd_Offset, TradingBalance
	, MIN (yyyymmd_Offset) OVER (ORDER BY yyyymmd_Offset) yyyymmdd_first_date
	FROM (
	SELECT DISTINCT yyyymmd_Offset, TradingBalance
	FROM stk.ZWIDailySimulatedActivity 
	) OS
) S1
JOIN
(
	SELECT DISTINCT yyyymmd_Offset, TradingBalance
	FROM stk.ZWIDailySimulatedActivity 
	) S2
	ON S1.yyyymmdd_first_date = S2.yyyymmd_Offset