# Step 6 - Testing and validation

## Project and environment

- Project: Smart Washing Machine Decision & Resource Optimizer
- Tested branch: `step-6-testing`
- Base commit tested: `bf2d6d1`
- Python: 3.14.3
- Streamlit: 1.67.0
- Scikit-learn: 1.9.1
- Joblib: 1.6.0
- Pandas: 3.0.6
- NumPy: 2.5.4
- Application: `app/step5_app.py`
- Launch command: `python -m streamlit run app/step5_app.py`

## Planned tests and results

| Test ID | Input/action | Expected behaviour | Actual result | Status |
|---|---|---|---|---|
| T01 | Dirt 70, load 5 kg, Cotton, Low | Generate prediction | Prediction generated successfully; wash time 92.01596 min, water 75.505856 L, detergent 69.856207 ml, spin speed 975.397537 RPM | PASS |
| T02 | Compare UI and script predictions for identical inputs | All four output values should match | Exact match; maximum difference 0.0 | PASS |
| T03 | Dirt level 0 | Accept minimum dirt boundary | Prediction generated successfully | PASS |
| T04 | Dirt level 100 | Accept maximum dirt boundary | Prediction generated successfully | PASS |
| T05 | Load 0.1 kg | Accept minimum load boundary | Prediction generated successfully | PASS |
| T06 | Load 10 kg | Accept maximum load boundary | Prediction generated successfully | PASS |
| T07 | Dirt level 101 | Reject out-of-range value | UI displayed allowed range 0.00 to 100.00 | PASS |
| T08 | Load -1 kg | Reject out-of-range value | UI displayed allowed range 0.10 to 10.00 | PASS |
| T09 | Run `python -m unittest -v test_product_predict` | All automated tests should pass | 5 tests ran; all 5 passed | PASS |
| T10 | Temporarily remove model in a separate test copy | Display a clear missing-model error | App displayed Saved ANN model not found; original model remained untouched | PASS |
| T11 | Restore model in temporary copy and predict again | Prediction should work after restoration | Prediction generated successfully | PASS |

## Evidence

| Test ID | Evidence file or observed output |
|---|---|
| T01 | `data/reports/step6_ui_prediction.csv` |
| T02 | `data/reports/step6_ui_prediction.csv` and `data/reports/step6_script_prediction.csv`; exact match, maximum difference 0.0 |
| T03-T08 | Observed Streamlit prediction results and input validation messages recorded during testing |
| T09 | Terminal output: 5 tests ran, OK |
| T10 | Temporary-copy UI error: Saved ANN model not found |
| T11 | Successful prediction after restoring the temporary model |

## Failures, fixes and retests

- No unresolved application failures were observed during the planned tests.
- The missing-model scenario was tested in a temporary copy of the project. The application displayed a clear error instead of generating a prediction.
- After restoring the model in the temporary copy, prediction generation worked successfully.
- The original model file was not modified.

## Known limits

- The ANN model uses simulated project data; predictions are not verified against a physical washing machine.
- The application provides predictions and does not directly control washing-machine hardware.
- Invalid numeric values outside the permitted ranges are blocked by the UI. Invalid categories and missing required inputs were also checked through automated unit tests.

## Contributions

- Executed normal prediction and boundary validation tests.
- Compared UI and script predictions using identical inputs.
- Verified invalid numeric input handling.
- Executed all five automated unit tests successfully.
- Tested missing-model error handling and recovery using a temporary project copy.
- Saved Step 6 UI and script prediction CSV evidence.
