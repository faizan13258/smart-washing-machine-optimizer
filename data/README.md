# Dataset Information

## Project
Smart Washing Machine Decision & Resource Optimizer using Fuzzy Logic and Genetic Algorithm.

## Dataset Requirements
The project aims to generate at least 10,000 valid and documented washing machine scenarios.

## Input Features
- Dirt level: 0–100
- Laundry load: 0–10 kg
- Fabric type: Cotton, Synthetic, Delicate, Wool
- Water availability: Low, Medium, High

## Output Features
- Wash time: minutes
- Water consumption: litres
- Detergent quantity: grams
- Spin speed: revolutions per minute (RPM)

## Data Source
The project will use simulated washing machine scenarios. These scenarios are generated for testing and are not claimed to be real-world collected records. No external dataset source or licence is claimed at this stage.

## Scenario Generation
A reproducible Python script will generate scenarios using documented input ranges and assumptions. The generation process will include normal, boundary, stress, and invalid test cases.

## Preprocessing and Validation
- Check for missing values.
- Validate input types and permitted ranges.
- Check supported fabric and water availability categories.
- Separate invalid test cases from valid scenarios.
- Save generated data in a reproducible format.

## Reproducibility
The scenario-generation and validation process will be implemented in Python so the scenarios can be regenerated and checked consistently.

## Limitations
Simulated scenarios are based on documented assumptions and may not represent every real washing machine or fabric condition.
