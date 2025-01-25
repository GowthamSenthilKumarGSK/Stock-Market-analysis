# Stock-Market-analysis
Developed a Python Flask-based stock analysis tool that fetches real-time stock prices using BeautifulSoup for web scraping. Enabled analysis of key financial metrics and created interactive visualizations to provide actionable insights into stock performance, enhancing user decision-making.

## Features

### Real-Time Stock Prices
- Fetch live stock prices for a predefined list of companies using web scraping with BeautifulSoup.
- Save the fetched data into a JSON file for future use.

### Stock Analysis
Analyze stock data for a selected company over a user-specified date range. The application includes in-depth analysis using the following financial indicators and metrics:
- **Moving Averages (50-day, 200-day)**
- **Bollinger Bands**
- **MACD (Moving Average Convergence Divergence)**
- **RSI (Relative Strength Index)**
- **Stochastic Oscillator**
- **Market Cap**
- **Volatility**
- **Alligator Indicator**
- **Scatter Matrix**

### Visualization
- Generate interactive and insightful plots for each metric using Matplotlib.
- Plots are embedded in the web application as base64-encoded images, making them directly viewable in the browser.

### Web Application
- User-friendly web interface built with Flask and HTML templates.
- Easy navigation for fetching stock data and visualizing analysis.
  
### Predefined Stock List
The application comes with a predefined list of stocks from global markets, including:
- **NASDAQ**: Apple (AAPL), Microsoft (MSFT), Amazon (AMZN)
- **NSE**: Infosys (INFY.NS), TCS (TCS.NS), Wipro (WIPRO.NS), HCL Technologies (HCLTECH.NS), ITC (ITC.NS), ICICI Bank (ICICIBANK.NS), Reliance (RELIANCE.NS)

