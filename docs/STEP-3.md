# Step 3 - Artificial Neural Network (ANN)

## Project
Smart Washing Machine Decision & Resource Optimizer

## 1. Objective
The objective of this phase is to develop an Artificial Neural Network that predicts washing-machine resource and operation parameters from input conditions.

## 2. Input Features
- Dirt level (0-100)
- Laundry load (kg)
- Fabric type
- Water availability

## 3. Prediction Outputs
- Washing time (minutes)
- Water consumption (litres)
- Detergent quantity (ml)
- Spin speed (RPM)

## 4. Dataset
The input dataset contains 10,000 simulated washing scenarios.

The dataset was divided into:
- Training: 70% (7,000 records)
- Validation: 15% (1,500 records)
- Testing: 15% (1,500 records)

Random state: 42

## 5. Target Generation - Important Limitation
The original input dataset did not contain measured output labels. Therefore, illustrative target outputs were generated using documented deterministic rules based on dirt level, load, fabric type and water availability.

These are simulated labels, not real measurements from a washing machine. The ANN learns these generated relationships. Consequently, evaluation metrics measure agreement with simulated labels and do not establish real-world machine accuracy or resource savings.

## 6. ANN Architecture
- Algorithm: Multi-output MLPRegressor
- Hidden layers: 64 and 32 neurons
- Activation: ReLU
- Solver: Adam
- Initial learning rate: 0.001
- Batch size: 64
- Maximum iterations: 1200
- Early stopping: Enabled
- Random state: 42

## 7. Data Preprocessing
- StandardScaler for numerical input features
- OneHotEncoder for categorical input features
- StandardScaler for output targets

## 8. Evaluation Metrics
Since all prediction targets are continuous numerical values, this is a regression problem.

The following metrics are used:
- MAE: Mean Absolute Error
- RMSE: Root Mean Squared Error
- R2: Coefficient of Determination

A confusion matrix is not suitable for this multi-output regression task.

## 9. Test Results

| Target | Test MAE | Test RMSE | Test R2 |
|---|---:|---:|---:|
| Wash time | 0.158327 | 0.201333 | 0.999888 |
| Water consumption | 0.212372 | 0.266299 | 0.999894 |
| Detergent quantity | 0.124914 | 0.155909 | 0.999925 |
| Spin speed | 1.370011 | 1.716632 | 0.999890 |

These results indicate that the ANN closely learned the simulated target-generation rules.

## 10. Generated Deliverables
- notebooks/02_ann_model.ipynb
- src/train_ann.py
- data/processed/ann_training_dataset.csv
- results/ann_metrics.csv
- results/ann_validation_predictions.csv
- results/ann_test_predictions.csv
- results/ann_loss_curve.png
- results/ann_wash_time_min_prediction.png
- results/ann_water_consumption_l_prediction.png
- results/ann_detergent_ml_prediction.png
- results/ann_spin_speed_rpm_prediction.png
- models/washing_machine_ann.joblib
- models/ann_metadata.json
- report/ann_metrics.json

## 11. Conclusion
The ANN training and evaluation pipeline was successfully implemented. It predicts four numerical outputs from washing scenario inputs and generates validation and test results.

Further work should use experimentally measured washing-machine data to validate the model under real operating conditions.
