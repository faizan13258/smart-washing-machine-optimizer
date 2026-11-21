
# Smart Washing Machine Decision & Resource Optimizer

## Project Overview
This project recommends washing settings based on dirt level, laundry load, fabric type, and water availability.

## Core Techniques
- Fuzzy Logic for handling uncertain washing conditions
- Genetic Algorithm for optimizing washing settings
- Fixed-cycle baseline for comparison

## Input Parameters
- Dirt level
- Laundry load size
- Fabric type
- Water availability

## Output Parameters
- Wash time
- Water consumption
- Detergent quantity
- Spin speed

## Technology Stack
- Python
- NumPy
- Pandas
- Matplotlib
- Scikit-Fuzzy
- Streamlit

## Project Structure
- `app/` — User interface
- `src/` — Algorithm implementations
- `data/` — Dataset information
- `results/` — Experimental results and visualizations
- `report/` — Project report and screenshots

## Status
Project setup and implementation are in progress.
# Step 3 - Artificial Neural Network (ANN)

## Overview
This phase implements a multi-output ANN for the Smart Washing Machine Decision & Resource Optimizer.

## Input Features
- Dirt level
- Laundry load
- Fabric type
- Water availability

## Predicted Outputs
- Washing time (minutes)
- Water consumption (litres)
- Detergent quantity (ml)
- Spin speed (RPM)

## ANN Configuration
- Model: Scikit-learn MLPRegressor
- Hidden layers: 64 and 32 neurons
- Activation: ReLU
- Optimizer: Adam
- Dataset: 10,000 simulated scenarios
- Split: 70% training, 15% validation, 15% testing

## Evaluation
Performance metrics: MAE, RMSE and R-squared. See results/ann_metrics.csv.

## Important Data Limitation
Target outputs are generated using deterministic simulation rules. They are not real washing-machine measurements. Metrics demonstrate learning of simulated relationships, not verified real-world accuracy or resource savings.

## Step 3 Files
- src/train_ann.py - ANN training and evaluation
- notebooks/02_ann_model.ipynb - Experiment notebook
- docs/STEP-3.md - Detailed documentation
- models/ - Saved model and metadata
- results/ - Metrics, predictions and graphs

## Run ANN Training
python src/train_ann.py
