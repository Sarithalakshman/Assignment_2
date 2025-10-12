# Assignment_2
Data-Driven Stock Analysis: Organizing, Cleaning, and Visualizing Market Trends

1. Project Overview & Goal:-

(i)Goal: To analyze stock performance over the past year and provide actionable investment insights.
(ii)Key Metrics Calculated: Volatility (Risk), Yearly Return (Performance), and Stock Correlation.
(iii)Output: Interactive dashboards in Power BI and Streamlit.

2. Problem Statement:-
 
 The main problem this project solves is streamlining stock analysis from raw data to a comprehensive, interactive dashboard to inform investment decisions.
This is achieved by solving three sub-problems:
(i)Inefficient Analysis (Python): Automating the complex process of fetching daily data and calculating key financial metrics    (Sharpe ratio, volatility, correlation, etc.).
(ii)Disjointed Data Storage (MySQL): Providing a single, structured database (dd_stockanalysis) to store all clean, 
   calculated metrics for centralized access.
(iii)Static Reporting (Power BI): Transforming the complex SQL data tables into a user-friendly, dynamic visual dashboard for    quick interpretation, filtering, and trend identification.

3. Project Workflow:-
   
(i)Python: Reads raw data, cleans it, and calculates all financial metrics (Volatility, Return, Correlation).
(ii)MySQL: Serves as the central database, storing all the calculated analytical tables.
(iii)Power BI: Connects to MySQL for creating complex charts (Line Chart, Heatmap) and data modeling.
(iv)Streamlit: Connects to MySQL to build the final, fast web application dashboard (e.g.,Top/Bottom 10 Rankings)

