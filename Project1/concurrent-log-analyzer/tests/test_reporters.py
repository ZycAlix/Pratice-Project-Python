import csv
import json

from log_analyzer.reporters import write_csv_report, write_json_report


def sample_result():
    return {
        "total_lines": 10,
        "levels": {"INFO": 4, "ERROR": 3, "WARN": 2},
        "services": {
            "auth-service": 3,
            "payment-service": 3,
            "order-service": 2,
            "user-service": 2,
        },
        "top_error_codes": [
            ("PAYMENT_TIMEOUT", 3),
            ("DB_CONNECTION_FAIL", 1),
        ],
    }


def test_write_json_report(tmp_path):
    output_file = tmp_path / "report.json"

    write_json_report(sample_result(), str(output_file))

    assert output_file.exists()

    data = json.loads(output_file.read_text(encoding="utf-8"))
    assert data["total_lines"] == 10
    assert data["levels"]["ERROR"] == 3


def test_write_csv_report(tmp_path):
    output_file = tmp_path / "report.csv"

    write_csv_report(sample_result(), str(output_file))

    assert output_file.exists()

    with open(output_file, "r", encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))

    assert rows[0] == ["event_code", "count"]
    assert rows[1] == ["PAYMENT_TIMEOUT", "3"]
    assert rows[2] == ["DB_CONNECTION_FAIL", "1"]