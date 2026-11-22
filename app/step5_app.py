import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.product_predict import predict_one

st.set_page_config(
    page_title="Smart Washing Machine Optimizer",
    page_icon="🧺",
    layout="wide"
)

st.title("🧺 Smart Washing Machine Decision & Resource Optimizer")
st.write(
    "Enter your laundry details to get washing-cycle predictions "
    "from the saved Artificial Neural Network."
)

st.info(
    "Educational prototype: predictions are based on simulated training "
    "targets, not measurements from a real washing machine."
)

with st.form("washing_prediction_form"):
    st.subheader("Laundry Details")

    col1, col2 = st.columns(2)

    with col1:
        dirt_level = st.number_input(
            "Dirt Level (0–100)",
            min_value=0.0,
            max_value=100.0,
            value=70.0,
            step=1.0
        )

        load_kg = st.number_input(
            "Laundry Load (kg)",
            min_value=0.1,
            max_value=10.0,
            value=5.0,
            step=0.1
        )

    with col2:
        fabric_type = st.selectbox(
            "Fabric Type",
            ["Cotton", "Synthetic", "Delicate", "Wool"]
        )

        water_availability = st.selectbox(
            "Water Availability",
            ["Low", "Medium", "High"]
        )

    submitted = st.form_submit_button(
        "Predict Washing Settings",
        type="primary",
        width="stretch"
    )

if submitted:
    user_input = {
        "dirt_level": dirt_level,
        "load_kg": load_kg,
        "fabric_type": fabric_type,
        "water_availability": water_availability
    }

    try:
        result = predict_one(user_input)
        predictions = result["predictions"]

        st.success("Prediction generated successfully!")

        st.subheader("Predicted Washing Settings")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Wash Time", f"{predictions['wash_time_min']:.2f} min")
        c2.metric(
            "Water Consumption",
            f"{predictions['water_consumption_l']:.2f} L"
        )
        c3.metric("Detergent", f"{predictions['detergent_ml']:.2f} ml")
        c4.metric("Spin Speed", f"{predictions['spin_speed_rpm']:.2f} RPM")

        st.subheader("Prediction Details")

        output_row = {
            **result["inputs"],
            **predictions
        }

        output_df = pd.DataFrame([output_row])
        st.dataframe(output_df, width="stretch")

        csv_data = output_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Prediction CSV",
            data=csv_data,
            file_name="washing_machine_prediction.csv",
            mime="text/csv",
            width="stretch"
        )

    except (ValueError, FileNotFoundError) as error:
        st.error(f"Unable to generate prediction: {error}")
    except Exception as error:
        st.error(f"Unexpected error: {error}")

st.divider()
st.caption(
    "Smart Washing Machine Optimizer | Product V1 | "
    "Powered by a saved multi-output ANN model"
)
