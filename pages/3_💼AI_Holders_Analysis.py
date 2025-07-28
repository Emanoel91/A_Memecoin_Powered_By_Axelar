import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

# --- Page Config: Tab Title & Icon ---
st.set_page_config(
    page_title="Any Inu: A Memecoin Powered By Axelar",
    page_icon="https://raw.githubusercontent.com/axelarnetwork/axelar-configs/main/images/tokens/ai.svg",
    layout="wide"
)

st.title("💼Any Inu Holders Analysis")

st.info(
    "🔔The data in this section is updated on Mondays between 14:30 and 15:00 UTC. "
    "To view the most recent updates, click on the '...' in the top-right corner of the page and select 'Rerun'."
)

# --- Load data from Dune API ---
@st.cache_data(ttl=3600)
def load_dune_ai_swaps():
    url = "https://api.dune.com/api/v1/query/5542748/results?api_key=kmCBMTxWKBxn6CVgCXhwDvcFL1fBp6rO"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data["result"]["rows"])
        df["Date"] = pd.to_datetime(df["Date"])
        for col in ["Swap Count", "Swap Volume ($AI)", "Swap Volume ($USD)", "Swapper Count"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        return df
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return pd.DataFrame()

df = load_dune_ai_swaps()

if df.empty:
    st.warning("No data available.")
    st.stop()

# --- KPIs ---
total_swaps = df["Swap Count"].sum()
total_volume_ai = df["Swap Volume ($AI)"].sum()
total_volume_usd = df["Swap Volume ($USD)"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Number of Swaps", f"{total_swaps:,.0f}")
col2.metric("Total Volume of Swaps ($AI)", f"{total_volume_ai:,.0f}")
col3.metric("Total Volume of Swaps ($USD)", f"${total_volume_usd:,.0f}")



