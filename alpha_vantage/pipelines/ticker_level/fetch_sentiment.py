import logging
from datetime import datetime
from typing import List, Optional, Tuple

import pandas as pd
import requests

from alpha_vantage.common.api import AlphaVantageAPI
from alpha_vantage.tables import SentimentData

log = logging.getLogger(__name__)


class NewsSentimentFetcher(AlphaVantageAPI):
    """
    A class for fetching news sentiment data using the Alpha Vantage API.

    This class provides methods to retrieve and process news sentiment data for a given stock ticker
    and year, allowing users to analyze the overall sentiment in financial news articles.

    Args:
        api_key (str): Your Alpha Vantage API key.

    Attributes:
        api_key (str): Your Alpha Vantage API key.

    Methods:
        build_urls(ticker: str, year: int) -> List[str]:
            Constructs URLs for fetching news sentiment data for a specific ticker and year.

        get_data(ticker: str, year: int) -> pd.DataFrame:
            Retrieves and aggregates news sentiment data from the constructed URLs into a single DataFrame.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the NewsSentimentFetcher, inheriting API key management and request handling
        from the AlphaVantageAPI class.
        """
        super().__init__(*args, **kwargs)

    @staticmethod
    def _generate_time_range(year: int) -> Tuple[str, str, str]:
        """
        Generate the start, mid, and end timestamps for a given year.

        Args:
            year (int): The year for which the time range is to be generated.

        Returns:
            Tuple[str, str, str]: A tuple containing the start, mid, and end timestamps formatted for the API.
        """
        time_start = f"{year}0101T0130"
        time_mid = f"{year}0630T0130"
        time_end = f"{year}1231T0130"
        return time_start, time_mid, time_end

    def build_urls(self, ticker: str, year: int) -> List[str]:
        """
        Construct URLs for fetching news sentiment data for a specific ticker and year.

        Args:
            ticker (str): The stock ticker symbol.
            year (int): The year for which to fetch news sentiment data.

        Returns:
            List[str]: A list of URLs to fetch news sentiment data for the specified ticker and year.

        Raises:
            ValueError: If the year is not within the valid range (2022 to current year).
        """
        current_year = datetime.now().year
        if year < 2022 or year > current_year:
            raise ValueError(f"Invalid year provided: {year}. Year must be between 2022 and {current_year}.")

        time_start, time_mid, time_end = self._generate_time_range(year=year)

        # Build URLs for the first and second half of the year
        kwargs = {'ticker': ticker, 'function': 'NEWS_SENTIMENT', 'limit': 1000, 'sort': 'RELEVANCE'}
        urls = [
            self.build_url_request(
                time_from=time_start,
                time_to=time_mid,
                **kwargs
            ),
            self.build_url_request(
                time_from=time_mid,
                time_to=time_end,
                **kwargs
            )
        ]
        return urls

    def get_sentiment_data(self, ticker: str, year: Optional[int] = None) -> pd.DataFrame:
        """
        Retrieve and aggregate news sentiment data for a specific ticker and year.

        This method fetches news sentiment data from Alpha Vantage API using the constructed URLs,
        processes the data, and returns a consolidated DataFrame with all entries.

        Args:
            ticker (str): The stock ticker symbol to fetch data for.
            year (int): The year for which to fetch news sentiment data.

        Returns:
            pd.DataFrame: A DataFrame containing aggregated news sentiment data.

        Raises:
            ValueError: If there are issues with HTTP requests, JSON decoding, or other unexpected errors.
        """

        if not year:

            # Get the current year
            current_year = datetime.now().year

            # Generate a list of years from 2022 to the current year
            years_list = list(range(2022, current_year + 1))

            urls = []
            for y in years_list:
                urls.extend(self.build_urls(ticker=ticker, year=y))

        dfs = []

        for url in urls:
            try:
                data = self.make_request(url=url)

                # Select relevant columns
                cols = ['time_published', 'title', 'source', 'overall_sentiment_score']
                df = pd.DataFrame([{col: item[col] for col in cols} for item in data['feed']])

                # Convert and rename columns
                df['time_published'] = pd.to_datetime(df['time_published'], format='%Y%m%dT%H%M%S')
                df.rename(columns={col: col.upper() for col in cols}, inplace=True)

                dfs.append(df)

            except requests.HTTPError as e:
                log.error(f"HTTP error occurred: {e}")
                raise ValueError(f"HTTP error occurred: {e}")
            except requests.RequestException as e:
                log.error(f"Error fetching data from {url}: {e}")
                raise ValueError(f"Error fetching data from {url}: {e}")
            except ValueError as e:
                log.error(f"Error decoding JSON data: {e}")
                raise ValueError(f"Error decoding JSON data: {e}")
            except Exception as e:
                log.error(f"An unexpected error occurred: {e}")
                raise ValueError(f"An unexpected error occurred: {e}")

        if dfs:
            full_df = pd.concat(dfs).drop_duplicates()

            # Format datetime into Date and Time
            full_df['TIME_PUBLISHED'] = pd.to_datetime(full_df['TIME_PUBLISHED'])

            # Split the datetime column into date and time
            full_df.insert(loc=0, column='DATE', value=full_df['TIME_PUBLISHED'].dt.date)
            full_df.insert(loc=1, column='TIME', value=full_df['TIME_PUBLISHED'].dt.time)

            full_df['TIME'] = full_df['TIME'].astype(str)

            full_df.drop(columns=['TIME_PUBLISHED'], inplace=True)

            # Insert ticker column
            full_df.insert(loc=2, column='TICKER', value=ticker.upper())

            # Function to retrieve the row with the most extreme sentiment score within each group
            def get_most_extreme_row(group):
                return group.loc[group['OVERALL_SENTIMENT_SCORE'].abs().idxmax()]

            # Group by the specified columns and apply the custom function
            full_df = full_df.groupby(
                ['DATE', 'TIME', 'TICKER', 'SOURCE', 'TITLE']
            ).apply(get_most_extreme_row)

            # Reset index to ensure no groupby index is left
            full_df.reset_index(drop=True, inplace=True)

        else:
            return pd.DataFrame()

        try:
            self.ingest_dataframe(df=full_df, database=SentimentData)
        except Exception as e:
            log.error(f"Failed to ingest data for ticker {ticker}: {str(e)}")

        return full_df
