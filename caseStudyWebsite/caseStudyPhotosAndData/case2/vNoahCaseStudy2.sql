DROP VIEW IF EXISTS vNoahCaseStudy2
GO

CREATE VIEW vNoahCaseStudy2
AS
SELECT yyyymmd_Offset ymd, TradingBalance myBalance, sim.capitalGainPercentage myPerc, LastClose dowJones, dow.capitalGainPercentage dowPerc
from vNoahCaseStudy2_simulationDailyPerformance sim
JOIN vNoahCaseStudy2_DowDailyPerformance dow
ON sim.yyyymmd_Offset = dow.yyyymmdd
--ORDER BY sim.yyyymmd_Offset