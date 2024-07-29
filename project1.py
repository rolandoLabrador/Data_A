import ccxt
import pandas as pd
import matplotlib.pyplot as plt

try:
    # Initialize exchange (switching from Binance to Kraken)
    exchange = ccxt.kraken()
    symbol = 'BTC/USD'
    since = exchange.parse8601('2023-01-01T00:00:00Z')

    # Fetch historical data
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1d', since=since)
    data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

    # Convert timestamp to datetime
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    print(data.head())

    # Handle missing values
    data.fillna(method='ffill', inplace=True)

    # Normalize data (example: min-max scaling)
    data['normalized_volume'] = (data['volume'] - data['volume'].min()) / (data['volume'].max() - data['volume'].min())
    print(data.head())

    # Plotting closing prices
    plt.figure(figsize=(12, 6))
    plt.plot(data['timestamp'], data['close'], label='Closing Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('BTC/USD Closing Prices')
    plt.legend()
    plt.show()

    # Calculate and plot moving average
    data['ma50'] = data['close'].rolling(window=50).mean()
    plt.figure(figsize=(12, 6))
    plt.plot(data['timestamp'], data['close'], label='Closing Price')
    plt.plot(data['timestamp'], data['ma50'], label='50-day MA', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('BTC/USD Closing Prices with 50-day MA')
    plt.legend()
    plt.show()

except ccxt.base.errors.ExchangeNotAvailable as e:
    print(f"Error: {e}")
