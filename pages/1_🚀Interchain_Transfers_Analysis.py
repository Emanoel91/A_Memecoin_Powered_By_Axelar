import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px
import plotly.graph_objects as go

# --- Page Config: Tab Title & Icon ---
st.set_page_config(
    page_title="Any Inu: A Memecoin Powered By Axelar",
    page_icon="https://axelarscan.io/logos/logo.png",
    layout="wide"
)

# --- Wide Layout ---
st.set_page_config(layout="wide")

st.title("Any Inu: Interchain Transfers Analysis🚀")

# --- Snowflake Connection ---
conn = snowflake.connector.connect(
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    account=st.secrets["snowflake"]["account"],
    warehouse="SNOWFLAKE_LEARNING_WH",
    database="AXELAR",
    schema="PUBLIC"
)

# --- Time Frame & Period Selection ---
timeframe = st.selectbox("Select Time Frame", ["month", "week","day"])
start_date = st.date_input("Start Date", value=pd.to_datetime("2023-12-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2025-06-30"))

# --- Helper function for date truncation based on timeframe ---
def truncate_date(date_col, timeframe):
    if timeframe == "day":
        return f"block_timestamp::date"
    elif timeframe == "week":
        return f"date_trunc('week', block_timestamp)"
    elif timeframe == "month":
        return f"date_trunc('month', block_timestamp)"
    else:
        return "block_timestamp::date"

date_col = truncate_date("block_timestamp", timeframe)

# --- Query Functions ---------------------------------------------------------------------------------------
@st.cache_data
def load_ai_transfer_kpis(start_date, end_date):
    query = f"""
        WITH tab2 AS (
            WITH tab1 AS (
                SELECT 
                    created_at AS block_timestamp,
                    id AS tx_id,
                    data:call.transaction.from::STRING AS sender_address,
                    data:call.returnValues.destinationContractAddress::STRING AS receiver_address,
                    data:amount::FLOAT AS token_amount,
                    (TRY_CAST(data:value::float AS FLOAT)) AS transfers_volume_usd,
                    TRY_CAST(data:fees:express_fee_usd::float AS FLOAT) AS transfer_fee,
                    data:symbol::STRING AS token_symbol,
                    data:call.chain::STRING AS source_chain,
                    data:call.returnValues.destinationChain::STRING AS destination_chain
                FROM axelar.axelscan.fact_gmp
            )
            SELECT block_timestamp, tx_id, sender_address, receiver_address, token_amount,
                CASE 
                    WHEN transfers_volume_usd IS NULL AND date_trunc('month', block_timestamp) = '2023-12-01 00:00:00.000'
                        THEN token_amount * 0.00000165
                    WHEN transfers_volume_usd IS NULL AND date_trunc('month', block_timestamp) = '2023-01-01 00:00:00.000'
                        THEN token_amount * 0.00000055
                    WHEN transfers_volume_usd IS NULL AND date_trunc('month', block_timestamp) = '2023-02-01 00:00:00.000'
                        THEN token_amount * 0.00000145
                    WHEN transfers_volume_usd IS NULL AND date_trunc('month', block_timestamp) = '2023-03-01 00:00:00.000'
                        THEN token_amount * 0.00000202
                    ELSE transfers_volume_usd 
                END AS transfers_volume_usd,
                transfer_fee, token_symbol, source_chain, destination_chain
            FROM tab1
        )
        SELECT 
            COUNT(DISTINCT tx_id) AS "Number of Transfers",
            COUNT(DISTINCT sender_address) AS "Number of Users",
            ROUND(SUM(token_amount), 2) AS "Volume of Transfers ($AI)",
            ROUND(SUM(transfers_volume_usd), 2) AS "Volume of Transfers ($USD)",
            ROUND(MEDIAN(transfers_volume_usd), 2) AS "Median Volume of Transfers ($USD)",
            ROUND(SUM(transfer_fee), 2) AS "Total Transfer Fees ($USD)",
            ROUND(Median(transfer_fee), 2) AS "Median Transfer Fees ($USD)",
            COUNT(DISTINCT (source_chain || '➡' || destination_chain)) AS "Number of Paths"
        FROM tab2
        WHERE token_symbol = 'AI'
          AND block_timestamp::date >= '{start_date}'
          AND block_timestamp::date <= '{end_date}'
    """
    return pd.read_sql(query, conn).iloc[0]


# --- Load Data ----------------------------------------------------------------------------------------
ai_transfer_kpis = load_ai_transfer_kpis(start_date, end_date)

# --- Row Data ------------------------------------------------------------------------------------------

# --- Row 1: Metrics ---
kpi_cols = st.columns(4)
kpi_cols[0].metric("🚀Number of Transfers", f"{ai_transfer_kpis['Number of Transfers']:,}")
kpi_cols[1].metric("👥Number of Users", f"{ai_transfer_kpis['Number of Users']:,}")
kpi_cols[2].metric("🔵Volume of Transfers ($AI)", f"{ai_transfer_kpis['Volume of Transfers ($AI)']:,}")
kpi_cols[3].metric("💰Volume of Transfers ($USD)", f"${ai_transfer_kpis['Volume of Transfers ($USD)']:,}")

kpi_cols2 = st.columns(4)
kpi_cols2[0].metric("📊Median Volume of Transfers ($USD)", f"${ai_transfer_kpis['Median Volume of Transfers ($USD)']:,}")
kpi_cols2[1].metric("⛽Total Transfer Fees ($USD)", f"${ai_transfer_kpis['Total Transfer Fees ($USD)']:,}")
kpi_cols2[2].metric("💨Median Transfer Fees ($USD)", f"${ai_transfer_kpis['Median Transfer Fees ($USD)']:,}")
kpi_cols2[3].metric("🔀Number of Paths", f"{ai_transfer_kpis['Number of Paths']:,}")
