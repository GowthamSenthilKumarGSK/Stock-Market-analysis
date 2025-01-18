from flask import Flask, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import yfinance as yf
from io import BytesIO
import base64

app = Flask(__name__)

# Function to fetch stock data
def fetch_data(company, start, end):
    return yf.download(company, start=start, end=end)

# Function to encode plots as base64
def get_img_data():
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_img = base64.b64encode(img.getvalue()).decode()
    plt.close()  # Close the plot to avoid memory leaks
    return plot_img

# Plot functions
def plot_volume(traded_data):
    plt.figure(figsize=(10, 5))
    traded_data['Volume'].plot()
    plt.title('Volume of Stock Traded')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.grid(True)
    plt.tight_layout()
    return get_img_data()

def plot_market_cap(data):
    data['MarketCap'] = data['Open'] * data['Volume']
    plt.figure(figsize=(10, 5))
    data['MarketCap'].plot()
    plt.title('Market Cap')
    plt.xlabel('Date')
    plt.ylabel('Market Cap')
    plt.grid(True)
    plt.tight_layout()
    return get_img_data()

def plot_moving_average(data):
    data['MA50'] = data['Open'].rolling(50).mean()
    data['MA200'] = data['Open'].rolling(200).mean()
    plt.figure(figsize=(10, 5))
    data['Open'].plot(label='Open Price')
    data['MA50'].plot(label='MA50')
    data['MA200'].plot(label='MA200')
    plt.title('Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return get_img_data()

def plot_scatter_matrix(data):
    scatter_matrix(data[['Open', 'High', 'Low', 'Close']], alpha=0.2, figsize=(10, 10), diagonal='kde')
    plt.suptitle('Scatter Matrix')
    plt.tight_layout()
    return get_img_data()

def plot_volatility(data):
    data['returns'] = (data['Close'] / data['Close'].shift(1)) - 1
    plt.figure(figsize=(10, 5))
    data['returns'].hist(bins=100, alpha=0.5)
    plt.title('Volatility')
    plt.xlabel('Returns')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    return get_img_data()

def plot_bollinger_bands(data):
    data['MA20'] = data['Close'].rolling(20).mean()
    data['STD'] = data['Close'].rolling(20).std()
    data['Upper Band'] = data['MA20'] + (2 * data['STD'])
    data['Lower Band'] = data['MA20'] - (2 * data['STD'])

    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label='Close Price', color='blue')
    plt.plot(data['MA20'], label='20-Day MA', color='orange')
    plt.plot(data['Upper Band'], label='Upper Band', color='green')
    plt.plot(data['Lower Band'], label='Lower Band', color='red')
    plt.fill_between(data.index, data['Upper Band'], data['Lower Band'], color='gray', alpha=0.2)
    plt.title('Bollinger Bands')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return get_img_data()

def plot_macd(data):
    data['EMA12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['EMA26'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = data['EMA12'] - data['EMA26']
    data['Signal Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

    plt.figure(figsize=(10, 5))
    plt.plot(data['MACD'], label='MACD', color='blue')
    plt.plot(data['Signal Line'], label='Signal Line', color='red')
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    plt.title('MACD (Moving Average Convergence Divergence)')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return get_img_data()

def plot_stochastic_oscillator(data):
    high14 = data['High'].rolling(window=14).max()
    low14 = data['Low'].rolling(window=14).min()
    data['%K'] = (data['Close'] - low14) / (high14 - low14) * 100
    data['%D'] = data['%K'].rolling(window=3).mean()

    plt.figure(figsize=(10, 5))
    plt.plot(data['%K'], label='%K (Stochastic Oscillator)', color='blue')
    plt.plot(data['%D'], label='%D (Signal Line)', color='red')
    plt.axhline(80, color='green', linestyle='--', linewidth=1, label='Overbought')
    plt.axhline(20, color='orange', linestyle='--', linewidth=1, label='Oversold')
    plt.title('Stochastic Oscillator')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return get_img_data()

def plot_rsi(data):
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, rsi, label='RSI', color='orange')
    plt.axhline(70, linestyle='--', color='red', label='Overbought')
    plt.axhline(30, linestyle='--', color='green', label='Oversold')
    plt.title('Relative Strength Index (RSI)')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return get_img_data()

def plot_alligator(data):
    data['Jaw'] = data['Close'].rolling(window=13).mean().shift(8)
    data['Teeth'] = data['Close'].rolling(window=8).mean().shift(5)
    data['Lips'] = data['Close'].rolling(window=5).mean().shift(3)

    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label='Close Price', color='black')
    plt.plot(data['Jaw'], label='Jaw (13 SMA, Shift 8)', color='blue')
    plt.plot(data['Teeth'], label='Teeth (8 SMA, Shift 5)', color='red')
    plt.plot(data['Lips'], label='Lips (5 SMA, Shift 3)', color='green')
    plt.title('Alligator Indicator')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return get_img_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/companylist')
def companylist():
    return render_template('companylist.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    company = request.form['company']

    data = fetch_data(company, start_date, end_date)

    if not data.empty:
        data = data.dropna()  # Handle missing values
        volume_plot = plot_volume(data)
        market_cap_plot = plot_market_cap(data)
        moving_average_plot = plot_moving_average(data)
        scatter_matrix_plot = plot_scatter_matrix(data)
        volatility_plot = plot_volatility(data)
        bollinger_bands_plot = plot_bollinger_bands(data)
        macd_plot = plot_macd(data)
        stochastic_oscillator_plot = plot_stochastic_oscillator(data)
        rsi_plot = plot_rsi(data)
        alligator_plot = plot_alligator(data)

        return render_template(
            'analyze.html',
            volume_plot=volume_plot,
            market_cap_plot=market_cap_plot,
            moving_average_plot=moving_average_plot,
            scatter_matrix_plot=scatter_matrix_plot,
            volatility_plot=volatility_plot,
            bollinger_bands_plot=bollinger_bands_plot,
            macd_plot=macd_plot,
            stochastic_oscillator_plot=stochastic_oscillator_plot,
            rsi_plot=rsi_plot,
            alligator_plot=alligator_plot
        )
    else:
        return "Error fetching data. Please check the inputs and try again."

if __name__ == "__main__":
    app.run(debug=True)
