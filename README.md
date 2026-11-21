# Smart Washing Machine Decision & Resource Optimizer

## 1. Project Overview

The Smart Washing Machine Decision & Resource Optimizer is a decision-support system that recommends suitable washing settings based on laundry conditions.

The system considers dirt level, laundry load, fabric type, and water availability to recommend washing parameters while aiming to reduce unnecessary water, detergent, and energy consumption.

The project uses Fuzzy Logic and Genetic Algorithm techniques and compares their results with a traditional fixed-cycle washing baseline.

## 2. Step 1: Project Contract

### 2.1 Project Objective

To design a smart washing decision system that recommends appropriate washing settings according to different laundry conditions.

### 2.2 Input Parameters

| Input              | Description               | Valid Range / Values              |
| ------------------ | ------------------------- | --------------------------------- |
| Dirt Level         | Amount of dirt on clothes | 0–100                             |
| Laundry Load       | Weight of laundry         | 0.1–10 kg                         |
| Fabric Type        | Type of clothing material | Cotton, Synthetic, Delicate, Wool |
| Water Availability | Available water level     | Low, Medium, High                 |

### 2.3 Output Parameters

| Output             | Description                     | Unit    |
| ------------------ | ------------------------------- | ------- |
| Wash Time          | Recommended washing duration    | Minutes |
| Water Consumption  | Estimated water required        | Litres  |
| Detergent Quantity | Recommended detergent amount    | ml      |
| Spin Speed         | Recommended drum spinning speed | RPM     |

### 2.4 System Scope

The system will:

- Accept laundry details from the user.
- Validate the entered input values.
- Process laundry conditions using decision-making techniques.
- Generate recommended washing settings.
- Compare smart recommendations with a fixed-cycle baseline.
- Display results in a simple user interface.

### 2.5 Project Limitations

- The initial system uses simulated test scenarios.
- Recommendations are software-generated estimates.
- The project does not directly control a physical washing machine.
- Actual washing performance may vary depending on machine specifications and detergent properties.

## 3. Core Techniques

### Fuzzy Logic

Fuzzy Logic will handle uncertain washing conditions such as low, medium, and high dirt levels and determine suitable washing settings.

### Genetic Algorithm

Genetic Algorithm will be used to optimize washing parameters while considering resource consumption and washing requirements.

### Fixed-Cycle Baseline

A traditional fixed-cycle approach will be implemented as a reference for comparing the optimized recommendations.

## 4. Named Roles and Responsibilities

This is an individual project. The project owner is responsible for all project activities.

| Responsible Person                     | Responsibility                                                                  |
| -------------------------------------- | ------------------------------------------------------------------------------- |
| Faizan Ali — Project Owner             | Overall project planning, implementation, testing, documentation and submission |
| Faizan Ali — Data & Validation         | Dataset preparation, input validation and test scenarios                        |
| Faizan Ali — Fuzzy Logic               | Design and implementation of the Fuzzy Logic system                             |
| Faizan Ali — Genetic Algorithm         | Optimization logic and resource-efficiency evaluation                           |
| Faizan Ali — Baseline & Evaluation     | Fixed-cycle implementation and performance comparison                           |
| Faizan Ali — Interface & Documentation | User interface, product sketch, reports and GitHub maintenance                  |

## 5. Starter Example Dataset

The following records demonstrate the expected input and output structure. Output values are illustrative examples, not measured washing-machine results.

```csv
scenario_id,dirt_level,load_kg,fabric_type,water_availability,expected_wash_time_min,expected_water_l,expected_detergent_ml,expected_spin_rpm
1,30,2.0,Cotton,Medium,40,45,35,800
2,80,5.0,Cotton,High,55,60,60,1000
3,50,3.0,Synthetic,Medium,45,50,40,800
4,20,1.5,Delicate,Low,35,35,25,600
5,90,7.0,Wool,High,50,65,55,600
```

These starter records are for demonstrating the data format. They must be validated and treated as examples, not real-world observations.

## 6. Input Validation Contract

The system must perform the following checks before processing:

| Validation                                       | Expected Result |
| ------------------------------------------------ | --------------- |
| Dirt level between 0 and 100                     | PASS            |
| Laundry load between 0.1 and 10 kg               | PASS            |
| Fabric type belongs to allowed categories        | PASS            |
| Water availability belongs to allowed categories | PASS            |
| No missing required values                       | PASS            |
| No duplicate scenario IDs                        | PASS            |

### PASS/FAIL Rules

- PASS: All required input fields contain valid values.
- FAIL: Any required value is missing, outside its allowed range, or belongs to an unsupported category.
- Invalid records must be rejected before recommendation generation.

## 7. Fixed-Cycle Baseline

The fixed-cycle baseline will provide the same reference washing settings regardless of the input conditions.

### Initial Baseline Settings

| Parameter          | Provisional Value |
| ------------------ | ----------------: |
| Wash Time          |        45 minutes |
| Water Consumption  |         60 litres |
| Detergent Quantity |             50 ml |
| Spin Speed         |           800 RPM |

These are initial project assumptions for comparison, not manufacturer specifications. They may be adjusted after testing.

### Baseline Pseudocode

```text
START

INPUT dirt_level
INPUT laundry_load
INPUT fabric_type
INPUT water_availability

VALIDATE all inputs

IF inputs are invalid:
    DISPLAY "FAIL - Invalid Input"
    STOP

SET wash_time = 45 minutes
SET water_consumption = 60 litres
SET detergent_quantity = 50 ml
SET spin_speed = 800 RPM

DISPLAY baseline washing settings

END
```

## 8. Product Sketch

### Proposed System Workflow

```text
        USER
         |
         v
  Enter Laundry Details
         |
         v
    Input Validation
         |
         v
   Decision Engine
         |
    +----+----+
    |         |
    v         v
 Fuzzy Logic  Genetic Algorithm
    |         |
    +----+----+
         |
         v
  Recommended Settings
         |
         v
   Fixed-Cycle Comparison
         |
         v
    Results Dashboard
         |
         v
  Water / Detergent / Time
       Estimates
```

### Proposed User Interface

The product interface will contain:

- Dirt level input field.
- Laundry load input field.
- Fabric type selection.
- Water availability selection.
- Generate Recommendation button.
- Recommended wash time.
- Estimated water consumption.
- Recommended detergent quantity.
- Recommended spin speed.
- Fixed-cycle comparison section.

## 9. Technology Stack

- Python
- NumPy
- Pandas
- Matplotlib
- Scikit-Fuzzy
- Streamlit
- Git and GitHub

## 10. Project Structure

```text
smart-washing-machine-optimizer/
│
├── app/
│   └── User Interface
│
├── src/
│   ├── Data Preparation
│   ├── Input Validation
│   ├── Fuzzy Logic
│   ├── Genetic Algorithm
│   └── Fixed-Cycle Baseline
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── results/
│
├── report/
│
└── README.md
```

## 11. Expected Outcome

The expected outcome is a working software prototype that accepts laundry conditions, validates the inputs, recommends washing settings, and compares optimized recommendations with a fixed-cycle baseline.

The system will be evaluated using simulated scenarios and documented validation and testing results.

## 12. Current Project Status

- [x] Project objective and input/output parameters defined.
- [x] Core techniques identified.
- [x] Project responsibilities documented.
- [x] Starter CSV format provided.
- [x] Input validation criteria defined.
- [x] Fixed-cycle baseline pseudocode documented.
- [x] Product workflow sketch included.
- [ ] Implementation and experimental evaluation to be completed.


## 13. Step 1 Deliverables

| Deliverable | File |
|---|---|
| Valid starter dataset | [starter_cases.csv](data/starter/starter_cases.csv) |
| Invalid test dataset | [invalid_cases.csv](data/starter/invalid_cases.csv) |
| Python input validator | [validate_step1.py](src/validate_step1.py) |
| Fixed-cycle baseline implementation | [fixed_cycle_baseline.py](src/fixed_cycle_baseline.py) |
| Actual validation and baseline results | [step1_validation_results.txt](results/step1_validation_results.txt) |
| Product interface sketch | [step1_interface_sketch.md](report/step1_interface_sketch.md) |

