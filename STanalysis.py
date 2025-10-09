import pandas as pd
import numpy as np
import time
from db import  save_to_db #Imports the saving function


FILE_PATH = "Stocks.csv"
ANALYSIS_COLUMNS = ['ibm', 'aapl', 'msft', 'xrx', 'amzn', 'dell', 'googl', 'adbe']



#LOAD AND CLEAN DATA 

try:
    # Reads the header
    df_stocks = pd.read_csv(FILE_PATH, header=1)
    df_stocks.columns = [col.lower() for col in df_stocks.columns]
    df_stocks['date'] = pd.to_datetime(df_stocks['date'])
    # df_daily is the clean, time-indexed DataFrame for returns/volatility calculations
    df_daily = df_stocks.dropna(subset=['date']).set_index('date').copy()
    print(f"✅ Data loaded. Ready for analysis.")
except FileNotFoundError:
    print(f"❌ Error: {FILE_PATH} not found. Exiting script.")
    exit()

#Prepare df_daily for Calculations
df_daily = df_daily[ANALYSIS_COLUMNS]



#CALCULATE CORE METRICS (Volatility and Yearly Return)

stock_metrics_list = []

for stock in ANALYSIS_COLUMNS:
    if stock not in df_daily.columns:
        continue

    daily_return = df_daily[stock].pct_change()
    
    # Calculate Volatility
    volatility = daily_return.std()
    
    # Calculate Yearly Return (Cumulative Return)
    cumulative_series = (1 + daily_return).cumprod() - 1
    yearly_return = cumulative_series.dropna().iloc[-1] if not cumulative_series.dropna().empty else np.nan

    stock_metrics_list.append({
        'ticker': stock.upper(),
        'volatility': volatility,
        'yearly_return': yearly_return,
        'sector': 'Unknown', # Temporary placeholder for sector mapping
    })

df_metrics_raw = pd.DataFrame(stock_metrics_list).dropna(subset=['yearly_return', 'volatility'])


#SECTOR MAPPING AND AGGREGATION
# Sector mapping data
sector_map = {
    'AAPL': 'IT', 'MSFT': 'IT', 'GOOGL': 'Communication Services', 
    'IBM': 'IT', 'XRX': 'IT', 'AMZN': 'Consumer Discretionary', 
    'DELL': 'IT', 'ADBE': 'IT'
}

#Prepare df_metrics (Update sector column)
df_metrics_raw['sector'] = df_metrics_raw['ticker'].map(sector_map)
df_metrics = df_metrics_raw[['ticker', 'volatility', 'yearly_return', 'sector']]

#Prepare df_sector (Aggregation)
df_sector_summary = df_metrics.groupby('sector').agg(
    avg_return=('yearly_return', 'mean'),
    num_stocks=('ticker', 'count')
).reset_index()

#CORRELATION MATRIX

print("\nCalculating Correlation Matrix")

# Calculate daily returns for correlation
df_returns = df_daily.pct_change().dropna()

# Calculate the correlation matrix
correlation_matrix = df_returns.corr()

# Convert matrix to a long format suitable for SQL table and Heatmap visual
df_correlation_long = correlation_matrix.stack().reset_index()
df_correlation_long.columns = ['stock_a', 'stock_b', 'correlation']

# Remove self-correlation (correlation == 1) for cleaner data
df_correlation = df_correlation_long[df_correlation_long['stock_a'] != df_correlation_long['stock_b']].copy()
print(f"DEBUG: df_correlation size: {len(df_correlation)} rows") #DEBUG CHECK




#MONTHLY & RAW DATA PREP (New Logic to fill stocks_raw & monthly_performance)
print("Preparing Monthly and Raw Data Tables")

#Prepare df_stocks_raw
#df_stocks is the original DataFrame with the 'date' column
df_stocks_raw = df_stocks[['date'] + ANALYSIS_COLUMNS].copy()
# Melt the DataFrame to long format (date, ticker, price)
df_stocks_raw = df_stocks_raw.melt(
    id_vars=['date'], 
    value_vars=ANALYSIS_COLUMNS, 
    var_name='ticker', 
    value_name='close' #assume the values are close prices
).dropna()

# Convert ticker to uppercase for consistency
df_stocks_raw['ticker'] = df_stocks_raw['ticker'].str.upper()
print(f"DEBUG: df_stocks_raw size: {len(df_stocks_raw)} rows") #DEBUG CHECK


# 2. Prepare df_monthly_performance (Uses the prepared daily returns)
# Resample daily returns to monthly returns
df_monthly_returns = (1 + df_returns).resample('M').prod() - 1
df_monthly_returns.index.name = 'date'

# Melt to long format
df_monthly_performance = df_monthly_returns.reset_index().melt(
    id_vars='date',
    var_name='ticker',
    value_name='monthly_return'
).dropna()

# Add month column and category/rank placeholders
df_monthly_performance['month'] = df_monthly_performance['date'].dt.strftime('%Y-%m')
df_monthly_performance['ticker'] = df_monthly_performance['ticker'].str.upper()
# Adding placeholder columns required by your previous structure
df_monthly_performance['category'] = 'Stock'
df_monthly_performance['monthly_rank'] = df_monthly_performance.groupby('month')['monthly_return'].rank(method='min', ascending=False).astype(int)

# Select final columns for SQL table
df_monthly_performance = df_monthly_performance[['month', 'ticker', 'monthly_return', 'category', 'monthly_rank']]


#DATABASE SAVING 

print("\n--- Saving All Data to MySQL Database ---")

# Save the detailed stock metrics 
save_to_db(df_metrics, 'stocks_metrics', if_exists='replace')

# Save the sector summary 
save_to_db(df_sector_summary, 'sector_summary', if_exists='replace')

# Save the CORRELATION MATRIX
save_to_db(df_correlation, 'correlation_matrix', if_exists='replace')

# Save the MONTHLY PERFORMANCE
save_to_db(df_monthly_performance, 'monthly_performance', if_exists='replace')

# Save the RAW STOCK DATA 
save_to_db(df_stocks_raw, 'stocks_raw', if_exists='replace')


