from typing import Optional

import click


@click.command(help="Fetches stock data for a given ticker and number of months.")
@click.option("--ticker", type=click.STRING, required=True, help="Stock ticker symbol (e.g., 'AAPL').")
@click.option("--n_months", type=click.INT, required=True, help="Number of months of data to fetch.")
@click.option("--interval", type=click.INT, default=5, help="Interval in minutes between data points.")
def main(ticker: str, n_months: int, interval: Optional[int] = 5):
    ...


if __name__ == "__main__":
    main()
