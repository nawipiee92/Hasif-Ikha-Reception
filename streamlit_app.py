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

# --- CUSTOM CSS FOR STYLING & BORDER.PNG ---
st.markdown(
    """
    <style>
    /* Import Ink Free font */
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
    
    /* Center container layout */
    .block-container {
        padding-top: 15vh;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 500px;
        text-align: center;
    }
    
    /* Frosted see-through glass card box */
    .card-box {
        background-color: rgba(245, 246, 248, 0.90);
        padding: 30px 20px;
        border-radius: 16px;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
        text-align: center;
    }
    
    /* Search bar alignment */
    .stTextInput {
        text-align: center;
        margin: 0 auto;
    }
    
    div[data-baseweb="input"] {
        background-color: #ffffff;
        border-radius: 10px;
        text-align: center;
        box-shadow: inset 0px 2px 4px rgba(0,0,0,0.06);
    }

    /* Title Header */
    .title-text {
        font-family: 'Ink Free', cursive, sans-serif;
        font-size: clamp(24px, 6vw, 32px);
        font-weight: bold;
        color: #4a235a;
        margin-bottom: 5px;
        text-align: center;
    }
    
    .underline {
        color: #4a235a;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 20px;
        font-size: 14px;
    }
    
    .welcome-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 14px;
        font-weight: bold;
        color: #7f8c8d;
        margin-top: 20px;
        letter-spacing: 1.5px;
        text-align: center;
    }
    
    /* Guest name using Century Gothic */
    .guest-name {
        font-family: 'Century Gothic', sans-serif;
        font-size: clamp(22px, 6vw, 28px);
        font-weight: bold;
        color: #1a1a2e;
        margin: 10px 0;
        text-align: center;
    }
    
    .msg-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 13px;
        color: #555555;
        margin-bottom: 12px;
        text-align: center;
    }
    
    .table-badge {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: clamp(26px, 7vw, 34px);
        font-weight: bold;
        color: #c70039;
        margin-top: 15px;
        text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- APP CONTAINER ---
st.markdown('<div class="card-box">', unsafe_allow_html=True)

st.markdown(
    '<div class="title-text">✦ Hasif & Ikha Reception ✦</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="underline">══════════════════</div>', unsafe_allow_html=True)

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
          '<div class="msg-text">Please check your spelling and try'
          ' again.</div>',
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
          '<div class="msg-text">We are overjoyed to celebrate our special day'
          ' with you! 💕</div>',
          unsafe_allow_html=True,
      )
      st.markdown(
          f'<div class="table-badge">⭐ Table {table_no} ⭐</div>',
          unsafe_allow_html=True,
      )

st.markdown('</div>', unsafe_allow_html=True)
