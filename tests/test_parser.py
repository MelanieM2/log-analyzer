"""
test_parser.py

Unit tests for log_analyzer/parser.py.
Tests cover: valid log line parsing, malformed line handling,
and full file parsing with mixed valid/invalid lines.
"""

import pytest
from log_analyzer.parser import parse_line, parse_file

class TestParseLine:
    """Tests for the parse_line() function."""

    def test_valid_info_line(self):
        line = "2026-06-18 10:23:45,123 - INFO - mymodule - Application started"
        result = parse_line(line)
        assert result is not None
        assert result["timestamp"] == "2026-06-18 10:23:45,123"
        assert result["level"] == "INFO"
        assert result["module"] == "mymodule"
        assert result["message"] == "Application started"

    def test_valid_error_line(self):
        line = "2026-06-18 10:23:48,012 - ERROR - database - Failed to connect"
        result = parse_line(line)
        assert result is not None
        assert result["level"] == "ERROR"
        assert result["module"] == "database"

    def test_malformed_line_returns_none(self):
        line = "this is not a valid log line"
        result = parse_line(line)
        assert result is None

    def test_empty_line_returns_none(self):
        result = parse_line("")
        assert result is None

    def test_all_levels_parsed(self):
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        for level in levels:
            line = f"2026-06-18 10:23:45,123 - {level} - mod - msg"
            result = parse_line(line)
            assert result is not None
            assert result["level"] == level



class TestParseFile:
    """Tests for the parse_file() function."""

    def test_parse_valid_file(self, tmp_path):
        log_file = tmp_path / "test.log"
        log_file.write_text(
            "2026-06-18 10:23:45,123 - INFO - mymodule - Application started\n"
            "2026-06-18 10:23:46,456 - ERROR - database - Connection failed\n"
        )
        records = parse_file(str(log_file))
        assert len(records) == 2
        assert records[0]["level"] == "INFO"
        assert records[1]["level"] == "ERROR"

    def test_malformed_lines_skipped(self, tmp_path):
        log_file = tmp_path / "test.log"
        log_file.write_text(
            "2026-06-18 10:23:45,123 - INFO - mymodule - Valid line\n"
            "this is malformed\n"
            "also malformed\n"
            "2026-06-18 10:23:46,456 - ERROR - database - Another valid line\n"
        )
        records = parse_file(str(log_file))
        assert len(records) == 2

    def test_empty_file_returns_empty_list(self, tmp_path):
        log_file = tmp_path / "test.log"
        log_file.write_text("")
        records = parse_file(str(log_file))
        assert records == []