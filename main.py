"""
main.py

Command-line interface for the Log Analyzer.

Usage:
    uv run main.py --input <logfile> [--output <reportfile>] [--ai-summary]

Arguments:
    --input       Path to the log file to analyze (required)
    --output      Path to save the report (optional, prints to stdout if omitted)
    --ai-summary  Request a natural language summary from Gemini (optional flag)
"""

import argparse # Python's built-in library for building command-line interfaces
import sys
from log_analyzer.parser import parse_file
from log_analyzer.analyzer import load_dataframe, build_summary
from log_analyzer.gemini_client import analyze_logs


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze log files and optionally generate an AI summary."
    )           #  creates the CLI engine


    parser.add_argument(
        "--input",
        required=True,
        help="Path to the log file to analyze."
    )
    parser.add_argument(
        "--output",
        required=False,
        default=None,
        help="Path to save the report. Prints to stdout if omitted."
    )
    parser.add_argument(
        "--ai-summary",
        action="store_true",
        help="Request a natural language summary from Gemini."
    )
    args = parser.parse_args()






    # Parse the log file
    records = parse_file(args.input)
    if not records:
        print(f"ERROR: No valid log records found in {args.input}", file=sys.stderr)
        sys.exit(1)

    # Load into DataFrame and build summary
    df = load_dataframe(records)
    summary = build_summary(df)

    # Build the report text
    report_lines = [
        f"Log Analysis Report",
        f"===================",
        f"File:    {args.input}",
        f"Total entries:  {summary['total']}",
        f"",
        f"Entries by level:",
    ]
    for level, count in summary["by_level"].items():
        report_lines.append(f"  {level:<10} {count}")

    report_lines.append("")
    report_lines.append("Entries by module:")
    for module, count in summary["by_module"].items():
        report_lines.append(f"  {module:<15} {count}")

    if summary["errors"]:
        report_lines.append("")
        report_lines.append("Errors and critical messages:")
        for msg in summary["errors"]:
            report_lines.append(f"  - {msg}")

    # Add Gemini summary if requested
    if args.ai_summary:
        print("Calling Gemini for AI summary...", file=sys.stderr)
        analysis = analyze_logs(summary)
        report_lines.append("")
        report_lines.append("AI Summary:")
        report_lines.append("===========")
        report_lines.append(analysis)

    # Output the report
    report = "\n".join(report_lines)
    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"Report saved to {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
