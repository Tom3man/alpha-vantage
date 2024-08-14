import logging
import time

import pandas as pd

from alpha_vantage.common.api import AlphaVantageAPI

log = logging.getLogger(__name__)


class TreasuryYieldFetcher(AlphaVantageAPI):
    """
    A class for fetching various treasury yield the Alpha Vantage API.
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
