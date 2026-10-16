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

# --- CUSTOM CSS FOR STYLING ---
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
    
    /* Custom Title Header Container */
    .title-card {
        background-color: rgba(255, 255, 255, 0.90);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 20px 20px 0px 0px;
        padding: 22px 15px 8px 15px;
        box-shadow: 0px -5px 20px rgba(74, 35, 90, 0.10);
        text-align: center;
    }

    /* Title Header styling - forced to single line with responsive sizing */
    .title-text {
        font-family: 'Ink Free', cursive, sans-serif;
        font-size: clamp(20px, 4.8vw, 26px);
        font-weight: bold;
        color: #4a235a;
        margin-bottom: 2px;
        text-align: center;
        white-space: nowrap;
        display: block;
        width: 100%;
    }
    
    /* Clean professional double underline */
    .double-underline {
        border-top: 2px solid #4a235a;
        border-bottom: 1px solid #4a235a;
        height: 3px;
        width: 75%;
        margin: 6px auto 12px auto;
    }

    /* Make the search input wrapper blend seamlessly underneath the title card */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.90) !important;
        border-top: none !important;
        border-radius: 0px 0px 20px 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0px 8px 25px rgba(74, 35, 90, 0.15);
        padding: 5px 15px 15px 15px !important;
        margin-top: -10px;
    }
    
    .welcome-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 13px;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 20px;
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
        margin: 8px 0;
        text-align: center;
        text-shadow: -1px -1px 0 #ffffff, 1px -1px 0 #ffffff, -1px 1px 0 #ffffff, 1px 1px 0 #ffffff, 0px 2px 4px rgba(0,0,0,0.20);
    }
    
    .msg-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 13px;
        color: #333333;
        font-weight: 600;
        margin-bottom: 10px;
        text-align: center;
        text-shadow: -1px -1px 0 #ffffff, 1px -1px 0 #ffffff, -1px 1px 0 #ffffff, 1px 1px 0 #ffffff;
    }
    
    .table-badge {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: clamp(26px, 7vw, 34px);
        font-weight: bold;
        color: #c70039;
        margin-top: 10px;
        text-align: center;
        text-shadow: -1px -1px 0 #ffffff, 1px -1px 0 #ffffff, -1px 1px 0 #ffffff, 1px 1px 0 #ffffff, 0px 2px 6px rgba(0,0,0,0.25);
    }

    /* Beautiful rounded styling for the bottom images */
    .bottom-images-container {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-top: 25px;
        margin-bottom: 20px;
    }
    
    .bottom-images-container img {
        width: 46%;
        max-height: 160px;
        object-fit: cover;
        border-radius: 18px;
        border: 2px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0px 6px 20px rgba(74, 35, 90, 0.20);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- APP LAYOUT ---
st.markdown(
    """
    <div class="title-card">
        <div class="title-text">✦ Hasif & Ikha Reception ✦</div>
        <div class="double-underline"></div>
    </div>
""",
    unsafe_allow_html=True,
)

if df is None:
  st.error(
      '⚠️ Could not find "names.xlsx". Make sure it is uploaded in your GitHub'
      ' repository!'
  )
  query = ''
else:
  query = st.text_input(
      '', placeholder='Type your name here...', label_visibility='collapsed'
  )

# --- RESULTS SECTION ---
if query:
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

# --- BOTTOM DECORATIVE IMAGES (123.png & 234.png) ---
st.markdown(
    """
    <div class="bottom-images-container">
        <img src="https://raw.githubusercontent.com/nawipiee92/Hasif-Ikha-Reception/main/123.png" alt="Reception Photo 1">
        <img src="https://raw.githubusercontent.com/nawipiee92/Hasif-Ikha-Reception/main/234.png" alt="Reception Photo 2">
    </div>
""",
    unsafe_allow_html=True,
)
