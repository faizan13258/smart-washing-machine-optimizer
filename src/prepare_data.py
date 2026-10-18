"""Reusable loading, validation, and preparation for washing scenarios."""

from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = [
    "scenario_id",
    "dirt_level",
    "load_kg",
    "fabric_type",
    "water_availability",
]

VALID_FABRICS = {"Cotton", "Synthetic", "Delicate", "Wool"}
VALID_WATER_LEVELS = {"Low", "Medium", "High"}


def load_data(path="data/processed/washing_scenarios.csv"):
    """Load the prepared washing-machine scenario CSV."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")
    return pd.read_csv(file_path)


def validate_data(df):
    """Return a list of data-quality errors."""
    errors = []

    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_columns:
        return [f"Missing columns: {sorted(missing_columns)}"]

    if df[REQUIRED_COLUMNS].isnull().any().any():
        errors.append("Missing values found.")

    if df["scenario_id"].duplicated().any():
        errors.append("Duplicate scenario IDs found.")

    if not df["dirt_level"].between(0, 100).all():
        errors.append("Dirt level must be between 0 and 100.")

    if not df["load_kg"].between(0.1, 10.0).all():
        errors.append("Load must be between 0.1 and 10.0 kg.")

    if not df["fabric_type"].isin(VALID_FABRICS).all():
        errors.append("Invalid fabric type found.")

    if not df["water_availability"].isin(VALID_WATER_LEVELS).all():
        errors.append("Invalid water availability value found.")

    return errors


def prepare_data(path="data/processed/washing_scenarios.csv"):
    """Load and validate data, then return a usable DataFrame."""
    df = load_data(path)
    errors = validate_data(df)

    if errors:
        raise ValueError("Data validation failed: " + "; ".join(errors))

    return df.copy()


if __name__ == "__main__":
    data = prepare_data()
    print(f"Prepared scenarios: {len(data)}")
    print("Validation: PASS")
