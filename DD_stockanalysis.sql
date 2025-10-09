create database dd_stockanalysis;
use  dd_stockanalysis;
# 1️ Daily stock OHLCV data
CREATE TABLE stocks_raw (
    date DATE NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    open DECIMAL(10,2),
    high DECIMAL(10,2),
    low DECIMAL(10,2),
    close DECIMAL(10,2),
    volume BIGINT,
    PRIMARY KEY (date, ticker)
);
#2️ Yearly metrics (volatility, return, Sharpe, sector)
CREATE TABLE stocks_metrics (
    ticker VARCHAR(10) PRIMARY KEY,
    volatility DECIMAL(10,4),
    yearly_return DECIMAL(10,4),
    sharpe_ratio DECIMAL(10,4),
    sector VARCHAR(50)
);

#3️ Monthly performance
CREATE TABLE monthly_performance (
    month VARCHAR(20),
    ticker VARCHAR(10),
    monthly_return DECIMAL(10,4),
    category VARCHAR(10),  -- 'Gainer' or 'Loser'
    monthly_rank INT
);

#4 Sector summary
CREATE TABLE sector_summary (
    sector VARCHAR(50) PRIMARY KEY,
    avg_return DECIMAL(10,4),
    num_stocks INT
);

#5️ Correlation matrix
CREATE TABLE if not exists correlation_matrix (
    stock_a VARCHAR(10) NOT NULL,
    stock_b VARCHAR(10) NOT NULL,
    correlation DECIMAL(10,4),
    PRIMARY KEY (stock_a, stock_b)
);
#Gainers
SELECT ticker, yearly_return
FROM stocks_metrics
ORDER BY yearly_return DESC
LIMIT 10;

# Losers
SELECT ticker, yearly_return
FROM stocks_metrics
ORDER BY yearly_return ASC
LIMIT 10;
SELECT 
    SUM(CASE WHEN yearly_return > 0 THEN 1 ELSE 0 END) AS green_stocks,
    SUM(CASE WHEN yearly_return < 0 THEN 1 ELSE 0 END) AS red_stocks
FROM stocks_metrics;
SELECT sector, AVG(yearly_return) AS avg_sector_return
FROM stocks_metrics
GROUP BY sector
ORDER BY avg_sector_return DESC;
-- Top 5 Gainers for a given month
SELECT month, ticker, monthly_return
FROM monthly_performance
WHERE category = 'Gainer' AND month = '2023-07'
ORDER BY monthly_return DESC
LIMIT 5;

-- Top 5 Losers for a given month
SELECT month, ticker, monthly_return
FROM monthly_performance
WHERE category = 'Loser' AND month = '2023-07'
ORDER BY monthly_return ASC
LIMIT 5;
-- Highly correlated pairs
SELECT *
FROM correlation_matrix
WHERE correlation > 0.8
ORDER BY correlation DESC;

-- Strongly inverse correlations
SELECT *
FROM correlation_matrix
WHERE correlation < -0.5
ORDER BY correlation ASC;
SELECT * FROM correlation_matrix;


