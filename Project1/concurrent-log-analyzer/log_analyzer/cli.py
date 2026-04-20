import argparse
from pathlib import Path

from log_analyzer.analyzer import analyze_entries
from log_analyzer.parser import parse_line
from log_analyzer.scanner import iter_log_files

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description = "Concurrent Log Analyzer - Phase 1"
    )

    parser.add_argument(
        "--dir",
        required=True,
        help="Directory containing log files",
    )
    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    all_entries = []

    for log_file in iter_log_files(args.dir):
        with open(log_file, "r", encoding = "utf-8") as f:
            for line in f:
                entry = parse_line(line, source_file=log_file.name)
                if entry is not None:
                    all_entries.append(entry)
    
    result = analyze_entries(all_entries)

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