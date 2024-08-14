# Alpha Vantage API Integration

This folder contains Python modules for interacting with the Alpha Vantage API to retrieve various types of financial data. The modules are organized as follows:

1. **API.py**: The base module that provides the core functionality for making API requests. It initializes the API key and constructs API request URLs.

2. **EconomicIndicators.py**: This module focuses on fetching economic indicator data using the Alpha Vantage API. It includes methods for retrieving U.S. Treasury yield data, U.S. Federal Funds Rate data, and various monthly economic indicators.

3. **FundamentalData.py**: This module deals with retrieving fundamental financial data for stocks. It includes methods for building DataFrames for balance sheets, income statements, cash flow statements, and earnings reports. These methods enable you to construct a DataFrame containing quarterly fundamental data for a stock.

4. **HistoricData.py**: This module is designed for fetching historic stock market data. It includes methods to obtain intraday stock data for a specified time interval and number of years. The data can be retrieved in various output sizes and formats (e.g., CSV or JSON).

## Setup

Before using these modules, make sure you obtain an API key from Alpha Vantage by signing up at [Alpha Vantage](https://www.alphavantage.co/support/). Once you have the API key, configure it in the respective modules.

## Usage

Each module provides specific methods for fetching different types of financial data. Refer to the docstrings within the modules for detailed information on how to use each method.

```python
# Example usage of EconomicIndicators module
from alpha_vantage import EconomicIndicators

# Initialize EconomicIndicators with your API key
economic_api = EconomicIndicators(api_key='your_api_key')

# Fetch Treasury yield data
treasury_yield_data = economic_api.treasury_yield()

# Fetch Federal Funds Rate data
federal_funds_data = economic_api.federal_funds()

# Fetch monthly economic indicators
monthly_indicators_data = economic_api.monthly_indicators()