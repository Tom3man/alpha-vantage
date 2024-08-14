import logging
import time

import pandas as pd

from alpha_vantage.common.api import AlphaVantageAPI

log = logging.getLogger(__name__)


class EconomicIndicatorsFetcher(AlphaVantageAPI):
    """
    A class for fetching various economic indicators using the Alpha Vantage API.

    This class provides methods to retrieve U.S. Treasury yield data, the U.S. Federal Funds Rate, and
    various monthly economic indicators such as CPI, inflation,
    retail sales, durables, unemployment, and nonfarm payrolls.

    Args:
        api_key (str): Your Alpha Vantage API key.

    Attributes:
        api_key (str): Your Alpha Vantage API key.

    Methods:
        treasury_yield() -> pd.DataFrame:
            Fetches U.S. Treasury yield data for various maturities.

        federal_funds() -> pd.DataFrame:
            Fetches the U.S. Federal Funds Rate data.

        monthly_indicators() -> pd.DataFrame:
            Fetches various monthly economic indicators.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the EconomicIndicatorsFetcher, inheriting API key management and request handling
        from the AlphaVantageAPI class.
        """
        super().__init__(*args, **kwargs)

    def get_treasury_yield_data(self) -> pd.DataFrame:
        """
        Fetch U.S. Treasury yield data for various maturities.

        This method retrieves daily Treasury yield data for multiple maturities (3-month, 2-year, 5-year, 7-year,
        10-year, and 30-year) from the Alpha Vantage API. It then combines the data into a single DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing Treasury yield data for various maturities.
        """
        dfs = []
        MATURITY_INTERVALS = ['3month', '2year', '5year', '7year', '10year', '30year']
        log.info(f"This method will use up {len(MATURITY_INTERVALS)} API calls.")
        for maturity in MATURITY_INTERVALS:
            # Create query parameters for the API request
            kwargs = {
                "function": 'TREASURY_YIELD',
                "interval": 'daily',
                "maturity": maturity,
            }
            url = self.build_url_request(**kwargs)
            data = self.make_request(url=url)

            df = pd.DataFrame(data['data'])
            df.columns = ['Date', f'TREASURY_YIELD_{maturity.upper()}']
            df['Date'] = pd.to_datetime(df['Date'])

            dfs.append(df)

            time.sleep(5)  # Wait to avoid hitting API rate limits

        # Merge all DataFrames on the 'Date' column
        full_df = pd.concat(
            [dfs[0]] + [df.drop(columns=['Date']) for df in dfs[1:]], axis=1, join='inner')

        return full_df

    def get_federal_funds_data(self) -> pd.DataFrame:
        """
        Fetch the U.S. Federal Funds Rate data.

        This method retrieves daily Federal Funds Rate data from the Alpha Vantage API and returns it as a DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing Federal Funds Rate data.
        """
        kwargs = {
            "function": 'FEDERAL_FUNDS_RATE',
            "interval": 'daily',
        }
        log.info("This method will use up 1 API call.")
        url = self.build_url_request(**kwargs)
        data = self.make_request(url=url)

        df = pd.DataFrame(data['data'])
        df.columns = ['Date', 'FEDERAL_FUNDS_RATE']

        return df

    def get_monthly_indicators_data(self) -> pd.DataFrame:
        """
        Fetch various monthly economic indicators.

        This method retrieves monthly data for several key economic indicators including CPI, inflation, retail sales,
        durables, unemployment, and nonfarm payrolls from the Alpha Vantage API. It then combines the data into a
        single DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing various monthly economic indicators.
        """
        dfs = []
        indicators = ['CPI', 'INFLATION', 'RETAIL_SALES', 'DURABLES', 'UNEMPLOYMENT', 'NONFARM_PAYROLL']

        log.info(f"This method will use up {len(indicators)} API calls.")
        for func in indicators:
            kwargs = {
                "function": func,
            }
            url = self.build_url_request(**kwargs)
            data = self.make_request(url=url)

            df = pd.DataFrame(data['data'])
            df.columns = ['DATE', func.upper()]
            df['DATE'] = pd.to_datetime(df['DATE'])

            dfs.append(df)

            time.sleep(5)  # Wait to avoid hitting API rate limits

        # Merge all DataFrames on the 'DATE' column
        full_df = pd.concat(
            [dfs[0]] + [df.drop(columns=['DATE']) for df in dfs[1:]], axis=1, join='inner')

        full_df['DATE'] = full_df['DATE'].dt.date

        return full_df
