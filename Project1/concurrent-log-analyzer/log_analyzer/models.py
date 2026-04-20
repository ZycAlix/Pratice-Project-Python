from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogEntry:
    timestamp: datetime
    level: str
    service: str
    event_code: str
    message: str
    source_file: str
    