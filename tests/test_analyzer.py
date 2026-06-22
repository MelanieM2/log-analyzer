"""
test_analyzer.py

Unit tests for log_analyzer/analyzer.py.
Tests cover: DataFrame loading, level counts, module counts,
error filtering, and summary dict construction.
"""

import pytest
import pandas as pd
from log_analyzer.analyzer import (
    load_dataframe,
    count_by_level,
    count_by_module,
    get_errors,
    build_summary,
)

@pytest.fixture  # this decorator tells pytest "the function below provides reusable test data". 
def sample_df():
    """Reusable sample DataFrame for all analyzer tests."""
    records = [
        {"timestamp": "2026-06-18 10:23:45,123", "level": "INFO", "module": "mymodule", "message": "Application started"},
        {"timestamp": "2026-06-18 10:23:46,456", "level": "DEBUG", "module": "mymodule", "message": "Loading config"},
        {"timestamp": "2026-06-18 10:23:47,789", "level": "WARNING", "module": "database", "message": "Connection pool low"},
        {"timestamp": "2026-06-18 10:23:48,012", "level": "ERROR", "module": "database", "message": "Connection failed"},
        {"timestamp": "2026-06-18 10:23:50,678", "level": "CRITICAL", "module": "database", "message": "All connections failed"},
    ]
    return load_dataframe(records)



class TestAnalyzer:
    """Tests for analyzer functions."""

    def test_load_dataframe_shape(self, sample_df):
        assert sample_df.shape == (5, 4)

    def test_load_dataframe_columns(self, sample_df):
        assert list(sample_df.columns) == ["timestamp", "level", "module", "message"]

    def test_count_by_level(self, sample_df):
        counts = count_by_level(sample_df)
        assert counts["INFO"] == 1
        assert counts["ERROR"] == 1
        assert counts["CRITICAL"] == 1

    def test_count_by_module(self, sample_df):
        counts = count_by_module(sample_df)
        assert counts["mymodule"] == 2
        assert counts["database"] == 3

    def test_get_errors_returns_only_errors(self, sample_df):
        errors = get_errors(sample_df)
        assert len(errors) == 2
        assert set(errors["level"].tolist()) == {"ERROR", "CRITICAL"}

    def test_get_errors_correct_messages(self, sample_df):
        errors = get_errors(sample_df)
        messages = errors["message"].tolist()
        assert "Connection failed" in messages
        assert "All connections failed" in messages

    def test_build_summary_structure(self, sample_df):
        summary = build_summary(sample_df)
        assert "total" in summary
        assert "by_level" in summary
        assert "by_module" in summary
        assert "errors" in summary

    def test_build_summary_total(self, sample_df):
        summary = build_summary(sample_df)
        assert summary["total"] == 5

    def test_build_summary_errors_list(self, sample_df):
        summary = build_summary(sample_df)
        assert isinstance(summary["errors"], list)
        assert len(summary["errors"]) == 2