from typing import Dict, List

from sqlite_forge.database import SqliteDatabase


class SentimentData(SqliteDatabase):

    DEFAULT_PATH: str = "SENTIMENT_SCORES"
    PRIMARY_KEY: List[str] = ["DATE", "TIME", "TICKER", "TITLE", "SOURCE"]
    DEFAULT_SCHEMA: Dict[str, str] = {
        "DATE": "DATE",
        "TIME": "TEXT",
        "TICKER": "VARCHAR(6)",
        "TITLE": "VARCHAR(250)",
        "SOURCE": "VARCHAR(50)",
        "OVERALL_SENTIMENT_SCORE": "DECIMAL(1,7)",
    }
