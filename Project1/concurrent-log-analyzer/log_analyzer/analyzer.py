from collections import Counter
from typing import Iterable

from log_analyzer.models import LogEntry

def analyze_entries(entries: Iterable[LogEntry]) -> dict:
    """
    Analyze parsed log entries and return summary statistics.
    """
    total_lines = 0
    level_counter = Counter()
    error_code_counter = Counter()
    service_counter = Counter()

    for entry in entries:
        total_lines +=1
        level_counter[entry.level] +=1
        service_counter[entry.service] +=1

        if entry.level == "ERROR":
            error_code_counter[entry.event_code] +=1
    
    return {
        "total_lines": total_lines,
        "levels": dict(level_counter),
        "services": dict(service_counter),
        "top_error_codes": error_code_counter.most_common(10),
    }