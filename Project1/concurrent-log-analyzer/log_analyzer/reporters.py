import csv
import json
from pathlib import Path

def write_json_report(result: dict, output_path: str) -> None:
    """
    Writer the analysis result to a JSON file
    """
    path = Path(output_path)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def write_csv_report(result: dict, output_path: str) -> None:
    """
    Writer the top error codes section to a CSV file.
    """
    path = Path(output_path)

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["event_code", "count"])

        for event_code, count in result["top_error_codes"]:
            writer.writerow([event_code, count])