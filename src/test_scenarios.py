"""Test normal, boundary, stress, and invalid washing scenarios."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prepare_data import validate_data

import pandas as pd


def make_scenario(scenario_id, dirt, load, fabric="Cotton", water="Medium"):
    return {
        "scenario_id": scenario_id,
        "dirt_level": dirt,
        "load_kg": load,
        "fabric_type": fabric,
        "water_availability": water,
    }


def main():
    # Normal and boundary inputs should pass validation.
    valid_cases = [
        make_scenario(1, 50, 5.0),
        make_scenario(2, 0, 0.1, "Delicate", "Low"),
        make_scenario(3, 100, 10.0, "Wool", "High"),
    ]

    for case in valid_cases:
        errors = validate_data(pd.DataFrame([case]))
        assert not errors, f"Valid case rejected: {case} -> {errors}"

    # Invalid inputs should be rejected.
    invalid_cases = [
        make_scenario(4, -1, 5.0),
        make_scenario(5, 101, 5.0),
        make_scenario(6, 50, 0.0),
        make_scenario(7, 50, 11.0),
        make_scenario(8, 50, 5.0, "UnknownFabric"),
        make_scenario(9, 50, 5.0, "Cotton", "UnknownWater"),
    ]

    for case in invalid_cases:
        errors = validate_data(pd.DataFrame([case]))
        assert errors, f"Invalid case incorrectly accepted: {case}"

    # Stress check: validate 1,000 valid scenarios together.
    stress = pd.DataFrame([
        make_scenario(i, i % 101, 0.1 + (i % 100) / 10)
        for i in range(1000, 2000)
    ])
    errors = validate_data(stress)
    assert not errors, f"Stress batch failed: {errors}"

    print("Normal cases: PASS (1)")
    print("Boundary cases: PASS (2)")
    print("Invalid cases rejected: PASS (6)")
    print("Stress batch: PASS (1000 scenarios)")


if __name__ == "__main__":
    main()
