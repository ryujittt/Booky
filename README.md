# Booky
A simple desktop application built with PyQt5 that analyzes real-time order book data from Binance. The app fetches data from the Binance public API and provides various tools for analyzing liquidity, volatility, mid-price statistics, and average bid/ask differences for selected trading pairs.

# 🔧 Features
Currency Pair Selection: Choose between ETHUSDT, BTCUSDT (or add more).

Customizable Depth Analysis: Select how many order book levels (rows) to include in the analysis.

Live Mode: Enable automatic updates every 3 seconds.

Analysis Tools:

Liquidity: Compares total bid and ask volume.

Volatility: Computes mid-price volatility using log returns.

Time Series: Shows mean, median, and range of mid-prices.

Bid/Ask Stats: Calculates quantity difference, average prices, and min/max levels.

# Install dependencies:


pip install PyQt5 requests pandas numpy


# 🖼️ UI Overview
Combo Boxes: Select trading pair and order book depth.

Radio Button: Toggle live update mode (fetches data every 2 seconds).

Buttons:

Calculate: Show average prices and quantity differences.

Liquidity: Analyze market depth balance.

Volatility: Measure mid-price volatility.

Timeseries: Basic statistics over selected depth.

Fill ComboBox: Auto-populate number-of-rows based on order book size.

# 🚀 Future Enhancements
Support for more exchanges (e.g., Coinbase, Kraken).

Candlestick plotting.

Graphical visualization of order book.

Saving time series data to CSV.


# Disclaimer:
This app is intended for research purposes only. The developers do not take any responsibility for any financial losses or damages resulting from the use of this app. Users are advised to make their own independent decisions and conduct thorough research before taking any actions based on the information provided by this app.

Booky Project. All rights reserved.

Open-source code, developed by [CHAKRAR ABDELMALIK].
