from log_analyzer.parser import parse_line

def test_parse_line_valid():
    line = "2026-04-20 10:15:05 | ERROR | payment-service | PAYMENT_TIMEOUT | order=999 timeout=30s"

    entry = parse_line(line, source_file="app1.log")

    assert entry is not None
    assert entry.level == "ERROR"
    assert entry.service == "payment-service"
    assert entry.event_code == "PAYMENT_TIMEOUT"
    assert entry.message == "order=999 timeout=30s"
    assert entry.source_file == "app1.log"
    assert entry.timestamp.year == 2026
    assert entry.timestamp.month == 4
    assert entry.timestamp.day == 20

def test_parse_line_empty_returns_none():
    entry = parse_line("", source_file="app1.log")
    assert entry is None

def test_parse_line_invalid_format_returns_none():
    line = "this is not a valid log line"
    entry = parse_line(line, source_file="app1.log")
    assert entry is None 

def test_parse_line_invalid_timestamp_returns_none():
    line = "bad-time | INFO | auth-service | USER_LOGIN_SUCCESS | user=123"
    entry = parse_line(line, source_file="app1.log")
    assert entry is None