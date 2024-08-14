import logging

from alpha_vantage.pipelines import (EconomicIndicatorsFetcher,
                                     FederalFundsFetcher, FinancialDataFetcher,
                                     NewsSentimentFetcher, StockPriceFetcher,
                                     TreasuryYieldFetcher)

log = logging.getLogger(__name__)


class TotalDataFetcher(
    EconomicIndicatorsFetcher, FederalFundsFetcher, FinancialDataFetcher,
    NewsSentimentFetcher, StockPriceFetcher, TreasuryYieldFetcher
):
    """
    A mega class that combines the functionality of FinancialDataFetcher, EconomicIndicatorsFetcher,
    NewsSentimentFetcher, and StockPriceFetcher, inheriting the Singleton pattern from APIKeyManager.

    This class provides a unified interface for fetching financial data, economic indicators,
    news sentiment data, and stock prices, all while tracking API usage through the Singleton pattern.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialise the MegaDataFetcher, which automatically initializes the parent classes,
        ensuring that the API key management and Singleton behavior are inherited.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
