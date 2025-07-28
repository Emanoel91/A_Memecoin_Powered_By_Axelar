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

# --- Info Box --------------------------------------------------------------------------------------------------------------
st.markdown(
    """
    <div style="background-color: #11caff; padding: 15px; border-radius: 10px; border: 1px solid #11caff;">
        Any Inu is powered by Axelar’s Interchain Token Service, which enables native interoperability across blockchains. 
        Axelar’s decentralized network and proof-of-stake consensus ensure secure cross-chain communication, eliminating the 
        need for wrapped tokens (common in traditional bridges) and reducing risks. Axelar’s ecosystem supports Any Inu’s presence 
        on multiple chains, enhancing its scalability and accessibility in the Web3 space.
    </div>
    """,
    unsafe_allow_html=True
)

# --- Reference and Rebuild Info --------------------------------------------------------------------------------------
st.markdown(
    """
    <div style="margin-top: 20px; margin-bottom: 20px; font-size: 16px;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
            <img src="https://cdn-icons-png.flaticon.com/512/3178/3178287.png" alt="Reference" style="width:20px; height:20px;">
            <span>Dashboard Reference: <a href="https://flipsidecrypto.xyz/Sniper/axelar-staking-NU6QUG" target="_blank">https://flipsidecrypto.xyz/Sniper/axelar-staking-NU6QUG/</a></span>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="https://pbs.twimg.com/profile_images/1841479747332608000/bindDGZQ_400x400.jpg" alt="Eman Raz" style="width:25px; height:25px; border-radius: 50%;">
            <span>Rebuilt by: <a href="https://x.com/0xeman_raz" target="_blank">Eman Raz</a></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Links with Logos ---------------------------------------------------------------------------------------
st.markdown(
    """
    <div style="font-size: 16px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="https://axelarscan.io/logos/logo.png" alt="Axelar" style="width:20px; height:20px;">
            <a href="https://www.axelar.network/" target="_blank">https://www.axelar.network/</a>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="https://cdn-icons-png.flaticon.com/512/5968/5968958.png" alt="X" style="width:20px; height:20px;">
            <a href="https://x.com/axelar" target="_blank">https://x.com/axelar</a>
        </div>
        
    </div>
    """,
    unsafe_allow_html=True
)
