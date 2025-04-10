import sys
import requests
import pandas as pd
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QVBoxLayout, QWidget, QRadioButton,QHBoxLayout
import numpy as np
class Booky(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Booky")
        self.setGeometry(100, 100, 400, 250)

        self.is_live_mode = False  # Flag to indicate live mode
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.setInterval(2000)  # Update every 2 seconds

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        ansys_button_layout = QHBoxLayout()
        # Currency pair symbol ComboBox
        self.symbol_label = QLabel("Currency Pair:")
        self.symbol_combo = QComboBox()
        self.symbol_combo.addItem("ETHUSDT")
        self.symbol_combo.addItem("BTCUSDT")
        # Add more currency pairs as needed
        self.symbol_combo.setCurrentText("BTCUSDT")  # Set default value

        # Number of rows ComboBox
        self.num_rows_label = QLabel("Sum table rows:")
        self.num_rows_combo = QComboBox()
        self.num_rows_combo.addItem("3")
        self.num_rows_combo.addItem("5")
        self.num_rows_combo.addItem("10")
        # Add more row options as needed
        self.num_rows_combo.setCurrentText("3")  # Set default value

        # Radio button for live mode
        self.live_mode_radio = QRadioButton("Live Mode (Update every 3 seconds)")
        self.live_mode_radio.toggled.connect(self.toggle_live_mode)

        self.result_label = QLabel("Quantity Difference and Average Prices:")

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_difference_and_average_prices)
        
        self.liquidity_button = QPushButton("Liquidity")
        self.liquidity_button.clicked.connect(self.show_liquidity_analysis)
        
        self.volatility_button = QPushButton("Volatility")
        self.volatility_button.clicked.connect(self.show_volatility_analysis)
        
        self.timeseries_button = QPushButton("Timeseries")
        self.timeseries_button.clicked.connect(self.show_timeseries_analysis)
        
        
            # New button for filling the ComboBox
        self.fill_combo_button = QPushButton("Fill ComboBox")
        self.fill_combo_button.clicked.connect(self.fill_combo_box)
    

        layout.addWidget(self.symbol_label)
        layout.addWidget(self.symbol_combo)
        layout.addWidget(self.num_rows_label)
        layout.addWidget(self.num_rows_combo)
        layout.addWidget(self.live_mode_radio)
        layout.addWidget(self.result_label)
        # Add both buttons to the button layout
        button_layout.addWidget(self.calculate_button)
        button_layout.addWidget(self.fill_combo_button)
        
        ansys_button_layout.addWidget(self.liquidity_button)
        ansys_button_layout.addWidget(self.volatility_button) 
        ansys_button_layout.addWidget(self.timeseries_button)

        layout.addLayout(ansys_button_layout)
        layout.addLayout(button_layout) 
        self.state = 'average'

        self.central_widget.setLayout(layout)
    def show_liquidity_analysis(self):
        self.state = 'liquidity'

        symbol = self.symbol_combo.currentText()

        
        try:
            url = 'https://api.binance.com/api/v3/depth'
            params = {
                'symbol': symbol,
            }

            response = requests.get(url, params=params)
            data = response.json()

            # Extract bids and asks data
            bids = data['bids']
            asks = data['asks']

            # Calculate the sum of quantities for top N bids and asks
            sum_bids_quantity = sum(float(bid[1]) for bid in bids[:])
            sum_asks_quantity = sum(float(ask[1]) for ask in asks[:])

            # Calculate the liquidity ratio
            liquidity_ratio = sum_bids_quantity / sum_asks_quantity

            result_text = f"Liquidity Ratio: {liquidity_ratio}"

            self.result_label.setText(result_text)
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")
        
        
        pass
    
    def show_volatility_analysis(self):
        self.state = 'voltality'

        
        symbol = self.symbol_combo.currentText()
        num_rows = int(float(self.num_rows_combo.currentText()))

        try:
            url = 'https://api.binance.com/api/v3/depth'
            params = {
                'symbol': symbol,
            }

            response = requests.get(url, params=params)
            data = response.json()

            # Extract bids and asks data
            bids = data['bids']
            asks = data['asks']

            # Calculate the mid-price for each level
            mid_prices = [(float(bid[0]) + float(ask[0])) / 2 for bid, ask in zip(bids, asks)]

            # Calculate returns as the logarithmic difference in mid-prices
            returns = np.diff(np.log(mid_prices))

            # Calculate volatility as the standard deviation of returns
            volatility = np.std(returns)

            result_text = f"Volatility (Standard Deviation): {volatility}"

            self.result_label.setText(result_text)
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")
    
    def show_timeseries_analysis(self):
        self.state = 'timeseries'

                
        symbol = self.symbol_combo.currentText()
        num_rows = int(float(self.num_rows_combo.currentText()))

        try:
            url = 'https://api.binance.com/api/v3/depth'
            params = {
                'symbol': symbol,
            }

            response = requests.get(url, params=params)
            data = response.json()

            # Extract bids and asks data
            bids = data['bids']
            asks = data['asks']

            # Calculate the mid-price for each level
            mid_prices = [(float(bid[0]) + float(ask[0])) / 2 for bid, ask in zip(bids, asks)]

            # Extract the historical prices based on the number of rows selected
            historical_prices = mid_prices[:num_rows]

            # Calculate various statistics
            price_mean = np.mean(historical_prices)
            price_median = np.median(historical_prices)
            price_range = np.ptp(historical_prices)  # Peak-to-peak range

            result_text = f"Time Series Analysis:\n"
            result_text += f"Mean Price: {price_mean}\n"
            result_text += f"Median Price: {price_median}\n"
            result_text += f"Price Range: {price_range}"

            self.result_label.setText(result_text)
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")
        
    
    def toggle_live_mode(self):
        self.is_live_mode = self.live_mode_radio.isChecked()
        if self.is_live_mode:
            self.timer.start()
        else:
            self.timer.stop()

    def update_data(self):
        if self.is_live_mode:
            if self.state == 'voltality':
                self.show_volatility_analysis()
        
            elif self.state  == 'liquidity':
                self.show_liquidity_analysis()
            
            elif self.state == 'timeseries':
                self.show_timeseries_analysis()
            
            elif self.state == 'average':
                self.calculate_difference_and_average_prices()

    def calculate_difference_and_average_prices(self):
        self.state = 'average'
        symbol = self.symbol_combo.currentText()
        num_rows = int(float(self.num_rows_combo.currentText()))

        try:
            url = 'https://api.binance.com/api/v3/depth'
            params = {
                'symbol': symbol,
            }

            response = requests.get(url, params=params)
            data = response.json()

            # Extract bids and asks data
            bids = data['bids']
            asks = data['asks']

            # Convert the data into a pandas DataFrame for easier manipulation
            bids_df = pd.DataFrame(bids, columns=['Price', 'Quantity'])
            asks_df = pd.DataFrame(asks, columns=['Price', 'Quantity'])

            # Sort the DataFrames by price in ascending order for bids and descending order for asks
            bids_df['Price'] = bids_df['Price'].astype(float)
            asks_df['Price'] = asks_df['Price'].astype(float)
            bids_df = bids_df.sort_values(by='Price', ascending=False)
            asks_df = asks_df.sort_values(by='Price', ascending=True)

            # Get the top N bids and asks using iloc
            top_n_bids = bids_df.iloc[:num_rows]
            top_n_asks = asks_df.iloc[:num_rows]
            
            

            # Calculate the sum of quantities for top N bids and asks
            sum_bids_quantity = top_n_bids['Quantity'].astype(float).sum()
            sum_asks_quantity = top_n_asks['Quantity'].astype(float).sum()

            # Calculate the quantity difference
            quantity_difference = sum_asks_quantity - sum_bids_quantity

            # Calculate the average ask and bid prices
            avg_ask_price = top_n_asks['Price'].astype(float).mean()
            avg_bid_price = top_n_bids['Price'].astype(float).mean()

            result_text = f"Quantity Difference: {quantity_difference:.2f}\n"
            result_text += f"Average Ask Price: {avg_ask_price:.3f}\n"
            result_text += f"Average Bid Price: {avg_bid_price:.3f}"
            
            demande_difference = bids_df['Quantity'].astype(float).sum() - asks_df['Quantity'].astype(float).sum()
            max_asks_price =asks_df['Price'].astype(float).max()
            min_bids_price = bids_df['Price'].astype(float).min()
            
            result_text += "\n"
            result_text += f"\nTotal Quantiy Difference: {demande_difference:.3f}"
            result_text += f"\nMin Price: {min_bids_price:.3f}"
            result_text += f"\nMax Price: {max_asks_price:.3f}"
            self.result_label.setText(result_text)
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")

            
    def fill_combo_box(self):
        
        
        symbol = self.symbol_combo.currentText()
        num_rows = float(self.num_rows_combo.currentText())

        try:
            url = 'https://api.binance.com/api/v3/depth'
            params = {
                'symbol': symbol,
            }

            response = requests.get(url, params=params)
            data = response.json()

            # Extract bids and asks data
            bids = data['bids']
            asks = data['asks']

            # Process bids and asks data directly
            min_value = min(float(bid[0]) for bid in bids)
            max_value = max(float(ask[0]) for ask in asks)
            num_values = int((len(bids) + len(asks)))
            numpy_array = np.linspace(2, num_values, num=int(num_values/2))
            self.num_rows_combo.clear()
            for value in numpy_array:
                self.num_rows_combo.addItem(str(int(value)))
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")
            
            
def main():
    app = QApplication(sys.argv)
    window = Booky()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
