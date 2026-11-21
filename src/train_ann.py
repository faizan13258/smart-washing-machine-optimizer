from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"
RESULTS_DIR = ROOT / "results"
REPORT_DIR = ROOT / "report"
MODEL_DIR = ROOT / "models"

for folder in [DATA_DIR, RESULTS_DIR, REPORT_DIR, MODEL_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42

# 1. Load and validate input dataset
input_path = DATA_DIR / "washing_scenarios.csv"
df = pd.read_csv(input_path)

required_columns = [
    "scenario_id", "dirt_level", "load_kg",
    "fabric_type", "water_availability"
]

if not all(col in df.columns for col in required_columns):
    raise ValueError("Input dataset is missing required columns.")

if df[required_columns].isnull().any().any():
    raise ValueError("Input dataset contains missing values.")

if df["scenario_id"].duplicated().any():
    raise ValueError("Duplicate scenario IDs found.")

# 2. Generate transparent simulated target outputs
# These are rule-generated demonstration labels, NOT real machine measurements.

fabric_time = {
    "Cotton": 5, "Synthetic": 2, "Delicate": 0, "Wool": 4
}
fabric_water = {
    "Cotton": 3, "Synthetic": 1, "Delicate": 0, "Wool": 1
}
fabric_detergent = {
    "Cotton": 3, "Synthetic": 1, "Delicate": 0, "Wool": 1
}
fabric_spin = {
    "Cotton": 1000, "Synthetic": 900, "Delicate": 700, "Wool": 600
}
water_penalty = {"Low": 8, "Medium": 3, "High": 0}

if not set(df["fabric_type"]).issubset(fabric_time):
    raise ValueError("Unknown fabric type found.")

if not set(df["water_availability"]).issubset(water_penalty):
    raise ValueError("Unknown water availability value found.")

dirt = df["dirt_level"].astype(float)
load = df["load_kg"].astype(float)

df["wash_time_min"] = (
    25 + 0.55 * dirt + 3.2 * load
    + df["fabric_type"].map(fabric_time)
    + df["water_availability"].map(water_penalty)
).round(2)

df["water_consumption_l"] = (
    22 + 9 * load + 0.08 * dirt
    + df["fabric_type"].map(fabric_water)
).round(2)

df["detergent_ml"] = (
    15 + 0.42 * dirt + 4.5 * load
    + df["fabric_type"].map(fabric_detergent)
).round(2)

df["spin_speed_rpm"] = (
    df["fabric_type"].map(fabric_spin)
    - 12 * load + 0.5 * dirt
).clip(lower=400, upper=1200).round(0)

df.to_csv(DATA_DIR / "ann_training_dataset.csv", index=False)

# 3. Prepare input and output variables
feature_columns = [
    "dirt_level", "load_kg", "fabric_type", "water_availability"
]
target_columns = [
    "wash_time_min", "water_consumption_l",
    "detergent_ml", "spin_speed_rpm"
]

X = df[feature_columns]
y = df[target_columns]

# 70% training, 15% validation, 15% testing
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, random_state=RANDOM_STATE
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=RANDOM_STATE
)

# 4. Preprocess numerical and categorical inputs
numeric_features = ["dirt_level", "load_kg"]
categorical_features = ["fabric_type", "water_availability"]

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", StandardScaler(), numeric_features),
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

X_train_processed = preprocessor.fit_transform(X_train)
X_val_processed = preprocessor.transform(X_val)
X_test_processed = preprocessor.transform(X_test)

# Scale multiple target outputs
target_scaler = StandardScaler()
y_train_scaled = target_scaler.fit_transform(y_train)
y_val_scaled = target_scaler.transform(y_val)

# 5. Build and train Artificial Neural Network
ann = MLPRegressor(
    hidden_layer_sizes=(64, 32),
    activation="relu",
    solver="adam",
    learning_rate_init=0.001,
    alpha=0.0001,
    batch_size=64,
    max_iter=1200,
    early_stopping=True,
    validation_fraction=0.15,
    n_iter_no_change=30,
    random_state=RANDOM_STATE
)

ann.fit(X_train_processed, y_train_scaled)

# 6. Generate validation and test predictions
val_predictions = target_scaler.inverse_transform(
    ann.predict(X_val_processed)
)
test_predictions = target_scaler.inverse_transform(
    ann.predict(X_test_processed)
)

# 7. Calculate regression metrics
def calculate_metrics(actual, predicted, split_name):
    rows = []
    for index, target in enumerate(target_columns):
        actual_values = actual.iloc[:, index].to_numpy()
        predicted_values = predicted[:, index]

        rows.append({
            "dataset": split_name,
            "target": target,
            "MAE": mean_absolute_error(actual_values, predicted_values),
            "RMSE": np.sqrt(mean_squared_error(actual_values, predicted_values)),
            "R2": r2_score(actual_values, predicted_values)
        })
    return rows

metrics = (
    calculate_metrics(y_val, val_predictions, "Validation")
    + calculate_metrics(y_test, test_predictions, "Test")
)

metrics_df = pd.DataFrame(metrics)
metrics_df.to_csv(RESULTS_DIR / "ann_metrics.csv", index=False)

with open(REPORT_DIR / "ann_metrics.json", "w") as file:
    json.dump(metrics, file, indent=4)

# 8. Save prediction results
def save_predictions(X_part, y_actual, predictions, filename):
    output = X_part.reset_index(drop=True).copy()
    output.insert(0, "scenario_id", df.loc[X_part.index, "scenario_id"].to_numpy())
    actual_reset = y_actual.reset_index(drop=True)

    for i, target in enumerate(target_columns):
        output[f"actual_{target}"] = actual_reset[target]
        output[f"predicted_{target}"] = predictions[:, i]

    output.to_csv(RESULTS_DIR / filename, index=False)

save_predictions(
    X_val, y_val, val_predictions, "ann_validation_predictions.csv"
)
save_predictions(
    X_test, y_test, test_predictions, "ann_test_predictions.csv"
)

# 9. Plot ANN training loss curve
plt.figure(figsize=(9, 5))
plt.plot(ann.loss_curve_)
plt.title("ANN Training Loss Curve")
plt.xlabel("Training Iterations")
plt.ylabel("Loss")
plt.grid(True)
plt.tight_layout()
plt.savefig(RESULTS_DIR / "ann_loss_curve.png", dpi=300)
plt.close()

# 10. Plot actual vs predicted values for each output
for i, target in enumerate(target_columns):
    actual = y_test.iloc[:, i].to_numpy()
    predicted = test_predictions[:, i]

    plt.figure(figsize=(7, 6))
    plt.scatter(actual, predicted, alpha=0.5)
    low = min(actual.min(), predicted.min())
    high = max(actual.max(), predicted.max())
    plt.plot([low, high], [low, high], linestyle="--")
    plt.title(f"Actual vs Predicted: {target}")
    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / f"ann_{target}_prediction.png", dpi=300)
    plt.close()

# 11. Save trained model and preprocessing components
joblib.dump(
    {
        "preprocessor": preprocessor,
        "target_scaler": target_scaler,
        "ann_model": ann,
        "feature_columns": feature_columns,
        "target_columns": target_columns
    },
    MODEL_DIR / "washing_machine_ann.joblib"
)

metadata = {
    "model": "Multi-output Artificial Neural Network",
    "library": "scikit-learn MLPRegressor",
    "architecture": [64, 32],
    "activation": "relu",
    "optimizer": "adam",
    "random_state": RANDOM_STATE,
    "training_rows": len(X_train),
    "validation_rows": len(X_val),
    "test_rows": len(X_test),
    "input_features": feature_columns,
    "output_targets": target_columns,
    "target_data_note": (
        "Targets are simulated using documented deterministic rules. "
        "They are not real washing-machine measurements."
    )
}

with open(MODEL_DIR / "ann_metadata.json", "w") as file:
    json.dump(metadata, file, indent=4)

print("\n========== ANN TRAINING COMPLETED ==========")
print("Dataset rows:", len(df))
print("Training rows:", len(X_train))
print("Validation rows:", len(X_val))
print("Testing rows:", len(X_test))
print("\nANN iterations:", ann.n_iter_)
print("\nMETRICS:")
print(metrics_df.to_string(index=False))
print("\nGenerated files:")
print("- data/processed/ann_training_dataset.csv")
print("- results/ann_metrics.csv")
print("- results/ann_validation_predictions.csv")
print("- results/ann_test_predictions.csv")
print("- results/ann_loss_curve.png")
print("- results/ann_*_prediction.png")
print("- models/washing_machine_ann.joblib")
print("- models/ann_metadata.json")
print("- report/ann_metrics.json")
