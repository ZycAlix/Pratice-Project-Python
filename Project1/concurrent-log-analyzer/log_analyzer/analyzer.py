from collections import Counter
from typing import Iterable

from log_analyzer.models import LogEntry


def analyze_entries(entries: Iterable[LogEntry]) -> dict:
    """
    Analyze parsed log entries and return raw counters.
    This version keeps Counter objects so partial results can be merged later.
    """
    total_lines = 0
    level_counter = Counter()
    error_code_counter = Counter()
    service_counter = Counter()

    for entry in entries:
        total_lines += 1
        level_counter[entry.level] += 1
        service_counter[entry.service] += 1

        if entry.level == "ERROR":
            error_code_counter[entry.event_code] += 1

    return {
        "total_lines": total_lines,
        "levels": level_counter,
        "services": service_counter,
        "error_codes": error_code_counter,
    }


def merge_analysis_results(results: list[dict]) -> dict:
    """
    Merge multiple partial analysis results into one final report.
    """
    total_lines = 0
    level_counter = Counter()
    service_counter = Counter()
    error_code_counter = Counter()

    for result in results:
        total_lines += result["total_lines"]
        level_counter.update(result["levels"])
        service_counter.update(result["services"])
        error_code_counter.update(result["error_codes"])

    return {
        "total_lines": total_lines,
        "levels": dict(level_counter),
        "services": dict(service_counter),
        "top_error_codes": error_code_counter.most_common(10),
    }