import streamlit as st
import pandas as pd
from storage_helper import download_data_from_blob, get_blob_last_modified


st.set_page_config(page_title="Energy Data Dashboard", layout="wide")

st.title("Energy Data Dashboard")

# Read latest saved data from Azure Blob Storage
try:
    data = download_data_from_blob()
    last_modified = get_blob_last_modified()
except Exception as e:
    st.error(f"Error loading data from Blob Storage: {e}")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(data)

if df.empty:
    st.warning("No data available.")
    st.stop()

# Status / last update
st.subheader("Status")
st.success(f"Latest data loaded successfully. Last update: {last_modified}")

# Show latest values for DK1 and DK2
st.subheader("Latest Values")

dk1_value = None
dk2_value = None

dk1_rows = df[df["area"] == "DK1"]
dk2_rows = df[df["area"] == "DK2"]

if not dk1_rows.empty:
    dk1_value = dk1_rows.iloc[-1]["value"]

if not dk2_rows.empty:
    dk2_value = dk2_rows.iloc[-1]["value"]

col1, col2 = st.columns(2)

with col1:
    st.metric(label="DK1", value=dk1_value if dk1_value is not None else "N/A")

with col2:
    st.metric(label="DK2", value=dk2_value if dk2_value is not None else "N/A")

# Filter by area (bonus)
st.subheader("Filter by Area")

selected_area = st.selectbox(
    "Choose area",
    ["All", "DK1", "DK2"]
)

if selected_area == "All":
    filtered_df = df
else:
    filtered_df = df[df["area"] == selected_area]

# Show table
st.subheader("Retrieved Data")
st.dataframe(filtered_df, use_container_width=True)

# Show chart
st.subheader("Chart")

chart_df = filtered_df.copy()

if not chart_df.empty:
    chart_df["mtuStart"] = pd.to_datetime(chart_df["mtuStart"])
    chart_df = chart_df.sort_values("mtuStart")
    chart_df = chart_df.set_index("mtuStart")

    st.line_chart(chart_df["value"])
else:
    st.info("No data available for chart.")

# Optional: small summary
st.subheader("Data Summary")
st.write(f"Number of rows: {len(filtered_df)}")