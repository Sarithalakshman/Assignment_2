# Assignment_2
Data-Driven Stock Analysis: Organizing, Cleaning, and Visualizing Market Trends

Project Overview & Goal:-

Goal: To analyze stock performance over the past year and provide actionable investment insights.
Key Metrics Calculated: Volatility (Risk), Yearly Return (Performance), and Stock Correlation.
Output: Interactive dashboards in Power BI and Streamlit.

Problem Statement:-

This project addresses the challenge of streamlining stock analysis from raw data to a comprehensive, interactive dashboard for informed investment decisions.
It tackles three key sub-problems:

*Inefficient Analysis (Python): Automates the complex process of fetching daily stock data and calculating key financial metrics such as Sharpe Ratio, Volatility, and Correlation.

*Disjointed Data Storage (MySQL): Establishes a unified, structured database (dd_stockanalysis) to store all cleaned and calculated metrics for centralized access.

*Static Reporting (Power BI): Transforms complex SQL tables into dynamic, user-friendly dashboards for quick interpretation, filtering, and trend identification.

Project Workflow:-

Python: Reads raw data, performs cleaning, and computes financial metrics (Volatility, Return, Correlation).

MySQL: Acts as the central database, storing all processed analytical tables.

Power BI: Connects to MySQL to build insightful visualizations such as line charts and heatmaps.

Streamlit: Connects to MySQL to deliver the final interactive web application, showcasing features like Top/Bottom 10 stock rankings.
