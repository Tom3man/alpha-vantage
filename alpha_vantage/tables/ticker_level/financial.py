from typing import Dict, List
from sqlite_forge.database import SqliteDatabase


class FinancialData(SqliteDatabase):
    DEFAULT_PATH: str = "FUNDAMENTAL_DATA"
    PRIMARY_KEY: List[str] = ["FISCAL_DATE_ENDING", "TICKER"]
    DEFAULT_SCHEMA: Dict[str, str] = {
        "FISCAL_DATE_ENDING": "DATE",
        "TICKER": "VARCHAR(6)",
        "TOTAL_ASSETS": "BIGINT",
        "TOTAL_CURRENT_ASSETS": "BIGINT",
        "CASH_AND_CASH_EQUIVALENTS_AT_CARRYING_VALUE": "BIGINT",
        "CASH_AND_SHORT_TERM_INVESTMENTS": "BIGINT",
        "INVENTORY": "BIGINT",
        "CURRENT_NET_RECEIVABLES": "BIGINT",
        "TOTAL_NON_CURRENT_ASSETS": "BIGINT",
        "PROPERTY_PLANT_EQUIPMENT": "BIGINT",
        "ACCUMULATED_DEPRECIATION_AMORTIZATION_P_P_E": "BIGINT",
        "INTANGIBLE_ASSETS": "BIGINT",
        "INTANGIBLE_ASSETS_EXCLUDING_GOODWILL": "BIGINT",
        "GOODWILL": "BIGINT",
        "INVESTMENTS": "BIGINT",
        "LONG_TERM_INVESTMENTS": "BIGINT",
        "SHORT_TERM_INVESTMENTS": "BIGINT",
        "OTHER_CURRENT_ASSETS": "BIGINT",
        "OTHER_NON_CURRENT_ASSETS": "BIGINT",
        "TOTAL_LIABILITIES": "BIGINT",
        "TOTAL_CURRENT_LIABILITIES": "BIGINT",
        "CURRENT_ACCOUNTS_PAYABLE": "BIGINT",
        "DEFERRED_REVENUE": "BIGINT",
        "CURRENT_DEBT": "BIGINT",
        "SHORT_TERM_DEBT": "BIGINT",
        "TOTAL_NON_CURRENT_LIABILITIES": "BIGINT",
        "CAPITAL_LEASE_OBLIGATIONS": "BIGINT",
        "LONG_TERM_DEBT": "BIGINT",
        "CURRENT_LONG_TERM_DEBT": "BIGINT",
        "LONG_TERM_DEBT_NONCURRENT": "BIGINT",
        "SHORT_LONG_TERM_DEBT_TOTAL": "BIGINT",
        "OTHER_CURRENT_LIABILITIES": "BIGINT",
        "OTHER_NON_CURRENT_LIABILITIES": "BIGINT",
        "TOTAL_SHAREHOLDER_EQUITY": "BIGINT",
        "TREASURY_STOCK": "BIGINT",
        "RETAINED_EARNINGS": "BIGINT",
        "COMMON_STOCK": "BIGINT",
        "COMMON_STOCK_SHARES_OUTSTANDING": "BIGINT",
        "GROSS_PROFIT": "BIGINT",
        "TOTAL_REVENUE": "BIGINT",
        "COST_OF_REVENUE": "BIGINT",
        "COSTOF_GOODS_AND_SERVICES_SOLD": "BIGINT",
        "OPERATING_INCOME": "BIGINT",
        "SELLING_GENERAL_AND_ADMINISTRATIVE": "BIGINT",
        "RESEARCH_AND_DEVELOPMENT": "BIGINT",
        "OPERATING_EXPENSES": "BIGINT",
        "INVESTMENT_INCOME_NET": "BIGINT",
        "NET_INTEREST_INCOME": "BIGINT",
        "INTEREST_INCOME": "BIGINT",
        "INTEREST_EXPENSE": "BIGINT",
        "NON_INTEREST_INCOME": "BIGINT",
        "OTHER_NON_OPERATING_INCOME": "BIGINT",
        "DEPRECIATION": "BIGINT",
        "DEPRECIATION_AND_AMORTIZATION": "BIGINT",
        "INCOME_BEFORE_TAX": "BIGINT",
        "INCOME_TAX_EXPENSE": "BIGINT",
        "INTEREST_AND_DEBT_EXPENSE": "BIGINT",
        "NET_INCOME_FROM_CONTINUING_OPERATIONS": "BIGINT",
        "COMPREHENSIVE_INCOME_NET_OF_TAX": "BIGINT",
        "EBIT": "BIGINT",
        "EBITDA": "BIGINT",
        "NET_INCOME_x": "BIGINT",
        "OPERATING_CASHFLOW": "BIGINT",
        "PAYMENTS_FOR_OPERATING_ACTIVITIES": "BIGINT",
        "PROCEEDS_FROM_OPERATING_ACTIVITIES": "BIGINT",
        "CHANGE_IN_OPERATING_LIABILITIES": "BIGINT",
        "CHANGE_IN_OPERATING_ASSETS": "BIGINT",
        "DEPRECIATION_DEPLETION_AND_AMORTIZATION": "BIGINT",
        "CAPITAL_EXPENDITURES": "BIGINT",
        "CHANGE_IN_RECEIVABLES": "BIGINT",
        "CHANGE_IN_INVENTORY": "BIGINT",
        "PROFIT_LOSS": "BIGINT",
        "CASHFLOW_FROM_INVESTMENT": "BIGINT",
        "CASHFLOW_FROM_FINANCING": "BIGINT",
        "PROCEEDS_FROM_REPAYMENTS_OF_SHORT_TERM_DEBT": "BIGINT",
        "PAYMENTS_FOR_REPURCHASE_OF_COMMON_STOCK": "BIGINT",
        "PAYMENTS_FOR_REPURCHASE_OF_EQUITY": "BIGINT",
        "PAYMENTS_FOR_REPURCHASE_OF_PREFERRED_STOCK": "BIGINT",
        "DIVIDEND_PAYOUT": "BIGINT",
        "DIVIDEND_PAYOUT_COMMON_STOCK": "BIGINT",
        "DIVIDEND_PAYOUT_PREFERRED_STOCK": "BIGINT",
        "PROCEEDS_FROM_ISSUANCE_OF_COMMON_STOCK": "BIGINT",
        "PROCEEDS_FROM_ISSUANCE_OF_LONG_TERM_DEBT_AND_CAPITAL_SECURITIES_NET": "BIGINT",
        "PROCEEDS_FROM_ISSUANCE_OF_PREFERRED_STOCK": "BIGINT",
        "PROCEEDS_FROM_REPURCHASE_OF_EQUITY": "BIGINT",
        "PROCEEDS_FROM_SALE_OF_TREASURY_STOCK": "BIGINT",
        "CHANGE_IN_CASH_AND_CASH_EQUIVALENTS": "BIGINT",
        "CHANGE_IN_EXCHANGE_RATE": "BIGINT",
        "NET_INCOME_y": "BIGINT",
        "REPORTED_DATE": "DATE",
        "REPORTED_E_P_S": "DECIMAL(10,2)",
        "ESTIMATED_E_P_S": "DECIMAL(10,2)",
        "SURPRISE": "DECIMAL(10,2)",
        "SURPRISE_PERCENTAGE": "DECIMAL(10,2)",
        "REPORT_TIME": "VARCHAR(20)",
    }
