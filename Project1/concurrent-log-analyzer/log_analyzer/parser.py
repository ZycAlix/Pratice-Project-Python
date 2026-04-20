from datetime import datetime
from typing import Optional

from log_analyzer.models import LogEntry

def parse_line(line: str, source_file: str) -> Optinal[LogEntry]:
    """
    Parse one log line into a LogEntry.
    Return None if the line is invalid.
    """
    raw = line.strip()
    if not raw:
        return None
    
    parts = raw.split(" | ")

    if len(parts) != 5:
        return None
    
    timestamp_str, level, service, event_code, message = parts

    try:
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None
    
    return LogEntry(
        timestamp=timestamp,
        level=level.strip(),
        service=service.strip(),
        event_code=event_code.strip(),
        message=message.strip(),
        source_file=source_file,
    )