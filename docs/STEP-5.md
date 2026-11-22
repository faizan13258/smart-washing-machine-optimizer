
# Step 5 - Product V1

## Team and project
- Team name: Individual project
- Project code and title: Smart Washing Machine Decision & Resource Optimizer
- Branch: `step-5-product-v1`
- Commit: Pending final commit

## User task

The interface is designed for a user who wants to estimate suitable washing-cycle settings by entering laundry details.

The user provides:
- Dirt level (0–100)
- Laundry load (0.1–10 kg)
- Fabric type (Cotton, Synthetic, Delicate, Wool)
- Water availability (Low, Medium, High)

The application predicts:
- Wash time (minutes)
- Water consumption (litres)
- Detergent quantity (ml)
- Spin speed (RPM)

These predictions support an educational washing-cycle decision demonstration.

## Interface and method

- Interface type: Streamlit web application
- Entry file: `app/step5_app.py`
- Inference module: `src/product_predict.py`
- Saved ANN model: `models/washing_machine_ann.joblib`
- Model approach: Saved multi-output Artificial Neural Network (ANN)
- Input validation: Numeric ranges, required fields and allowed categories are checked before prediction.
- Output: Four predicted washing settings with their units.
- Download: Prediction can be downloaded as a CSV file.

Data flow:

`User input -> Input validation -> Saved preprocessing pipeline -> Saved ANN model -> Inverse target scaling -> Prediction display -> CSV download`

The application loads the saved model. It does not retrain the model during normal prediction.

## Run instructions

- Python version: 3.14.3
- Interface framework: Streamlit 1.67.0
- Working directory: Project repository root

Install dependencies:

```powershell
python -m pip install pandas joblib scikit-learn streamlit
```

Start the application:

```powershell
python -m streamlit run app/step5_app.py
```

Expected local address:

`http://localhost:8501`

The demonstration is currently a local Streamlit application. No hosted deployment is claimed.

## Actual test evidence

Five automated tests were executed using:

```powershell
python -m unittest test_product_predict -v
```

Observed result: All five tests passed.

| Case | Actual input or evidence | Expected behaviour | Observed behaviour | Result |
|---|---|---|---|---|
| Normal prediction | Dirt 70, load 5 kg, Cotton, Medium | Four finite predictions | Prediction generated | PASS |
| Boundary values | Dirt 0 and 100; load 0.1 and 10 kg | Boundary inputs accepted | Predictions generated | PASS |
| Invalid numeric values | Dirt 101 and load -1 | ValueError | Invalid values rejected | PASS |
| Invalid categories | Unsupported fabric and water categories | ValueError | Invalid categories rejected | PASS |
| Missing input | Required field omitted | ValueError | Missing field rejected | PASS |
| Missing model | Temporary unavailable model path | FileNotFoundError and UI error | Error displayed in inference test and Streamlit UI | PASS |
| UI and inference consistency | Dirt 100, load 6 kg, Synthetic, Medium | Matching output | Exact CSV match; maximum numeric difference 0.0 | PASS |

The five automated tests and the additional missing-model and consistency checks are reported separately.

## Screenshots and evidence

Actual screenshots are stored in `docs/evidence/step5/`.

1. `01_input_form.png` - Input form.
2. `02_successful_prediction.png` - Successful prediction.
3. `03_validation_error.png` - Missing-model error displayed in the Streamlit interface.

Prediction consistency files:

- `data/reports/step5_script_prediction.csv`
- `data/reports/step5_ui_prediction.csv`

Both CSV files contain one row and eight columns. Their values match exactly for the same input.

## Earlier feedback addressed

- Step 2 data preparation and validation were retained.
- Step 3 saved ANN model and preprocessing pipeline were reused.
- Step 4 baseline comparison artifacts were preserved.
- Step 5 inference logic was separated from the Streamlit interface.
- Input validation, error handling and CSV export were implemented.
- The original Step 3 and Step 4 evidence was not intentionally overwritten.

No separate written instructor feedback item is claimed as resolved without its supporting record.

## Limitations and responsible use

- Training targets are simulated and are not measurements from a physical washing machine.
- Predictions are educational estimates, not guaranteed real-world washing settings.
- The application has not been validated using physical washing-machine experiments.
- Actual water consumption, detergent requirements and wash time may vary by machine, detergent, fabric condition and operating environment.
- The application should not be treated as a certified appliance controller.
- Model performance on simulated test data does not establish real-world accuracy.

## Team contributions

This is an individual project.

The student completed the Step 5 inference module, Streamlit interface, input validation, CSV export, automated tests, consistency checks, error-handling checks and project documentation.
