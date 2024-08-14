from typing import Dict, List

from sqlite_forge.database import SqliteDatabase


class StockData(SqliteDatabase):

    DEFAULT_PATH: str = "HISTORIC_STOCK"
    PRIMARY_KEY: List[str] = ["TIMESTAMP", "TICKER"]
    DEFAULT_SCHEMA: Dict[str, str] = {
        "TIMESTAMP": "DATE",
        "TICKER": "VARCHAR(6)",
        "OPEN": "DECIMAL(10,2)",
        "HIGH": "DECIMAL(10,2)",
        "LOW": "DECIMAL(10,2)",
        "CLOSE": "DECIMAL(10,2)",
        "VOLUME": "INT",
    }
