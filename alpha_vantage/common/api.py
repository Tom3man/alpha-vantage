import logging
import urllib.parse
from abc import ABC
from typing import Optional

import pandas as pd
from sqlite_forge.database import SqliteDatabase

from alpha_vantage import DATABASE_PATH
from alpha_vantage.common.key_manager import APIKeyManager

log = logging.getLogger(__name__)


class APIRequestError(Exception):
    """
    Custom exception for errors during API requests.

    Attributes:
        message (str): The error message associated with the exception.
        status_code (Optional[int]): The HTTP status code returned by the API, if applicable.
    """
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class AlphaVantageAPI(APIKeyManager, ABC):
    """
    Provides methods to interact with the Alpha Vantage API for extracting stock market data.

    The Alpha Vantage API offers access to a wide range of financial market data, requiring an active API key.
    API keys can be obtained by signing up at: https://www.alphavantage.co/support/

    Attributes:
        BASE_URL (str): The base URL for the Alpha Vantage API.

    Methods:
        build_url_request(function: str, **kwargs) -> str:
            Builds and returns the complete URL for making an API request to Alpha Vantage.
    """

    BASE_URL: str = "https://www.alphavantage.co/query"

    def __init__(self, *args, **kwargs):
        """
        Initialise the AlphaVantageAPI class, inheriting API key management from APIKeyManager.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

    def build_url_request(self, function: str, **kwargs) -> str:
        """
        Build the URL for the Alpha Vantage API request.

        Args:
            function (str): The function name to retrieve specific data (e.g., 'TIME_SERIES_INTRADAY').
            **kwargs: Additional parameters to include in the API request.

        Returns:
            str: The complete URL for the API request, including all query parameters.
        """
        # Create a dictionary for query parameters
        params = {
            "function": function,
            "apikey": self.api_key,
        }

        # Update the params dictionary with any additional keyword arguments (kwargs)
        params.update(kwargs)

        # Encode the parameters and construct the full URL
        url = f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"
        log.info(f"URL built: {url}")

        return url

    @staticmethod
    def ingest_dataframe(df: pd.DataFrame, database: SqliteDatabase):

        # Define the database path, either from the environment or defaulting to a relative path
        database_path = f"{DATABASE_PATH}/"

        # Initialise the database table handler
        database_inst = database(database_path=database_path)

        # Create the table if it doesn't exist and insert the data
        database_inst.create_table()

        if 'TIMESTAMP' in df:
            # Format to string for sqlite
            df['TIMESTAMP'] = df['TIMESTAMP'].astype(str)

        database_inst.ingest_dataframe(df=df)
