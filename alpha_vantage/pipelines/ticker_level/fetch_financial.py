import logging
import re

import pandas as pd

from alpha_vantage.common.api import AlphaVantageAPI
from alpha_vantage.tables import FinancialData

log = logging.getLogger(__name__)


class FinancialDataFetcher(AlphaVantageAPI):
    """
    Fetches and processes financial data for a given stock ticker using the Alpha Vantage API.

    This class provides methods to retrieve and build DataFrames for various financial statements
    such as balance sheets, income statements, cash flows, and earnings reports.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the FinancialDataFetcher, inheriting API key management and request handling
        from the AlphaVantageAPI class.
        """
        super().__init__(*args, **kwargs)

    def _build_balance_sheet(self, ticker: str) -> pd.DataFrame:
        """
        Retrieve and build a DataFrame for the balance sheet data.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            pd.DataFrame: A DataFrame containing the balance sheet data, with currency columns removed.
        """
        return self._build_dataframe(
            ticker, 'BALANCE_SHEET', 'quarterlyReports').drop(columns='REPORTED_CURRENCY')

    def _build_dataframe(self, ticker: str, function: str, data_key: str) -> pd.DataFrame:
        """
        Retrieve data from the API and build a DataFrame for a specific financial function.

        Args:
            ticker (str): The stock ticker symbol.
            function (str): The financial function to retrieve (e.g., 'BALANCE_SHEET', 'INCOME_STATEMENT').
            data_key (str): The key to access the relevant data in the API response.

        Returns:
            pd.DataFrame: A DataFrame constructed from the API response for the specified financial function.
        """
        kwargs = {'symbol': ticker, 'function': function}
        url = self.build_url_request(**kwargs)

        data = self.make_request(url=url)

        df = pd.DataFrame(data[data_key])

        # Convert camelCase to snake_case and uppercase all column names
        df.columns = [re.sub(r'(?<!^)(?=[A-Z])', '_', col).upper() for col in df.columns]

        return df

    def _build_income_statement(self, ticker: str) -> pd.DataFrame:
        """
        Retrieve and build a DataFrame for the income statement data.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            pd.DataFrame: A DataFrame containing the income statement data, with currency columns removed.
        """
        return self._build_dataframe(
            ticker, 'INCOME_STATEMENT', 'quarterlyReports').drop(columns='REPORTED_CURRENCY')

    def _build_cash_flow(self, ticker: str) -> pd.DataFrame:
        """
        Retrieve and build a DataFrame for the cash flow data.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            pd.DataFrame: A DataFrame containing the cash flow data, with currency columns removed.
        """
        return self._build_dataframe(
            ticker, 'CASH_FLOW', 'quarterlyReports').drop(columns='REPORTED_CURRENCY')

    def _build_earnings(self, ticker: str) -> pd.DataFrame:
        """
        Retrieve and build a DataFrame for the earnings data.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            pd.DataFrame: A DataFrame containing the earnings data.
        """
        return self._build_dataframe(
            ticker, 'EARNINGS', 'quarterlyEarnings')

    def get_financial_data(self, ticker: str) -> pd.DataFrame:
        """
        Build a consolidated DataFrame containing quarterly fundamental data for a stock.

        This method combines balance sheet, income statement, cash flow, and earnings data into a single DataFrame.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            pd.DataFrame: A DataFrame containing consolidated quarterly fundamental data for the given ticker.
        """
        balance_sheet = self._build_balance_sheet(ticker)
        income_statement = self._build_income_statement(ticker)
        cash_flow = self._build_cash_flow(ticker)
        earnings = self._build_earnings(ticker)

        # Merge all financial data on the fiscal date
        df = balance_sheet.merge(income_statement, on='FISCAL_DATE_ENDING', how='inner')
        df = df.merge(cash_flow, on='FISCAL_DATE_ENDING', how='inner')
        df = df.merge(earnings, on='FISCAL_DATE_ENDING', how='inner')

        # Insert the ticker symbol as a column
        df.insert(loc=1, column='TICKER', value=ticker.upper())

        # Group by relevant columns and aggregate by taking the maximum value
        group_by_cols = ['FISCAL_DATE_ENDING', 'TICKER', 'REPORTED_DATE', 'REPORT_TIME']
        df = df.groupby(group_by_cols).agg(
            {col: 'max' for col in df.columns if col not in group_by_cols}
        ).reset_index()

        # Drop duplicate rows
        df = df.drop_duplicates()

        try:
            self.ingest_dataframe(df=df, database=FinancialData)
        except Exception as e:
            log.error(f"Failed to ingest data for ticker {ticker}: {str(e)}")

        return df
