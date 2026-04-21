from datetime import datetime

from log_analyzer.analyzer import analyze_entries
from log_analyzer.models import LogEntry


def make_entry(level: str, service: str, event_code: str, message: str = "msg") -> LogEntry:
    return LogEntry(
        timestamp=datetime(2026, 4, 20, 10, 0, 0),
        level=level,
        service=service,
        event_code=event_code,
        message=message,
        source_file="test.log",
    )


def test_analyze_entries_basic_counts():
    entries = [
        make_entry("INFO", "auth-service", "USER_LOGIN_SUCCESS"),
        make_entry("ERROR", "payment-service", "PAYMENT_TIMEOUT"),
        make_entry("ERROR", "payment-service", "PAYMENT_TIMEOUT"),
        make_entry("WARN", "auth-service", "TOKEN_EXPIRING"),
        make_entry("ERROR", "order-service", "DB_CONNECTION_FAIL"),
    ]

    result = analyze_entries(entries)

    assert result["total_lines"] == 5
    assert result["levels"]["INFO"] == 1
    assert result["levels"]["WARN"] == 1
    assert result["levels"]["ERROR"] == 3

    assert result["services"]["auth-service"] == 2
    assert result["services"]["payment-service"] == 2
    assert result["services"]["order-service"] == 1

    assert result["top_error_codes"][0] == ("PAYMENT_TIMEOUT", 2)
    assert result["top_error_codes"][1] == ("DB_CONNECTION_FAIL", 1)


def test_analyze_entries_empty():
    result = analyze_entries([])

    assert result["total_lines"] == 0
    assert result["levels"] == {}
    assert result["services"] == {}
    assert result["top_error_codes"] == []