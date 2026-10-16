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
        background-color: rgba(240, 244, 248, 0.88);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.7);
        border-radius: 20px;
        padding: 25px 20px;
        box-shadow: 0px 8px 32px rgba(74, 35, 90, 0.15);
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
        color: #333333;
        font-weight: 600;
        margin-bottom: 12px;
        text-align: center;
        text-shadow: -1px -1px 0 #ffffff, 1px -1px 0 #ffffff, -1px 1px 0 #ffffff, 1px 1px 0 #ffffff;
    }
    
    .table-badge {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: clamp(26px, 7vw, 34px);
        font-weight: bold;
        color: #c70039;
        margin-top: 15px;
        text-align: center;
        text-shadow: -1px -1px 0 #ffffff, 1px -1px 0 #ffffff, -1px 1px 0 #ffffff, 1px 1px 0 #ffffff, 0px 2px 6px rgba(0,0,0,0.25);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- APP LAYOUT ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown(
    '<div class="title-text">✦ Hasif & Ikha Reception ✦</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="double-underline"></div>', unsafe_allow_html=True)

if df is None:
  st.error(
      '⚠️ Could not find "names.xlsx". Make sure it is uploaded in your GitHub'
      ' repository!'
  )
else:
  # Search input box centered for portrait view
  query = st.text_input(
      '', placeholder='Type your name here...', label_visibility='collapsed'
  )
st.markdown('</div>', unsafe_allow_html=True)

# --- RESULTS SECTION ---
if 'query' in locals() and query:
  query_clean = query.strip().lower()
  results = df[
      df['Name'].astype(str).str.lower().str.contains(query_clean, na=False)
  ]

  if results.empty:
    st.markdown(
        '<div class="welcome-text" style="color: #c70039;">❌ Guest not'
        ' found</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="msg-text">Please check your spelling and try again.</div>',
        unsafe_allow_html=True,
    )
  else:
    row = results.iloc[0]
    guest_name = row['Name']
    table_no = row['Table No.']

    st.markdown(
        '<div class="welcome-text">— W E L C O M E —</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="guest-name">✨ {guest_name} ✨</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="msg-text">We are overjoyed to celebrate our special day with'
        ' you! 💕</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="table-badge">⭐ Table {table_no} ⭐</div>',
        unsafe_allow_html=True,
    )
