import re
from typing import Optional

PYTHON_LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})"
    r" - (?P<level>\w+)"
    r" - (?P<module>\w+)"
    r" - (?P<message>.+)"
)

def parse_line(line: str) -> Optional[dict]:
    """Parse a single log line. Returns a dict or None if line doesn't match."""
    match = PYTHON_LOG_PATTERN.match(line.strip())
    if not match:
        return None
    return match.groupdict()

def parse_file(filepath: str) -> list[dict]:
    """Read a log file and return a list of parsed log records."""
    records = []
    with open(filepath, "r") as f:
        for line in f:
            record = parse_line(line)
            if record is not None:
                records.append(record)
    return records
