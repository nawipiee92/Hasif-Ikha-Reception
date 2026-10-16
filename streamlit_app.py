import os
import pandas as pd
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title='Hasif & Ikha Reception 🌸!', page_icon='🌸', layout='centered'
)

# --- LOAD EXCEL FILE ---
@st.cache_data
def load_data():
  if os.path.exists('names.xlsx'):
    return pd.read_excel('names.xlsx')
  return None


df = load_data()

# --- CUSTOM CSS: PORTRAIT MOBILE-FRIENDLY BACKGROUND ---
st.markdown(
    """
    <style>
    /* Portrait mobile wallpaper scaling for the floral border */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/nawipiee92/Hasif-Ikha-Reception/main/FBorder.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Hide Streamlit header/footer elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Perfect vertical centering for portrait mobile screens */
    .block-container {
        padding-top: 18vh;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
        max-width: 550px;
        text-align: center;
    }
    
    /* Center search bar nicely with subtle background */
    .stTextInput {
        text-align: center;
        margin: 0 auto;
    }
    
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
    }

    /* Custom Centered Text Styling */
    .title-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: clamp(22px, 5.5vw, 28px);
        font-weight: bold;
        color: #4a235a;
        margin-bottom: 25px;
        text-align: center;
    }
    
    .welcome-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: clamp(14px, 4vw, 16px);
        font-weight: bold;
        color: #7f8c8d;
        margin-top: 30px;
        letter-spacing: 1px;
        text-align: center;
    }
    
    .guest-name {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: clamp(24px, 6.5vw, 30px);
        font-weight: bold;
        color: #1a1a2e;
        margin: 12px 0;
        text-align: center;
    }
    
    .msg-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: clamp(13px, 3.8vw, 15px);
        color: #555555;
        margin-bottom: 15px;
        text-align: center;
    }
    
    .table-badge {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: clamp(28px, 7.5vw, 36px);
        font-weight: bold;
        color: #c70039;
        margin-top: 15px;
        text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- APP LAYOUT ---
st.markdown(
    '<div class="title-text">✦ Hasif & Ikha Reception ✦</div>',
    unsafe_allow_html=True,
)

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
