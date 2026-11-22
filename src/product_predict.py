from pathlib import Path
import math
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "washing_machine_ann.joblib"

INPUT_FEATURES = [
    "dirt_level",
    "load_kg",
    "fabric_type",
    "water_availability"
]

OUTPUT_TARGETS = [
    "wash_time_min",
    "water_consumption_l",
    "detergent_ml",
    "spin_speed_rpm"
]

ALLOWED_FABRICS = ["Cotton", "Synthetic", "Delicate", "Wool"]
ALLOWED_WATER = ["Low", "Medium", "High"]


def validate_input(inputs):
    if not isinstance(inputs, dict):
        raise ValueError("Input must be provided as a dictionary.")

    missing = [key for key in INPUT_FEATURES if key not in inputs]
    if missing:
        raise ValueError(f"Missing required inputs: {', '.join(missing)}")

    try:
        dirt = float(inputs["dirt_level"])
        load = float(inputs["load_kg"])
    except (TypeError, ValueError):
        raise ValueError("Dirt level and load must be numeric values.")

    if not math.isfinite(dirt) or not 0 <= dirt <= 100:
        raise ValueError("Dirt level must be between 0 and 100.")

    if not math.isfinite(load) or not 0.1 <= load <= 10:
        raise ValueError("Load must be between 0.1 and 10 kg.")

    if inputs["fabric_type"] not in ALLOWED_FABRICS:
        raise ValueError(f"Fabric type must be one of: {ALLOWED_FABRICS}")

    if inputs["water_availability"] not in ALLOWED_WATER:
        raise ValueError(f"Water availability must be one of: {ALLOWED_WATER}")

    return {
        "dirt_level": dirt,
        "load_kg": load,
        "fabric_type": inputs["fabric_type"],
        "water_availability": inputs["water_availability"]
    }


def load_model_bundle():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Saved ANN model not found: {MODEL_PATH}"
        )

    bundle = joblib.load(MODEL_PATH)

    required = [
        "preprocessor",
        "target_scaler",
        "ann_model",
        "feature_columns",
        "target_columns"
    ]

    missing = [key for key in required if key not in bundle]
    if missing:
        raise ValueError(f"Model bundle is incomplete: {missing}")

    return bundle


def predict_one(inputs):
    clean_inputs = validate_input(inputs)
    bundle = load_model_bundle()

    if bundle["feature_columns"] != INPUT_FEATURES:
        raise ValueError("Model input feature order does not match.")

    if bundle["target_columns"] != OUTPUT_TARGETS:
        raise ValueError("Model output target order does not match.")

    input_df = pd.DataFrame([clean_inputs], columns=INPUT_FEATURES)

    processed = bundle["preprocessor"].transform(input_df)
    scaled_prediction = bundle["ann_model"].predict(processed)
    prediction = bundle["target_scaler"].inverse_transform(
        scaled_prediction
    )[0]

    result = {
        target: float(value)
        for target, value in zip(OUTPUT_TARGETS, prediction)
    }

    if not all(math.isfinite(value) for value in result.values()):
        raise ValueError("Model generated a non-finite prediction.")

    return {
        "inputs": clean_inputs,
        "predictions": result
    }
