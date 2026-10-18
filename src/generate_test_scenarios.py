
"""Generate reproducible washing-machine test scenarios."""

import random
import csv
from pathlib import Path

SEED = 42
NUMBER_OF_SCENARIOS = 10_000

FABRIC_TYPES = ["Cotton", "Synthetic", "Delicate", "Wool"]
WATER_LEVELS = ["Low", "Medium", "High"]


def generate_scenarios(count=NUMBER_OF_SCENARIOS, seed=SEED):
    """Generate valid simulated scenarios reproducibly."""
    rng = random.Random(seed)
    scenarios = []

    for scenario_id in range(1, count + 1):
        scenarios.append({
            "scenario_id": scenario_id,
            "dirt_level": rng.randint(0, 100),
            "load_kg": round(rng.uniform(0.1, 10.0), 2),
            "fabric_type": rng.choice(FABRIC_TYPES),
            "water_availability": rng.choice(WATER_LEVELS),
        })

    return scenarios


def validate_scenario(scenario):
    """Return True when the scenario has valid input values."""
    return (
        isinstance(scenario["dirt_level"], int)
        and 0 <= scenario["dirt_level"] <= 100
        and isinstance(scenario["load_kg"], (int, float))
        and 0.1 <= scenario["load_kg"] <= 10.0
        and scenario["fabric_type"] in FABRIC_TYPES
        and scenario["water_availability"] in WATER_LEVELS
    )


def save_scenarios(scenarios, output_path):
    """Validate scenarios and save them to a CSV file."""
    valid_scenarios = [
        scenario for scenario in scenarios
        if validate_scenario(scenario)
    ]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not valid_scenarios:
        raise ValueError("No valid scenarios to save.")

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=valid_scenarios[0].keys()
        )
        writer.writeheader()
        writer.writerows(valid_scenarios)

    return len(valid_scenarios)


if __name__ == "__main__":
    data = generate_scenarios()
    output_file = Path("data/processed/washing_scenarios.csv")
    saved_count = save_scenarios(data, output_file)

    print(f"Generated scenarios: {len(data)}")
    print(f"Valid scenarios saved: {saved_count}")
    print(f"Output file: {output_file}")
