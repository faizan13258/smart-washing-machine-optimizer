
"""Validate generated washing-machine scenarios."""

import csv
from pathlib import Path

INPUT_FILE = Path("data/processed/washing_scenarios.csv")
REPORT_FILE = Path("report/data_quality_report.md")

REQUIRED_COLUMNS = {
    "scenario_id",
    "dirt_level",
    "load_kg",
    "fabric_type",
    "water_availability",
}

VALID_FABRICS = {"Cotton", "Synthetic", "Delicate", "Wool"}
VALID_WATER_LEVELS = {"Low", "Medium", "High"}


def validate_scenarios():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"CSV file not found: {INPUT_FILE}")

    with INPUT_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file is empty or has no header.")

        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing_columns:
            raise ValueError(f"Missing columns: {sorted(missing_columns)}")

        rows = list(reader)

    errors = []
    seen_ids = set()

    for line_number, row in enumerate(rows, start=2):
        try:
            scenario_id = int(row["scenario_id"])
            dirt = int(row["dirt_level"])
            load = float(row["load_kg"])

            if scenario_id in seen_ids:
                errors.append(f"Line {line_number}: duplicate scenario ID")
            seen_ids.add(scenario_id)

            if not 0 <= dirt <= 100:
                errors.append(f"Line {line_number}: dirt level out of range")

            if not 0.1 <= load <= 10:
                errors.append(f"Line {line_number}: load out of range")

            if row["fabric_type"] not in VALID_FABRICS:
                errors.append(f"Line {line_number}: invalid fabric type")

            if row["water_availability"] not in VALID_WATER_LEVELS:
                errors.append(f"Line {line_number}: invalid water level")

            if any(value is None or value.strip() == "" for value in row.values()):
                errors.append(f"Line {line_number}: missing value")

        except (ValueError, TypeError, KeyError):
            errors.append(f"Line {line_number}: invalid or missing field")

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    report = [
        "# Data Quality Report",
        "",
        f"- Total scenarios: {len(rows)}",
        f"- Validation errors: {len(errors)}",
        f"- Unique scenario IDs: {len(seen_ids)}",
        f"- Status: {'PASS' if not errors else 'FAIL'}",
        "",
        "## Validation Checks",
        "- Required columns are present.",
        "- Dirt level must be between 0 and 100.",
        "- Laundry load must be between 0.1 and 10 kg.",
        "- Fabric and water categories must be supported.",
        "- Scenario IDs must be unique.",
        "- Missing values are checked.",
        "",
        "## Errors",
    ]

    report.extend(
        f"- {error}" for error in errors[:100]
    ) if errors else report.append("- No validation errors found.")

    REPORT_FILE.write_text("\n".join(report) + "\n", encoding="utf-8")

    print(f"Total scenarios: {len(rows)}")
    print(f"Validation errors: {len(errors)}")
    print(f"Report saved: {REPORT_FILE}")
    print("Status:", "PASS" if not errors else "FAIL")


if __name__ == "__main__":
    validate_scenarios()
