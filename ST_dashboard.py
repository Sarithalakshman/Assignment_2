import streamlit as st
import pandas as pd
from db import read_from_db 
import plotly.express as px

#PAGE CONFIGURATION 
st.set_page_config(layout="wide", page_title="Data-Driven Stock Analysis")

#DATA FETCHING (Using the utility function)
@st.cache_data
def get_dashboard_data():
    """Fetches all necessary data from the database."""
    
    # Fetch Master Metrics (Volatility, Yearly Returns, Sector)
    metrics_query = "SELECT ticker, volatility, yearly_return, sector FROM stocks_metrics"
    df_metrics = read_from_db(metrics_query)
    
    # Fetch Sector Summary (Average return per sector)
    sector_query = "SELECT sector, avg_return, num_stocks FROM sector_summary"
    df_sector = read_from_db(sector_query)
    
    # Check if data was successfully fetched
    if df_metrics is None or df_sector is None:
        st.error("Could not connect to or retrieve data from the database. Please check db.py configuration.")
        return None, None
        
    return df_metrics, df_sector

# Fetch data for the entire app
df_metrics, df_sector = get_dashboard_data()

# Only run the dashboard code if data is available
if df_metrics is not None:
    
    st.title("Nifty 50 Performance Dashboard")
    
    #VISUALIZATION 1: Top 10 Most Volatile Stocks
    st.header("Top 10 Most Volatile Stocks 📉")
    df_volatile = df_metrics.sort_values(by='volatility', ascending=False).head(10)
    
    fig_volatility = px.bar(
        df_volatile,
        x='ticker',
        y='volatility',
        title='Stocks by Historical Volatility (Standard Deviation of Daily Returns)',
        color='volatility',
        color_continuous_scale=px.colors.sequential.Reds
    )
    st.plotly_chart(fig_volatility, use_container_width=True)

    #VISUALIZATION 2:Average Sector Returns
    st.header("Average Yearly Return by Sector 🏭")
    
    # Ensure sectors are sorted correctly for the visualization
    df_sector = df_sector.sort_values(by='avg_return', ascending=False)
    
    fig_sector = px.bar(
        df_sector,
        x='sector',
        y='avg_return',
        title='Average Sector Performance',
        color='avg_return',
        color_continuous_scale=['red', 'yellow', 'green']
    )
    st.plotly_chart(fig_sector, use_container_width=True)

    #VISUALIZATION 3:Top and Bottom 10 Performers 
   
    st.header("Top 10 Best & Worst Performing Stocks 🟢/🔴")
    
    #Data Preparation for Rankings
    # Sort for Top 10 (Best Performers)
    df_top_10 = df_metrics.sort_values(
        by='yearly_return', 
        ascending=False
    ).head(10).reset_index(drop=True)
    
    # Sort for Bottom 10 (Worst Performers)
    df_bottom_10 = df_metrics.sort_values(
        by='yearly_return', 
        ascending=True
    ).head(10).reset_index(drop=True)
    
    #Layout into two columns 
    col1, col2 = st.columns(2)
    
    # Display Top 10
    with col1:
        st.subheader("Top 10 Best Performers")
        display_top = df_top_10[['ticker', 'yearly_return', 'sector']].copy()
        display_top['yearly_return'] = (display_top['yearly_return'] * 100).round(2).astype(str) + '%'
        st.dataframe(display_top, use_container_width=True, hide_index=True)
        
    # Display Bottom 10
    with col2:
        st.subheader("Top 10 Worst Performers")
        display_bottom = df_bottom_10[['ticker', 'yearly_return', 'sector']].copy()
        display_bottom['yearly_return'] = (display_bottom['yearly_return'] * 100).round(2).astype(str) + '%'
        st.dataframe(display_bottom, use_container_width=True, hide_index=True)
        
    