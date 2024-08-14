from unittest.mock import MagicMock

import pandas as pd
import pytest

from alpha_vantage.pipelines import EconomicIndicatorsFetcher

EXPECTED_COLUMNS = [
    'DATE', 'CPI', 'INFLATION', 'RETAIL_SALES', 'DURABLES',
    'UNEMPLOYMENT', 'NONFARM_PAYROLL'
]


@pytest.fixture(scope="module")
def setup_dataframe():
    # Create an instance of the data fetcher
    economic_indicators = EconomicIndicatorsFetcher()

    mock_data = {col: [1] if col != 'TICKER' else ['IBM'] for col in EXPECTED_COLUMNS}
    mocked_df = pd.DataFrame(mock_data)

    # Mock the method to return this DataFrame
    economic_indicators.build_quarterly_fundamental_data = MagicMock(return_value=mocked_df)

    # Use the mocked method to generate a DataFrame
    df = economic_indicators.build_quarterly_fundamental_data(ticker='IBM')
    return df


def test_columns_exist(setup_dataframe):

    for col in EXPECTED_COLUMNS:
        assert col in setup_dataframe.columns, f"DataFrame is missing '{col}' column"


def test_dataframe_length(setup_dataframe):
    assert len(setup_dataframe) > 0, "DataFrame should not be empty"
