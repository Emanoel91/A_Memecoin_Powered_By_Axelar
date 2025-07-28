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

# --- Row 6: Market Share Trend by Chain Over Time (Stacked Area Chart) ---
if not df.empty:
    df['Date'] = pd.to_datetime(df['Date'])
    total_by_date = df.groupby('Date')['Swap Volume ($USD)'].transform('sum')
    df['Market Share (%)'] = (df['Swap Volume ($USD)'] / total_by_date) * 100

    fig_market_share = px.area(
        df,
        x='Date',
        y='Market Share (%)',
        color='Chain',
        title="Any Inu ($AI) Market Share Trend by Chain Over Time",
        groupnorm='percent',
        hover_data={
            'Swap Volume ($USD)': ':.2f',
            'Market Share (%)': ':.2f',
            'Chain': True
        },
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig_market_share.update_traces(line=dict(width=0.5))
    fig_market_share.update_layout(
        yaxis_title='Market Share (%)',
        xaxis_title='Date',
        legend_title='Chain',
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig_market_share, use_container_width=True)

# -----------------------
# --- Load Data ---
@st.cache_data(ttl=3600)
def load_dune_dex():
    url = "https://api.dune.com/api/v1/query/5544025/results?api_key=kmCBMTxWKBxn6CVgCXhwDvcFL1fBp6rO"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data["result"]["rows"])
        return df
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return pd.DataFrame()

dex_df = load_dune_dex()

if not dex_df.empty:
    dex_df = dex_df.sort_values(by="Swap Count", ascending=True).reset_index(drop=True)
    dex_df.index = dex_df.index + 1

    st.subheader("🔵Any Inu ($AI) Swap Stats By DEX Across Different Chains")
    st.dataframe(dex_df.style.format({
        "Swap Count": "{:,.0f}",
        "Swap Volume ($AI)": "{:,.0f}",
        "Swap Volume ($USD)": "{:,.0f}",
        "Swapper Count": "{:,.0f}"
    }), use_container_width=True)

    col1, col2 = st.columns(2)

    swap_count_norm = dex_df.groupby(['Chain', 'dex'])['Swap Count'].sum().reset_index()
    total_per_chain = swap_count_norm.groupby('Chain')['Swap Count'].transform('sum')
    swap_count_norm['Percentage'] = swap_count_norm['Swap Count'] / total_per_chain * 100

    fig1 = px.bar(
        swap_count_norm,
        x="Chain",
        y="Percentage",
        color="dex",
        title="Normalized Swap Count (%) by Chain and DEX",
        text=swap_count_norm["Percentage"].round(1).astype(str) + '%'
    )
    fig1.update_layout(barmode="stack", yaxis_title="Percentage (%)")
    col1.plotly_chart(fig1, use_container_width=True)

    swap_volume_norm = dex_df.groupby(['Chain', 'dex'])['Swap Volume ($AI)'].sum().reset_index()
    total_vol_chain = swap_volume_norm.groupby('Chain')['Swap Volume ($AI)'].transform('sum')
    swap_volume_norm['Percentage'] = swap_volume_norm['Swap Volume ($AI)'] / total_vol_chain * 100

    fig2 = px.bar(
        swap_volume_norm,
        x="Chain",
        y="Percentage",
        color="dex",
        title="Normalized Swap Volume ($AI) (%) by Chain and DEX",
        text=swap_volume_norm["Percentage"].round(1).astype(str) + '%'
    )
    fig2.update_layout(barmode="stack", yaxis_title="Percentage (%)")
    col2.plotly_chart(fig2, use_container_width=True)

    col3, col4, col5 = st.columns(3)

    count_by_dex = dex_df.groupby('dex')['Swap Count'].sum().sort_values(ascending=True)
    fig3 = px.bar(
        count_by_dex,
        x=count_by_dex.values,
        y=count_by_dex.index,
        orientation='h',
        title="Total Swap Count by DEX",
        text=count_by_dex.values
    )
    fig3.update_traces(textposition="outside")
    fig3.update_layout(xaxis_title="Swap Count")
    col3.plotly_chart(fig3, use_container_width=True)

    ai_by_dex = dex_df.groupby('dex')['Swap Volume ($AI)'].sum().sort_values(ascending=True)
    fig4 = px.bar(
        ai_by_dex,
        x=ai_by_dex.values,
        y=ai_by_dex.index,
        orientation='h',
        title="Total Swap Volume ($AI) by DEX",
        text=ai_by_dex.values.round(0)
    )
    fig4.update_traces(textposition="outside")
    fig4.update_layout(xaxis_title="Swap Volume ($AI)")
    col4.plotly_chart(fig4, use_container_width=True)

    usd_by_dex = dex_df.groupby('dex')['Swap Volume ($USD)'].sum().sort_values(ascending=True)
    fig5 = px.bar(
        usd_by_dex,
        x=usd_by_dex.values,
        y=usd_by_dex.index,
        orientation='h',
        title="Total Swap Volume ($USD) by DEX",
        text=usd_by_dex.values.round(0)
    )
    fig5.update_traces(textposition="outside")
    fig5.update_layout(xaxis_title="Swap Volume ($USD)")
    col5.plotly_chart(fig5, use_container_width=True)

    swapper_by_chain_dex = dex_df.groupby(['Chain', 'dex'])['Swapper Count'].sum().reset_index()
    fig6 = px.bar(
        swapper_by_chain_dex,
        x="Chain",
        y="Swapper Count",
        color="dex",
        barmode="group",
        title="Swapper Count by Chain and DEX",
        text=swapper_by_chain_dex["Swapper Count"]
    )
    fig6.update_traces(textposition="outside")
    st.plotly_chart(fig6, use_container_width=True)

else:
    st.warning("No data available.")


st.info(
    "🔔The data in this section is updated on Mondays between 3:30 and 4:00 PM. "
    "To view the most recent updates, click on the '...' in the top-right corner of the page and select 'Rerun'."
)
