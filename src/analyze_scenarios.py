
import csv
from collections import Counter
from pathlib import Path
import matplotlib.pyplot as plt

INPUT_FILE = Path("data/processed/washing_scenarios.csv")
REPORT_DIR = Path("report")
RESULTS_DIR = Path("results")

REPORT_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

with INPUT_FILE.open("r", newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

if not rows:
    raise ValueError("No scenarios found in the CSV file.")

dirt_levels = [int(row["dirt_level"]) for row in rows]
loads = [float(row["load_kg"]) for row in rows]
fabrics = Counter(row["fabric_type"] for row in rows)
water_levels = Counter(row["water_availability"] for row in rows)

report = [
    "# Scenario Data Analysis",
    "",
    f"- Total scenarios: {len(rows)}",
    f"- Average dirt level: {sum(dirt_levels) / len(dirt_levels):.2f}",
    f"- Minimum dirt level: {min(dirt_levels)}",
    f"- Maximum dirt level: {max(dirt_levels)}",
    f"- Average laundry load: {sum(loads) / len(loads):.2f} kg",
    f"- Minimum laundry load: {min(loads):.2f} kg",
    f"- Maximum laundry load: {max(loads):.2f} kg",
    "",
    "## Fabric Distribution",
]

report.extend(f"- {name}: {count}" for name, count in sorted(fabrics.items()))
report.extend(["", "## Water Availability Distribution"])
report.extend(
    f"- {name}: {count}" for name, count in sorted(water_levels.items())
)

(REPORT_DIR / "scenario_analysis.md").write_text(
    "\n".join(report) + "\n", encoding="utf-8"
)

plt.figure(figsize=(8, 5))
plt.hist(dirt_levels, bins=20, edgecolor="black")
plt.title("Distribution of Dirt Levels")
plt.xlabel("Dirt Level")
plt.ylabel("Number of Scenarios")
plt.tight_layout()
plt.savefig(RESULTS_DIR / "dirt_level_distribution.png")
plt.close()

plt.figure(figsize=(8, 5))
plt.bar(sorted(fabrics.keys()), [fabrics[k] for k in sorted(fabrics)])
plt.title("Fabric Type Distribution")
plt.xlabel("Fabric Type")
plt.ylabel("Number of Scenarios")
plt.tight_layout()
plt.savefig(RESULTS_DIR / "fabric_distribution.png")
plt.close()

print(f"Scenarios analyzed: {len(rows)}")
print(f"Analysis report: {REPORT_DIR / 'scenario_analysis.md'}")
print(f"Charts saved in: {RESULTS_DIR}")
