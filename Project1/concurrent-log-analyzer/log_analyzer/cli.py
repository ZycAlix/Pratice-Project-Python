import argparse
from pathlib import Path

from log_analyzer.analyzer import analyze_entries
from log_analyzer.parser import iter_entries_from_file
from log_analyzer.scanner import iter_log_files

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description = "Concurrent Log Analyzer - Phase 1.5"
    )

    parser.add_argument(
        "--dir",
        required=True,
        help="Directory containing log files",
    )
    return parser

def iter_all_entries(directory: str):
    """
    Yield LogEntry objects from all log files under the directory.
    """
    for log_file in iter_log_files(directory):
        yield from iter_entries_from_file(log_file)

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    entries = iter_all_entries(args.dir)
    result = analyze_entries(entries)

    print("=" * 60)
    print("LOG ANALYSIS REPORT")
    print("=" * 60)
    print(f"Total parsed lines: {result['total_lines']}")
    print()

    print("Level counts:")
    for level, count in result["levels"].items():
        print(f"  {level:<8} {count}")

    print()
    print("Service counts:")
    for service, count in result["services"].items():
        print(f"  {service:<20} {count}")

    print()
    print("Top error codes:")
    for event_code, count in result["top_error_codes"]:
        print(f"  {event_code:<25} {count}")


if __name__ == "__main__":
    main()