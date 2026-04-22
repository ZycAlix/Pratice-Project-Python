from pathlib import Path

from log_analyzer.concurrency import analyze_files_concurrently


def test_analyze_files_concurrently(tmp_path):
    file1 = tmp_path / "app1.log"
    file2 = tmp_path / "app2.log"

    file1.write_text(
        "\n".join(
            [
                "2026-04-20 10:15:03 | INFO | auth-service | USER_LOGIN_SUCCESS | user=123",
                "2026-04-20 10:15:05 | ERROR | payment-service | PAYMENT_TIMEOUT | order=999 timeout=30s",
            ]
        ),
        encoding="utf-8",
    )

    file2.write_text(
        "\n".join(
            [
                "2026-04-20 11:00:01 | INFO | user-service | USER_CREATED | user=888",
                "2026-04-20 11:00:02 | ERROR | order-service | DB_CONNECTION_FAIL | db=orders",
            ]
        ),
        encoding="utf-8",
    )

    result = analyze_files_concurrently([file1, file2], max_workers=2)

    assert result["total_lines"] == 4
    assert result["levels"]["INFO"] == 2
    assert result["levels"]["ERROR"] == 2
    assert result["services"]["auth-service"] == 1
    assert result["services"]["payment-service"] == 1
    assert result["services"]["user-service"] == 1
    assert result["services"]["order-service"] == 1
    assert ("PAYMENT_TIMEOUT", 1) in result["top_error_codes"]
    assert ("DB_CONNECTION_FAIL", 1) in result["top_error_codes"]