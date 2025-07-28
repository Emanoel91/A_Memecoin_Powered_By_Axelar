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
    
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="https://pbs.twimg.com/profile_images/1841479747332608000/bindDGZQ_400x400.jpg" alt="Eman Raz" style="width:25px; height:25px; border-radius: 50%;">
            <span>Built by: <a href="https://x.com/0xeman_raz" target="_blank">Eman Raz</a></span>
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
            <a href="https://www.axelar.network/" target="_blank">Axelar Website</a>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="https://axelarscan.io/logos/logo.png" alt="Axelar" style="width:20px; height:20px;">
            <a href="https://interchain.axelar.dev/" target="_blank">Interchain Token Service (ITS)</a>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="https://axelarscan.io/logos/logo.png" alt="Axelar" style="width:20px; height:20px;">
            <a href="https://x.com/axelar" target="_blank">Axelar X Account</a>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="https://raw.githubusercontent.com/axelarnetwork/axelar-configs/main/images/tokens/ai.svg" alt="AnyInu" style="width:20px; height:20px;">
            <a href="https://www.anyinu.xyz/" target="_blank">AnyInu Website</a>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="https://raw.githubusercontent.com/axelarnetwork/axelar-configs/main/images/tokens/ai.svg" alt="AnyInu" style="width:20px; height:20px;">
            <a href="https://x.com/AnyInuCoin" target="_blank">AnyInu X Account</a>
        </div>
        
    </div>
    """,
    unsafe_allow_html=True
)
