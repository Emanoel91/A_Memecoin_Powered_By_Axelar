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

st.title("Any Inu: Swap Analysis🔄")

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

# --- Row 2: Combo Chart ---
monthly_summary = df.groupby(df["Date"].dt.to_period("M")).agg(
    {"Swap Count": "sum", "Swap Volume ($USD)": "sum"}
).reset_index()
monthly_summary["Date"] = monthly_summary["Date"].dt.to_timestamp()

fig_combo = go.Figure()
fig_combo.add_trace(go.Bar(
    x=monthly_summary["Date"],
    y=monthly_summary["Swap Count"],
    name="Total Swaps",
    marker_color='steelblue',
    yaxis="y1"
))
fig_combo.add_trace(go.Scatter(
    x=monthly_summary["Date"],
    y=monthly_summary["Swap Volume ($USD)"],
    name="Total Volume ($USD)",
    marker_color='orange',
    yaxis="y2"
))

fig_combo.update_layout(
    title="Monthly Swap Count vs Swap Volume ($USD)",
    xaxis=dict(title="Date"),
    yaxis=dict(title="Swap Count", side="left"),
    yaxis2=dict(title="Volume ($USD)", overlaying="y", side="right"),
    legend=dict(x=0.01, y=0.99),
    bargap=0.3
)
st.plotly_chart(fig_combo, use_container_width=True)

# --- Row 3: Stacked Bar Charts for Count & Swappers ---
count_monthly = df.groupby([df["Date"].dt.to_period("M"), "Chain"])["Swap Count"].sum().reset_index()
count_monthly["Date"] = count_monthly["Date"].dt.to_timestamp()

swappers_monthly = df.groupby([df["Date"].dt.to_period("M"), "Chain"])["Swapper Count"].sum().reset_index()
swappers_monthly["Date"] = swappers_monthly["Date"].dt.to_timestamp()

col1, col2 = st.columns(2)
with col1:
    fig_count = px.bar(
        count_monthly, x="Date", y="Swap Count", color="Chain",
        title="Number of AI Token Swaps By Chain per Month",
        barmode="stack"
    )
    st.plotly_chart(fig_count, use_container_width=True)

with col2:
    fig_swappers = px.bar(
        swappers_monthly, x="Date", y="Swapper Count", color="Chain",
        title="Number of AI Token Swappers By Chain per Month",
        barmode="stack"
    )
    st.plotly_chart(fig_swappers, use_container_width=True)

# --- Row 4: Stacked Bar Charts for Volume ---
usd_monthly = df.groupby([df["Date"].dt.to_period("M"), "Chain"])["Swap Volume ($USD)"].sum().reset_index()
usd_monthly["Date"] = usd_monthly["Date"].dt.to_timestamp()

ai_monthly = df.groupby([df["Date"].dt.to_period("M"), "Chain"])["Swap Volume ($AI)"].sum().reset_index()
ai_monthly["Date"] = ai_monthly["Date"].dt.to_timestamp()

col3, col4 = st.columns(2)
with col3:
    fig_usd = px.bar(
        usd_monthly, x="Date", y="Swap Volume ($USD)", color="Chain",
        title="Volume of AI Token Swaps By Chain per Month ($USD)",
        barmode="stack"
    )
    st.plotly_chart(fig_usd, use_container_width=True)

with col4:
    fig_ai = px.bar(
        ai_monthly, x="Date", y="Swap Volume ($AI)", color="Chain",
        title="Volume of AI Token Swaps By Chain per Month ($AI)",
        barmode="stack"
    )
    st.plotly_chart(fig_ai, use_container_width=True)

# --- Row 5: Donut Charts ---
chain_summary = df.groupby("Chain").agg(
    {"Swap Count": "sum", "Swap Volume ($USD)": "sum", "Swap Volume ($AI)": "sum"}
).reset_index()

col1, col2, col3 = st.columns(3)
with col1:
    fig_donut1 = px.pie(chain_summary, names="Chain", values="Swap Count", hole=0.5, title="Total Number of Swaps Across Chains")
    st.plotly_chart(fig_donut1, use_container_width=True)

with col2:
    fig_donut2 = px.pie(chain_summary, names="Chain", values="Swap Volume ($USD)", hole=0.5, title="Total Swap Volume ($USD) Across Chains")
    st.plotly_chart(fig_donut2, use_container_width=True)

with col3:
    fig_donut3 = px.pie(chain_summary, names="Chain", values="Swap Volume ($AI)", hole=0.5, title="Total Swap Volume ($AI) Across Chains")
    st.plotly_chart(fig_donut3, use_container_width=True)

