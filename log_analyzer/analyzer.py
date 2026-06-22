"""
analyzer.py

Takes parsed log records from parser.py and loads them into a Pandas DataFrame.

Produces the following summaries:
    - Count of log entries by level (INFO, WARNING, ERROR, etc.)
    - Count of log entries by module
    - Most recent errors
"""
import pandas as pd
from typing import Optional


def load_dataframe(records: list[dict]) -> pd.DataFrame:
    """Load a list of parsed log records into a Pandas DataFrame."""
    return pd.DataFrame(records)

def count_by_level(df: pd.DataFrame) -> pd.Series:
    """Count log entries grouped by severity level."""
    return df["level"].value_counts()


def count_by_module(df: pd.DataFrame) -> pd.Series:
    """Count log entries grouped by module name."""
    return df["module"].value_counts()


def get_errors(df: pd.DataFrame) -> pd.DataFrame:
    """Return only ERROR and CRITICAL log entries."""
    return df[df["level"].isin(["ERROR", "CRITICAL"])]