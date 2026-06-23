# Log Analyzer

A command-line tool that parses log files, analyzes them using Pandas, and optionally generates a natural language summary using the Gemini API.

This is Project 2 in a personal learning roadmap toward Data Science and ML Engineering, building directly on the git workflow, Python packaging, and security practices established in [linux-system-inspector](https://github.com/MelanieM2/linux-system-inspector).

---

## Features

- Parses Python-format log files using regex
- Loads parsed records into a Pandas DataFrame
- Produces structured summaries: entry counts by severity level and by module, error and critical message extraction
- Optionally calls the Gemini API to generate a plain-English analysis of what the logs are telling you
- CLI interface with `--input`, `--output`, and `--ai-summary` flags
- Supply chain security framework inherited from Project 1

---

## Installation

Requires [uv](https://github.com/astral-sh/uv).

```bash
git clone git@github.com:MelanieM2/log-analyzer.git
cd log-analyzer
uv sync
```

`uv sync` will install all pinned dependencies from `uv.lock` and verify cryptographic checksums before installation.

---

## Usage

### Basic analysis (stdout)

```bash
uv run main.py --input /path/to/logfile.log
```

### Save report to file

```bash
uv run main.py --input /path/to/logfile.log --output report.md
```

### With Gemini AI summary

```bash
uv run main.py --input /path/to/logfile.log --ai-summary
```

### Full example

```bash
uv run main.py --input /var/log/syslog --output report.md --ai-summary
```

---

## Real World Log Sources

This tool works with any log file in standard Python logging format. Practical sources include:

- **Linux system logs** — `/var/log/syslog`, `/var/log/auth.log`, `/var/log/kern.log`
- **Your own Python projects** — any script using Python's built-in `logging` module
- **Remote machines via SSH** — pull logs from a remote host (e.g. an Acer server) and analyze locally
- **Web servers** — Apache and Nginx log format support is planned for a future release

---

## Project Structure

```
log-analyzer/
├── log_analyzer/
│   ├── __init__.py
│   ├── parser.py         # Regex-based log line parser
│   ├── analyzer.py       # Pandas DataFrame analysis and summary
│   ├── gemini_client.py  # Gemini API integration
│   └── reporter.py       # (planned) formatted report output
├── tests/
│   ├── test_parser.py    # 8 unit tests for parser
│   ├── test_analyzer.py  # 9 unit tests for analyzer
│   └── test_security.py  # API key environment check
├── main.py               # CLI entry point
├── pyproject.toml        # Project config and pinned dependencies
└── uv.lock               # Cryptographic lockfile
```

---

## Security

This project follows the same supply chain security framework as `linux-system-inspector`:

- All dependencies pinned to exact versions (`==`) via `add-bounds = "exact"` in `pyproject.toml`
- 7-day quarantine buffer via `exclude-newer = "7 days ago"` — no packages released in the last 7 days are installed
- `uv.lock` committed to version control with cryptographic checksums for every package
- `uv audit` run before every dependency commit — no known vulnerabilities
- Gemini API key loaded from environment variable (`GEMINI_API_KEY`) — never hardcoded

See `SECURITY.md` for full details.

---

## Running Tests

```bash
uv run pytest tests/ -v
```

17 tests, all passing.

---


## Development Notes & AI Usage

### AI-Assisted Pair-Programming

This repository is the result of an independent learning and development workflow, not agentic automation. While Claude Sonnet 4.6 was used to:

* generate structural snippets,
* clarify unfamiliar concepts,
* explore architectural design options,
* review and iterate on code structure,
* accelerate development of boilerplate and automation logic,

its output was above all used as a learning foundation. I evaluated, corrected, and manually typed the implementation to ensure a personal understanding of system design principles in Linux and Python.

---

### Runtime AI Integration

In addition to development support, the system integrates the Google Gemini API (`gemini-3.1-flash-lite`) at runtime to generate natural language log analysis from structured Pandas summaries.

---

## Project Context

This project is part of a broader personal learning roadmap through Data Science, ML Engineering, and Agentic AI including:

* Python-based automation systems
* Linux system architecture and infrastructure design
* Bash scripting for workflow automation
* Applied machine learning and LLM-integrated pipelines

The goal is to bridge theoretical foundations in mathematics and machine learning with practical systems engineering and production-style automation workflow

---

**Connections to other projects:**
- Inherits git workflow and security framework from `linux-system-inspector` (Project 1)
- Shares Gemini API integration pattern with `research_digester`
- Planned: SSH into Acer machine, pull real `/var/log/syslog`, analyze it with this tool
- ...
<!--
- Planned: Apache/Nginx log format support
- Stretch goal: agentic loop — parse → ask Gemini what to look for next → re-parse → synthesise findings
-->
---