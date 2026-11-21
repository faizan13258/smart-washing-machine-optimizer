import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
notebook_path = root / "notebooks" / "02_ann_model.ipynb"

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Step 3: Artificial Neural Network Model\n",
            "\n",
            "## Smart Washing Machine Decision & Resource Optimizer\n",
            "\n",
            "This notebook documents the ANN training and evaluation pipeline.\n",
            "\n",
            "**Important:** Target outputs are simulated using deterministic rules. They are not real washing-machine measurements."
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Dataset and Features\n",
            "\n",
            "Input features: dirt level, load weight, fabric type and water availability.\n",
            "\n",
            "Prediction targets: wash time, water consumption, detergent quantity and spin speed."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from pathlib import Path\n",
            "import pandas as pd\n",
            "import matplotlib.pyplot as plt\n",
            "\n",
            "ROOT = Path.cwd()\n",
            "if not (ROOT / 'results').exists():\n",
            "    ROOT = ROOT.parent\n",
            "\n",
            "data = pd.read_csv(ROOT / 'data/processed/ann_training_dataset.csv')\n",
            "metrics = pd.read_csv(ROOT / 'results/ann_metrics.csv')\n",
            "print('Dataset shape:', data.shape)\n",
            "display(data.head())\n",
            "display(metrics)"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Dataset Split\n",
            "\n",
            "The dataset was divided into 70% training, 15% validation and 15% testing data using random_state=42."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print('Total records:', len(data))\n",
            "print('Training records: 7000')\n",
            "print('Validation records: 1500')\n",
            "print('Testing records: 1500')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. ANN Architecture\n",
            "\n",
            "- Model: Multi-output MLPRegressor\n",
            "- Hidden layers: 64 and 32 neurons\n",
            "- Activation: ReLU\n",
            "- Optimizer: Adam\n",
            "- Initial learning rate: 0.001\n",
            "- Random state: 42\n",
            "- Early stopping: Enabled\n",
            "\n",
            "Numerical inputs and targets are scaled. Categorical inputs are one-hot encoded."
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Training Loss Curve\n"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from IPython.display import Image, display\n",
            "display(Image(filename=str(ROOT / 'results/ann_loss_curve.png')))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Validation and Test Metrics\n",
            "\n",
            "MAE, RMSE and R-squared are used because all four outputs are continuous numerical values. A confusion matrix is not appropriate for this regression problem."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "display(metrics.round(5))\n",
            "test_metrics = metrics[metrics['dataset'] == 'Test']\n",
            "display(test_metrics)"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Actual vs Predicted Plots\n"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "targets = ['wash_time_min', 'water_consumption_l', 'detergent_ml', 'spin_speed_rpm']\n",
            "for target in targets:\n",
            "    display(Image(filename=str(ROOT / 'results' / f'ann_{target}_prediction.png')))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. Conclusion and Limitations\n",
            "\n",
            "The ANN successfully learned the generated input-output relationships and produced predictions for four resource-related outputs. The test metrics indicate a close fit to the simulated labels.\n",
            "\n",
            "**Limitation:** The target values were generated using deterministic illustrative rules, not collected from a physical washing machine. Therefore, the metrics measure agreement with those simulated rules and do not establish real-world performance. Real sensor readings and experimentally verified labels would be required for real-world validation."
        ]
    }
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {"name": "python"}
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

notebook_path.write_text(json.dumps(notebook, indent=2), encoding="utf-8")
print("Created:", notebook_path)
