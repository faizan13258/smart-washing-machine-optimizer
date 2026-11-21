def fixed_cycle_baseline(dirt_level, load_kg, fabric_type, water_availability):
    # Fixed settings used as a reference for comparison.
    return {
        "wash_time_min": 45,
        "water_consumption_l": 60,
        "detergent_quantity_ml": 50,
        "spin_speed_rpm": 800
    }


if __name__ == "__main__":
    result = fixed_cycle_baseline(
        dirt_level=80,
        load_kg=5.0,
        fabric_type="Cotton",
        water_availability="Medium"
    )

    print("FIXED-CYCLE BASELINE")
    print("--------------------")
    print("Wash Time:", result["wash_time_min"], "minutes")
    print("Water Consumption:", result["water_consumption_l"], "litres")
    print("Detergent Quantity:", result["detergent_quantity_ml"], "ml")
    print("Spin Speed:", result["spin_speed_rpm"], "RPM")
