import os
import pandas as pd
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title='Hasif & Ikha Reception 🌸', page_icon='🌸', layout='centered'
)

# --- LOAD EXCEL FILE ---
@st.cache_data
def load_data():
  if os.path.exists('names.xlsx'):
    return pd.read_excel('names.xlsx')
  return None


df = load_data()

# --- CUSTOM CSS FOR FROSTED GLASS CARD & STYLING ---
st.markdown(
    """
    <style>
    /* Import Ink Free & Century Gothic fonts */
    @import url('https://fonts.googleapis.com/css2?family=Century+Gothic&display=swap');

    /* Portrait mobile wallpaper scaling for Border.png */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/nawipiee92/Hasif-Ikha-Reception/main/Border.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Hide Streamlit header/footer elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Container alignment and phone-compatible width */
    .block-container {
        padding-top: 15vh;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
        max-width: 420px;
        text-align: center;
    }
    
    /* Frosted Blue-White Translucent Glass Box for Title & Search */
    .glass-card {
        background-color: rgba(240, 244, 248, 0.85);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 20px;
        padding: 25px 20px;
        box-shadow: 0px 8px 32px rgba(74, 35, 90, 0.12);
        margin-bottom: 25px;
    }
    
    /* Search bar alignment */
    .stTextInput {
        text-align: center;
        margin: 0 auto;
    }
    
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        text-align: center;
        box-shadow: inset 0px 2px 4px rgba(0,0,0,0.06);
    }

    /* Title Header styling */
    .title-text {
        font-family: 'Ink Free', cursive, sans-serif;
        font-size: clamp(22px, 5vw, 28px);
        font-weight: bold;
        color: #4a235a;
        margin-bottom: 2px;
        text-align: center;
        white-space: nowrap;
    }
    
    /* Clean professional double underline HTML element */
    .double-underline {
        border-top: 2px solid #4a235a;
        border-bottom: 1px solid #4a235a;
        height: 3px;
        width: 70%;
        margin: 8px auto 18px auto;
    }
    
    .welcome-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 13px;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 15px;
        letter-spacing: 1.5px;
        text-align: center;
        text-shadow: -1px -1px 0 #ffffff, 1px -1px 0 #ffffff, -1px 1px 0 #ffffff, 1px 1px 0 #ffffff;
    }
    
    /* Guest name using Century Gothic with outline */
    .guest-name {
        font-family: 'Century Gothic', sans-serif;
        font-size: clamp(22px, 6vw, 27px);
        font-weight: bold;
        color: #1a1a2e;
        margin: 10px 0;
        text-align: center;
        text-shadow: -1px -1px 0 #ffffff, 1px -1px 0 #ffffff, -1px 1px 0 #ffffff, 1px 1px 0 #ffffff, 0px 2px 4px rgba(0,0,0,0.20);
    }
    
    .msg-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 13px;
