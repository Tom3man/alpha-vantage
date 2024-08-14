import logging

import pandas as pd
import requests

from alpha_vantage.common.api import AlphaVantageAPI, APIRequestError
from alpha_vantage.tables import StockData

log = logging.getLogger(__name__)


class StockPriceFetcher(AlphaVantageAPI):
    """
    A class to fetch and process historical stock market data using the AlphaVantage API.

    Inherits from:
        AlphaVantageAPI: A base class for interacting with the AlphaVantage API.

    Methods:
        get_historic_data(ticker: str) -> pd.DataFrame:
            Fetches and processes historical stock data for a given ticker.
    """

    def get_stock_data(self, ticker: str) -> pd.DataFrame:
        """
        Fetch and process historic stock market data for the specified ticker symbol.

        Args:
            ticker (str): The stock symbol/ticker.

        Returns:
            pd.DataFrame: DataFrame containing the historic stock market data with columns
            ['TIMESTAMP', 'TICKER', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME'].

        Raises:
            APIRequestError: If there is an error with the API request.
            Exception: For any other exceptions that occur during data processing.
        """

        # Prepare parameters for API request
        kwargs = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': ticker,
            'outputsize': 'full',
        }
        url = self.build_url_request(**kwargs)
        log.info(f"Requesting DAILY data for ticker {ticker} from AlphaVantage.")

        try:
            # Make API request
            data = self.make_request(url=url)

        except requests.exceptions.RequestException as e:
            log.error(f"API request error for ticker {ticker}: {str(e)}")
            raise APIRequestError(f"API request error for ticker {ticker}: {str(e)}")

        if not data:
            log.error(f"No data returned for ticker {ticker}.")
            raise APIRequestError(f"No data returned for ticker {ticker}.")

        try:
            # Extract time series data
            time_series_data = list(data.values())[1]
        except Exception as e:
            log.error(f"Error extracting data for ticker {ticker}: {str(e)}")
            raise Exception(f"Failed to extract data for ticker {ticker}: {str(e)}")

        try:
            # Convert time series data to DataFrame
            df = pd.DataFrame(time_series_data).T

            # Rename columns for clarity
            df.columns = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]

            # Convert data types to numeric
            df = df.apply(pd.to_numeric, errors='coerce')

            # Reset index and rename it to 'timestamp'
            df.reset_index(inplace=True)
            df.rename(columns={'index': 'timestamp'}, inplace=True)

            # Convert 'timestamp' column to datetime
            df['TIMESTAMP'] = pd.to_datetime(df['timestamp'])
            df.drop(columns=['timestamp'], inplace=True)

            # Add 'TICKER' column with the ticker symbol
            df.insert(loc=1, column='TICKER', value=ticker.upper())

            log.info(f"Successfully fetched and processed data for ticker {ticker}.")

            # Reorder df columns
            df = df[['TIMESTAMP', 'TICKER', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']]

        except Exception as e:
            log.error(f"Failed to process data for ticker {ticker}: {str(e)}")
            raise Exception(f"Data processing error for ticker {ticker}: {str(e)}")

        try:
            self.ingest_dataframe(df=df, database=StockData)
        except Exception as e:
            log.error(f"Failed to ingest data for ticker {ticker}: {str(e)}")

        return df
