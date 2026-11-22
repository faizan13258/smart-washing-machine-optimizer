
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# --------------------------------------------------
# 1. PROJECT PATHS AND CONFIGURATION
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data" / "processed"
RESULTS_DIR = ROOT / "results"
REPORT_DIR = ROOT / "report"

SOURCE_FILE = DATA_DIR / "ann_training_dataset.csv"
VALIDATION_FILE = RESULTS_DIR / "ann_validation_predictions.csv"
TEST_FILE = RESULTS_DIR / "ann_test_predictions.csv"

FEATURES = [
    "dirt_level",
    "load_kg",
    "fabric_type",
    "water_availability"
]

TARGETS = [
    "wash_time_min",
    "water_consumption_l",
    "detergent_ml",
    "spin_speed_rpm"
]

RANDOM_STATE = 42

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. LOAD AND VALIDATE DATA
# --------------------------------------------------

source = pd.read_csv(SOURCE_FILE)

required_source = ["scenario_id"] + FEATURES + TARGETS

if not set(required_source).issubset(source.columns):
    raise ValueError("Source dataset is missing required columns.")

if source[required_source].isnull().any().any():
    raise ValueError("Source dataset contains missing values.")

if source["scenario_id"].duplicated().any():
    raise ValueError("Duplicate scenario IDs in source dataset.")

if len(source) != 10000:
    raise ValueError("Expected exactly 10,000 source scenarios.")


# --------------------------------------------------
# 3. RECREATE THE ORIGINAL STEP 3 DATA SPLIT
# --------------------------------------------------

train_idx, temp_idx = train_test_split(
    source.index,
    test_size=0.30,
    random_state=RANDOM_STATE
)

val_idx, test_idx = train_test_split(
    temp_idx,
    test_size=0.50,
    random_state=RANDOM_STATE
)

train_data = source.loc[train_idx].copy()

expected_validation_ids = (
    source.loc[val_idx, "scenario_id"].tolist()
)

expected_test_ids = (
    source.loc[test_idx, "scenario_id"].tolist()
)

print("Training rows:", len(train_data))
print("Validation rows:", len(expected_validation_ids))
print("Test rows:", len(expected_test_ids))


# --------------------------------------------------
# 4. DEFINE FIXED WASH-CYCLE CATEGORIES
# --------------------------------------------------

def dirt_category(value):
    if value <= 33:
        return "Light"
    elif value <= 66:
        return "Normal"
    return "Heavy"


def load_category(value):
    if value <= 3:
        return "Small"
    elif value <= 7:
        return "Medium"
    return "Large"


def add_cycle_categories(data):
    data = data.copy()

    data["dirt_band"] = data["dirt_level"].apply(
        dirt_category
    )

    data["load_band"] = data["load_kg"].apply(
        load_category
    )

    return data


train_data = add_cycle_categories(train_data)


# --------------------------------------------------
# 5. BUILD LOOKUP TABLE USING TRAINING DATA ONLY
# --------------------------------------------------

lookup_levels = [
    [
        "fabric_type",
        "dirt_band",
        "load_band",
        "water_availability"
    ],
    [
        "fabric_type",
        "dirt_band",
        "load_band"
    ],
    [
        "fabric_type",
        "dirt_band"
    ],
    [
        "fabric_type"
    ],
    []
]

lookup_maps = []

for columns in lookup_levels:

    if columns:
        grouped = (
            train_data
            .groupby(columns, observed=True)[TARGETS]
            .median()
            .reset_index()
        )

        mapping = {}

        for _, row in grouped.iterrows():
            key = tuple(row[column] for column in columns)
            mapping[key] = row[TARGETS].to_numpy(dtype=float)

    else:
        mapping = {
            (): train_data[TARGETS].median().to_numpy(dtype=float)
        }

    lookup_maps.append(mapping)


# Save the detailed fixed-cycle lookup table
full_lookup = (
    train_data
    .groupby(
        lookup_levels[0],
        observed=True
    )[TARGETS]
    .median()
    .reset_index()
)

full_lookup.to_csv(
    REPORT_DIR / "step4_fixed_cycle_lookup.csv",
    index=False
)


# --------------------------------------------------
# 6. GENERATE FIXED LOOKUP PREDICTIONS
# --------------------------------------------------

def predict_with_lookup(data):

    categorized = add_cycle_categories(data)

    predictions = []
    fallback_levels = []

    for _, row in categorized.iterrows():

        prediction = None
        selected_level = None

        for level_index, columns in enumerate(lookup_levels):

            if columns:
                key = tuple(row[column] for column in columns)
            else:
                key = ()

            if key in lookup_maps[level_index]:
                prediction = lookup_maps[level_index][key]
                selected_level = level_index
                break

        if prediction is None:
            raise ValueError("No baseline lookup value found.")

        predictions.append(prediction)
        fallback_levels.append(selected_level)

    prediction_array = np.array(predictions)

    return prediction_array, fallback_levels


# --------------------------------------------------
# 7. VERIFY ANN PREDICTIONS AGAINST SOURCE DATA
# --------------------------------------------------

def verify_prediction_file(file_path, expected_ids):

    predictions = pd.read_csv(file_path)

    required_columns = (
        ["scenario_id"]
        + FEATURES
        + [f"actual_{target}" for target in TARGETS]
        + [f"predicted_{target}" for target in TARGETS]
    )

    if not set(required_columns).issubset(predictions.columns):
        raise ValueError(
            f"Missing required columns in {file_path.name}"
        )

    if predictions["scenario_id"].duplicated().any():
        raise ValueError("Duplicate IDs in prediction file.")

    if predictions["scenario_id"].tolist() != expected_ids:
        raise ValueError(
            f"Scenario ID/order mismatch in {file_path.name}"
        )

    reference = (
        source
        .set_index("scenario_id")
        .loc[predictions["scenario_id"]]
    )

    for feature in FEATURES:

        if feature in ["fabric_type", "water_availability"]:

            if not predictions[feature].astype(str).reset_index(
                drop=True
            ).equals(
                reference[feature].astype(str).reset_index(drop=True)
            ):
                raise ValueError(
                    f"Feature mismatch: {feature}"
                )

        else:

            if not np.allclose(
                predictions[feature].to_numpy(dtype=float),
                reference[feature].to_numpy(dtype=float)
            ):
                raise ValueError(
                    f"Feature mismatch: {feature}"
                )

    for target in TARGETS:

        if not np.allclose(
            predictions[f"actual_{target}"].to_numpy(dtype=float),
            reference[target].to_numpy(dtype=float)
        ):
            raise ValueError(
                f"Actual target mismatch: {target}"
            )

        if not np.isfinite(
            predictions[f"predicted_{target}"].to_numpy(dtype=float)
        ).all():
            raise ValueError(
                f"Invalid ANN predictions: {target}"
            )

    return predictions


# --------------------------------------------------
# 8. CREATE FAIR PAIRED COMPARISON
# --------------------------------------------------

def compare_split(split_name, file_path, expected_ids):

    predictions = verify_prediction_file(
        file_path,
        expected_ids
    )

    baseline_predictions, fallback_levels = (
        predict_with_lookup(predictions)
    )

    paired = predictions[
        ["scenario_id"] + FEATURES
    ].copy()

    metric_rows = []

    comparison_rows = []

    for index, target in enumerate(TARGETS):

        actual = predictions[
            f"actual_{target}"
        ].to_numpy(dtype=float)

        ann_predicted = predictions[
            f"predicted_{target}"
        ].to_numpy(dtype=float)

        baseline_predicted = baseline_predictions[:, index]

        paired[f"actual_{target}"] = actual
        paired[f"ann_predicted_{target}"] = ann_predicted
        paired[f"baseline_predicted_{target}"] = baseline_predicted

        ann_mae = mean_absolute_error(actual, ann_predicted)
        ann_rmse = np.sqrt(mean_squared_error(actual, ann_predicted))
        ann_r2 = r2_score(actual, ann_predicted)

        baseline_mae = mean_absolute_error(
            actual,
            baseline_predicted
        )

        baseline_rmse = np.sqrt(
            mean_squared_error(actual, baseline_predicted)
        )

        baseline_r2 = r2_score(
            actual,
            baseline_predicted
        )

        metric_rows.extend([
            {
                "dataset": split_name,
                "target": target,
                "model": "ANN",
                "MAE": ann_mae,
                "RMSE": ann_rmse,
                "R2": ann_r2
            },
            {
                "dataset": split_name,
                "target": target,
                "model": "Fixed Cycle Lookup",
                "MAE": baseline_mae,
                "RMSE": baseline_rmse,
                "R2": baseline_r2
            }
        ])

        comparison_rows.append({
            "dataset": split_name,
            "target": target,
            "ANN_MAE": ann_mae,
            "Baseline_MAE": baseline_mae,
            "MAE_difference_baseline_minus_ANN": (
                baseline_mae - ann_mae
            ),
            "ANN_RMSE": ann_rmse,
            "Baseline_RMSE": baseline_rmse,
            "ANN_R2": ann_r2,
            "Baseline_R2": baseline_r2
        })

    paired.to_csv(
        RESULTS_DIR / f"step4_{split_name.lower()}_paired_predictions.csv",
        index=False
    )

    fallback_counts = pd.Series(fallback_levels).value_counts().sort_index()

    print(f"\n{split_name} fallback level counts:")
    print(fallback_counts.to_string())

    return metric_rows, comparison_rows


# --------------------------------------------------
# 9. RUN VALIDATION AND TEST COMPARISONS
# --------------------------------------------------

validation_metrics, validation_comparison = compare_split(
    "Validation",
    VALIDATION_FILE,
    expected_validation_ids
)

test_metrics, test_comparison = compare_split(
    "Test",
    TEST_FILE,
    expected_test_ids
)

all_metrics = validation_metrics + test_metrics

all_comparisons = (
    validation_comparison + test_comparison
)

metrics_df = pd.DataFrame(all_metrics)

comparison_df = pd.DataFrame(all_comparisons)

metrics_df.to_csv(
    REPORT_DIR / "step4_baseline_metrics.csv",
    index=False
)

comparison_df.to_csv(
    REPORT_DIR / "step4_comparison.csv",
    index=False
)


# --------------------------------------------------
# 10. CREATE TEST MAE COMPARISON FIGURE
# --------------------------------------------------

test_results = comparison_df[
    comparison_df["dataset"] == "Test"
].copy()

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes = axes.flatten()

for index, target in enumerate(TARGETS):

    row = test_results[
        test_results["target"] == target
    ].iloc[0]

    axes[index].bar(
        ["ANN", "Fixed Cycle Lookup"],
        [row["ANN_MAE"], row["Baseline_MAE"]]
    )

    axes[index].set_title(target)
    axes[index].set_ylabel("MAE")
    axes[index].tick_params(axis="x", rotation=12)
    axes[index].grid(axis="y", alpha=0.3)

fig.suptitle(
    "Step 4: ANN vs Fixed Wash-Cycle Lookup (Test MAE)"
)

plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "step4_baseline_vs_ann.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# --------------------------------------------------
# 11. FINAL SUMMARY
# --------------------------------------------------

print("\n========== STEP 4 COMPARISON COMPLETED ==========")

print("\nMETRICS:")
print(metrics_df.to_string(index=False))

print("\nCOMPARISON:")
print(comparison_df.to_string(index=False))

print("\nGenerated files:")
print("- report/step4_fixed_cycle_lookup.csv")
print("- report/step4_baseline_metrics.csv")
print("- report/step4_comparison.csv")
print("- results/step4_validation_paired_predictions.csv")
print("- results/step4_test_paired_predictions.csv")
print("- results/step4_baseline_vs_ann.png")

print("\nAll scenario alignment checks: PASS")
print("Baseline lookup built using training data only.")
