import streamlit as st

# --- Page Config: Tab Title & Icon ---
st.set_page_config(
    page_title="Any Inu: A Memecoin Powered By Axelar",
    page_icon="https://raw.githubusercontent.com/axelarnetwork/axelar-configs/main/images/tokens/ai.svg",
    layout="wide"
)

# --- Title with Logo ---------------------------------------------------------------------------------------------------
st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 15px;">
        <img src="https://raw.githubusercontent.com/axelarnetwork/axelar-configs/main/images/tokens/ai.svg" alt="Any Inu Logo" style="width:60px; height:60px;">
        <h1 style="margin: 0;">Any Inu: A Memecoin Powered By Axelar</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Display Image ------------------------------------------------------------------------------------------------------
st.image(
    "https://pbs.twimg.com/profile_banners/1739891504255025152/1709784887/1500x500",
    use_container_width=True
)

st.markdown("""
Any Inu ($AI) is an omnichain meme token powered by Axelar's Interchain Token Service.
""")

# --- Links with Logos ---
# st.markdown("### Official Links")

links = [
    {
        "logo": "https://axelarscan.io/logos/logo.png",
        "url": "https://www.axelar.network/",
        "label": "Axelar Network"
    },
    {
        "logo": "https://raw.githubusercontent.com/axelarnetwork/axelar-configs/main/images/tokens/ai.svg",
        "url": "https://www.anyinu.xyz/",
        "label": "Any Inu Official Website"
    },
    {
        "logo": "https://upload.wikimedia.org/wikipedia/commons/5/53/X_logo_2023_original.svg",
        "url": "https://x.com/axelar",
        "label": "Axelar on X"
    },
    {
        "logo": "https://upload.wikimedia.org/wikipedia/commons/5/53/X_logo_2023_original.svg",
        "url": "https://x.com/AnyInucoin",
        "label": "Any Inu on X"
    }
]

for link in links:
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.image(link["logo"], width=30)
    with col2:
        st.markdown(f"[{link['label']}]({link['url']})")
