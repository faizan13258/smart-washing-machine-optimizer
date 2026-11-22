# Step 4 - Fair Comparison Report

## Team and Project

**Project Title:** Smart Washing Machine Decision & Resource Optimizer  
**Project Domain:** Soft Computing  
**Branch:** `step-4-baseline`  
**Baseline Model:** Fixed Cycle Lookup  
**Machine Learning Model:** Artificial Neural Network (ANN)

## Question

The objective of Step 4 is to compare the Artificial Neural Network (ANN) model developed in Step 3 with a traditional Fixed Cycle Lookup baseline.

The comparison evaluates whether the ANN model predicts washing machine parameters more accurately than a fixed-cycle approach.

The four target parameters are:

- Wash Time (minutes)
- Water Consumption (litres)
- Detergent Quantity (ml)
- Spin Speed (RPM)

## Data and Scenarios

The project uses 10,000 simulated washing machine scenarios.

The dataset contains the following input features:

- Dirt Level
- Load (kg)
- Fabric Type
- Water Availability

The dataset was divided into three subsets:

| Dataset | Number of Rows |
|---|---:|
| Training | 7,000 |
| Validation | 1,500 |
| Testing | 1,500 |
| Total | 10,000 |

The same scenario split and corresponding target values were used for a fair comparison between ANN and the baseline.

## Baseline Rule

A Fixed Cycle Lookup baseline was implemented using training data only.

The baseline predicts washing parameters using grouped median values based on:

1. Fabric type
2. Dirt level category
3. Load category
4. Water availability

The dirt categories are Light, Normal and Heavy. Load categories are Small, Medium and Large.

A hierarchical fallback mechanism is included for cases where an exact group is unavailable.

The lookup table is built using only training data to prevent data leakage.

## Fair-Comparison Checks

The following checks were performed:

- Recreated the original Step 3 train, validation and test split.
- Verified scenario IDs and their order.
- Checked input features and actual target values.
- Used the same validation and test scenarios for both models.
- Built the baseline lookup using training data only.
- Verified prediction alignment.

**Validation fallback level:** 0 for all 1,500 rows.

**Test fallback level:** 0 for all 1,500 rows.

**Scenario alignment checks:** PASS.

## Results

The models were evaluated using Mean Absolute Error (MAE), Root Mean Squared Error (RMSE) and R-squared (R²).

### Test Dataset Results

| Target | Model | MAE | RMSE | R² |
|---|---|---:|---:|---:|
| Wash Time | ANN | 0.158327 | 0.201333 | 0.999888 |
| Wash Time | Fixed Cycle Lookup | 5.181483 | 6.285184 | 0.890772 |
| Water Consumption | ANN | 0.212372 | 0.266299 | 0.999894 |
| Water Consumption | Fixed Cycle Lookup | 7.771213 | 9.149413 | 0.875251 |
| Detergent Quantity | ANN | 0.124914 | 0.155909 | 0.999925 |
| Detergent Quantity | Fixed Cycle Lookup | 4.929290 | 6.095778 | 0.885454 |
| Spin Speed | ANN | 1.370011 | 1.716632 | 0.999890 |
| Spin Speed | Fixed Cycle Lookup | 11.103667 | 13.314973 | 0.993365 |

### Validation Dataset Results

| Target | Model | MAE | RMSE | R² |
|---|---|---:|---:|---:|
| Wash Time | ANN | 0.158586 | 0.203570 | 0.999889 |
| Wash Time | Fixed Cycle Lookup | 5.320203 | 6.373313 | 0.890897 |
| Water Consumption | ANN | 0.213346 | 0.272467 | 0.999890 |
| Water Consumption | Fixed Cycle Lookup | 7.743990 | 9.172823 | 0.875553 |
| Detergent Quantity | ANN | 0.127971 | 0.160909 | 0.999922 |
| Detergent Quantity | Fixed Cycle Lookup | 5.086350 | 6.208532 | 0.883529 |
| Spin Speed | ANN | 1.349218 | 1.696571 | 0.999891 |
| Spin Speed | Fixed Cycle Lookup | 10.787333 | 13.028251 | 0.993588 |

## Interpretation

The ANN model achieved lower MAE and RMSE than the Fixed Cycle Lookup baseline for all four target parameters on both validation and test datasets.

The results indicate that ANN can model the relationships in the simulated dataset more accurately than the fixed-cycle lookup approach.

The baseline provides a simpler and more interpretable alternative, but its predictions are less accurate for this dataset.

## Limitations and Responsible Use

- The dataset and target values are simulated using predefined rules.
- The results do not represent measurements from a real washing machine.
- The ANN's high accuracy reflects its ability to learn the simulated target-generation patterns.
- Real-world testing with actual washing machine sensors and measurements is required before practical deployment.
- The system should be treated as an educational prototype and not as a certified appliance controller.

## Reproducibility and Evidence

The comparison can be reproduced using:

`src/compare_baseline.py`

The notebook used for reproduction is:

`notebooks/03_baseline_comparison.ipynb`

Generated evidence files:

- `report/step4_baseline_metrics.csv`
- `report/step4_comparison.csv`
- `report/step4_fixed_cycle_lookup.csv`
- `results/step4_validation_paired_predictions.csv`
- `results/step4_test_paired_predictions.csv`
- `results/step4_baseline_vs_ann.png`

Notebook reproduction completed successfully.

Scenario alignment checks: PASS.

## Team Contributions

The project work includes dataset preparation, ANN model development, baseline implementation, model comparison, validation, testing and documentation.

**Contribution details should reflect the actual work performed by each project member.**