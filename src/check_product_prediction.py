from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.product_predict import predict_one

sample_input = {
    "dirt_level": 100,
    "load_kg": 6,
    "fabric_type": "Synthetic",
    "water_availability": "Medium"
}

result = predict_one(sample_input)

output = {
    **result["inputs"],
    **result["predictions"]
}

df = pd.DataFrame([output])

report_dir = ROOT / "data" / "reports"
report_dir.mkdir(parents=True, exist_ok=True)

output_path = report_dir / "step5_script_prediction.csv"
df.to_csv(output_path, index=False)

print("Inference consistency reference generated.")
print(df.to_string(index=False))
print("\nSaved:", output_path)
