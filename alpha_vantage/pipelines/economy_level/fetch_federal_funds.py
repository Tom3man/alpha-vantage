import logging

import pandas as pd

from alpha_vantage.common.api import AlphaVantageAPI

log = logging.getLogger(__name__)


class FederalFundsFetcher(AlphaVantageAPI):
    """
    A class for fetching federal funds data using the Alpha Vantage API.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the EconomicIndicatorsFetcher, inheriting API key management and request handling
        from the AlphaVantageAPI class.
        """
        super().__init__(*args, **kwargs)

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
