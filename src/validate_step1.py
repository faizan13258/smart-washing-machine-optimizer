import pandas as pd
import sys

REQUIRED_COLUMNS = [
    "scenario_id",
    "dirt_level",
    "load_kg",
    "fabric_type",
    "water_availability"
]

FABRICS = {"Cotton", "Synthetic", "Delicate", "Wool"}
WATER_LEVELS = {"Low", "Medium", "High"}

def validate_csv(file_path):
    errors = []

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"FAIL: Unable to read CSV: {e}")
        return False

    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        errors.append(f"Missing columns: {sorted(missing_columns)}")
        print("FAIL")
        for error in errors:
            print("-", error)
        return False

    df = df[REQUIRED_COLUMNS]

    if df.empty:
        errors.append("CSV contains no records")

    if df.isnull().any().any():
        errors.append("Missing values found")

    if df["scenario_id"].duplicated().any():
        errors.append("Duplicate scenario IDs found")

    dirt = pd.to_numeric(df["dirt_level"], errors="coerce")
    load = pd.to_numeric(df["load_kg"], errors="coerce")

    if dirt.isnull().any() or not dirt.between(0, 100).all():
        errors.append("Dirt level must be between 0 and 100")

    if load.isnull().any() or not load.between(0.1, 10.0).all():
        errors.append("Laundry load must be between 0.1 and 10 kg")

    if not df["fabric_type"].isin(FABRICS).all():
        errors.append("Unsupported fabric type found")

    if not df["water_availability"].isin(WATER_LEVELS).all():
        errors.append("Invalid water availability level found")

    if errors:
        print("FAIL")
        for error in errors:
            print("-", error)
        return False

    print(f"PASS: {len(df)} valid records")
    return True


if __name__ == "__main__":
    valid_file = "data/starter/starter_cases.csv"
    invalid_file = "data/starter/invalid_cases.csv"

    valid_result = validate_csv(valid_file)
    invalid_result = validate_csv(invalid_file)

    print("\nFINAL TEST SUMMARY")
    print("Valid CSV test:", "PASS" if valid_result else "FAIL")
    print("Invalid CSV rejection test:", "PASS" if not invalid_result else "FAIL")

    if valid_result and not invalid_result:
        print("OVERALL RESULT: PASS")
    else:
        print("OVERALL RESULT: FAIL")
        sys.exit(1)
