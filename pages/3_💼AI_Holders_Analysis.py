import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# --- Page Config ---
st.set_page_config(
    page_title="💼Any Inu Holders Analysis",
    page_icon="https://raw.githubusercontent.com/axelarnetwork/axelar-configs/main/images/tokens/ai.svg",
    layout="wide"
)

st.title("📊 Any Inu Holders Distribution")

# --- Load data from Dune API ---
@st.cache_data(ttl=3600)
def load_holders_data():
    url = "https://api.dune.com/api/v1/query/5543959/results?api_key=kmCBMTxWKBxn6CVgCXhwDvcFL1fBp6rO"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data["result"]["rows"])
        df["Holders Count"] = pd.to_numeric(df["Holders Count"], errors="coerce")
        return df
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return pd.DataFrame()

df = load_holders_data()

if df.empty:
    st.warning("No data available.")
    st.stop()

# --- Mapping logos ---
chain_logos = {
    "Ethereum": "https://img.cryptorank.io/coins/60x60.ethereum1524754015525.png",
    "Binance Smart Chain": "https://img.cryptorank.io/coins/60x60.wrapped%20bnb1648029706921.png",
    "Avalanche": "https://img.cryptorank.io/coins/60x60.avalanche1629705441155.png",
    "Mantle": "https://img.cryptorank.io/coins/60x60.mantle1739806212282.png",
    "Arbitrum": "https://img.cryptorank.io/coins/60x60.arbitrum1696871846920.png",
    "Polygon": "https://img.cryptorank.io/coins/60x60.polygon_ecosystem_token1698250519897.png",
    "Optimism": "https://img.cryptorank.io/coins/60x60.optimism1654027460186.png",
    "Celo": "https://img.cryptorank.io/coins/60x60.celo1673883176164.png",
    "Blast": "https://img.cryptorank.io/coins/60x60.blast1719473292032.png",
    "Scroll": "https://img.cryptorank.io/coins/60x60.scroll1693474620599.png",
    "Fantom": "https://img.cryptorank.io/coins/60x60.fantom1611564619788.png",
    "Linea": "https://img.cryptorank.io/coins/60x60.linea1680021297845.png",
    "Base": "https://img.cryptorank.io/coins/60x60.base1752857325751.png"
}

df["Logo"] = df["Chain"].map(chain_logos)

# --- KPI ---
total_holders = df["Holders Count"].sum()
st.markdown(
    f"<h2 style='text-align: center; color: #4CAF50;'>Number of Any Inu (AI) Holders: {total_holders:,}</h2>",
    unsafe_allow_html=True
)

# --- Charts ---
col1, col2 = st.columns(2)

with col1:
    df_sorted = df.sort_values("Holders Count", ascending=True)
    fig_bar = px.bar(
        df_sorted,
        x="Holders Count",
        y="Chain",
        orientation="h",
        text="Holders Count",
        title="Any Inu Holders by Chain",
    )
    fig_bar.update_traces(texttemplate="%{text:,}", textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    fig_donut = px.pie(
        df,
        values="Holders Count",
        names="Chain",
        hole=0.5,
        title="Distribution of Any Inu Holders"
    )
    st.plotly_chart(fig_donut, use_container_width=True)
