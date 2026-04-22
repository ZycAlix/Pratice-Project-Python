import argparse

from log_analyzer.analyzer import analyze_entries
from log_analyzer.concurrency import analyze_files_concurrently
from log_analyzer.parser import iter_entries_from_file
from log_analyzer.reporters import write_csv_report, write_json_report
from log_analyzer.scanner import iter_log_files


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Concurrent Log Analyzer - Phase 3"
    )
    parser.add_argument(
        "--dir",
        required=True,
        help="Directory containing log files",
    )
    parser.add_argument(
        "--json-out",
        help="Optional path to write JSON report",
    )
    parser.add_argument(
        "--csv-out",
        help="Optional path to write CSV report",
    )
    parser.add_argument(
        "--concurrent",
        action="store_true",
        help="Enable concurrent file analysis using a thread pool",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of worker threads when --concurrent is enabled",
    )
    return parser


def iter_all_entries(directory: str):
    """
    Yield LogEntry objects from all log files under the directory.
    """
    for log_file in iter_log_files(directory):
        yield from iter_entries_from_file(log_file)


def print_report(result: dict) -> None:
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


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.concurrent:
        log_files = list(iter_log_files(args.dir))
        result = analyze_files_concurrently(log_files, max_workers=args.workers)
    else:
        entries = iter_all_entries(args.dir)
        raw_result = analyze_entries(entries)
        result = {
            "total_lines": raw_result["total_lines"],
            "levels": dict(raw_result["levels"]),
            "services": dict(raw_result["services"]),
            "top_error_codes": raw_result["error_codes"].most_common(10),
        }

    print_report(result)

    if args.json_out:
        write_json_report(result, args.json_out)
        print(f"\nJSON report written to: {args.json_out}")

    if args.csv_out:
        write_csv_report(result, args.csv_out)
        print(f"CSV report written to: {args.csv_out}")


if __name__ == "__main__":
    main()