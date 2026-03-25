import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from azure.cosmos import CosmosClient

st.set_page_config(page_title="Energy Data Dashboard", layout="wide")

DATABASE_NAME = "energydb"
CONTAINER_NAME = "energydata"


def get_setting(name):
    value = os.getenv(name)
    if value:
        return value

    try:
        with open("local.settings.json", "r") as file:
            settings = json.load(file)
        return settings["Values"].get(name)
    except Exception:
        return None


def get_cosmos_container():
    endpoint = get_setting("COSMOS_ENDPOINT")
    key = get_setting("COSMOS_KEY")

    if not endpoint or not key:
        st.error("Cosmos DB configuration is missing.")
        st.stop()

    client = CosmosClient(endpoint, key)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)
    return container


# @st.cache_data(ttl=60)
def read_all_items_from_cosmos():
    try:
        container = get_cosmos_container()
        query = "SELECT * FROM c"
        items = list(
            container.query_items(
                query=query,
                enable_cross_partition_query=True
            )
        )
        return items
    except Exception as e:
        st.error(f"Error while reading data from Cosmos DB: {e}")
        return []





data = read_all_items_from_cosmos()

if not data:
    st.warning("No data available.")
    st.stop()

df = pd.DataFrame(data)

required_columns = ["timeStamp", "mtuStart", "area", "value"]
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing columns in data: {missing_columns}")
    st.stop()

df["timeStamp"] = pd.to_datetime(df["timeStamp"], errors="coerce", utc=True)
df["mtuStart"] = pd.to_datetime(df["mtuStart"], errors="coerce", utc=True)
df["fetchTime"] = pd.to_datetime(df["fetchTime"], errors="coerce", utc=True)
df["fetchTime"]= df["fetchTime"].dt.tz_convert("Europe/Rome")
df["value"] = pd.to_numeric(df["value"], errors="coerce")
df["_ts"]= pd.to_datetime(df["_ts"], unit="s", utc= True)

df = df.dropna(subset=["timeStamp", "mtuStart", "area", "value"])



default_areas= sorted(df["area"].dropna().unique().tolist())
if "selected_areas" not in st.session_state:
    st.session_state["selected_areas"] = default_areas
col1, col2 = st.columns([7, 1]) 
with col1: st.title("Energy Data Dashboard")
with col2: 
    st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Refresh"): 
     st.session_state["period_filter"]= "Latest"
     st.session_state["selected_areas"]= default_areas
     st.rerun()


option = st.selectbox(
    "Select period",
    ["Latest", "Last Week", "Custom Period"],
    key= "period_filter"
)

selected_areas = st.multiselect(
    "Select Area",
    options=default_areas,
    key= "selected_areas"
)

filtered_df = df.copy()
filtered_df= filtered_df[filtered_df["area"].isin(selected_areas)]
if option == "Latest":
    latest_ts = filtered_df["timeStamp"].max()
    filtered_df = filtered_df[filtered_df["timeStamp"] == latest_ts]

elif option == "Last Week":
    one_week_ago = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=7)
    filtered_df = filtered_df[filtered_df["timeStamp"] >= one_week_ago]

elif option == "Custom Period":
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start date")

    with col2:
        end_date = st.date_input("End date")

    if end_date < start_date:
        st.error("End date cannot be earlier than start date.")
        st.stop()

    start_dt = pd.to_datetime(start_date).tz_localize("UTC")
    # end_dt = pd.to_datetime(end_date).dt.tz_localize("UTC") + pd.Timedelta(days=1)
    end_dt = pd.to_datetime(end_date).tz_localize("UTC") + pd.Timedelta(days=1)
    
    filtered_df = filtered_df[
        (filtered_df["timeStamp"] >= start_dt) &
        (filtered_df["timeStamp"] < end_dt)
    ]

filtered_df = filtered_df.sort_values("mtuStart")

most_recent_fetch = df["_ts"].max()
most_recent_fetch_local = most_recent_fetch.tz_convert("Europe/Rome")
formatted_fetch_time= most_recent_fetch_local.strftime("%Y-%m-%d %H:%M:%S %Z")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total records", len(filtered_df))

with col2:
    st.metric(
        "Most recent fetch time",
        str(formatted_fetch_time) if formatted_fetch_time is not None else "N/A"
    )

st.subheader("Data Table")
st.dataframe(
    filtered_df[["timeStamp", "mtuStart", "area", "value"]],
    use_container_width=True
)

st.subheader("DK1 and DK2 Chart")
fig = px.line(
    filtered_df,
    x="mtuStart",
    y="value",
    color="area",
    color_discrete_map={"DK1": "#1f77b4","DK2": "#e63946"},
    markers=True,
    title="DK1 and DK2 Values Over Time",
    labels={
        "mtuStart": "MTU Start",
        "value": "Value",
        "area": "Area"
    }
)

fig.update_traces(mode="lines+markers",line=dict(width=3),marker=dict(size=6)) 
fig.update_layout(legend_title_text="Area", template= "plotly_white", 
    xaxis=dict(showgrid=True, gridcolor="lightgray"),
    yaxis=dict(showgrid=True, gridcolor="lightgray"),   
    title={
        "text": "DK1 and DK2 Values Over Time",
        "font": {"size": 20, "color": "#584E50"}
    }
  

) 
st.plotly_chart(fig, use_container_width=True,  
config={ "displayModeBar": True, "displaylogo":False, 
        "modeBarButtonsToRemove": [ "zoom2d",
                                    "pan2d", 
                                    "select2d", 
                                    "lasso2d", 
                                    "autoScale2d",
                                    "resetScale2d",
                                        "toImage" ] 
    })