from typing import Dict, List

from sqlite_forge.database import SqliteDatabase


class IndicatorData(SqliteDatabase):

    DEFAULT_PATH: str = "FINANCIAL_INDICATORS"
    PRIMARY_KEY: List[str] = ["DATE"]
    DEFAULT_SCHEMA: Dict[str, str] = {
        "DATE": "DATE",
        "CPI": "DECIMAL(4, 4)",
        "INFLATION": "DECIMAL(3,10)",
        "RETAIL_SALES": "BIGINT",
        "DURABLES": "INT",
        "UNEMPLOYMENT": "DECIMAL(2,2)",
        "NONFARM_PAYROLL": "INT",
    }
