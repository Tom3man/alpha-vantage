import logging
import time

import pandas as pd

from alpha_vantage.common.api import AlphaVantageAPI

log = logging.getLogger(__name__)


class EconomicIndicatorsFetcher(AlphaVantageAPI):
    """
    A class for fetching monthly ndicators data using the Alpha Vantage API.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the EconomicIndicatorsFetcher, inheriting API key management and request handling
        from the AlphaVantageAPI class.
        """
        super().__init__(*args, **kwargs)

    def get_economic_indicators_data(self) -> pd.DataFrame:
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
