DROP VIEW IF EXISTS vNoahZWIDailySimulatedActivity
GO
CREATE VIEW vNoahZWIDailySimulatedActivity
	AS 
	SELECT id, Symbol, ymd_R dateBought, LastOpen priceBought, yyyymmd_Offset dateSold, LastClose_Offset priceSold, Profit CapitalGain, RunningTotal 
	FROM stk.ZWIDailySimulatedActivity