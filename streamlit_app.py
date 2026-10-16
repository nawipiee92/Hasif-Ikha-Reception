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

# --- CUSTOM CSS: MOBILE-OPTIMIZED FULL BORDER & CENTERED TEXT ---
st.markdown(
    """
    <style>
    /* Force full-screen background that stretches to fit mobile and desktop screens perfectly */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/nawipiee92/Hasif-Ikha-Reception/main/FBorder.png");
        background-size: 100% 100%;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Hide Streamlit header/footer elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive layout padding to keep everything neatly inside the frame on mobile */
    .block-container {
        padding-top: 15vh;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 600px;
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
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }

    /* Custom Centered Text Styling */
    .title-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: clamp(20px, 5vw, 26px);
        font-weight: bold;
        color: #4a235a;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .welcome-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: clamp(14px, 4vw, 16px);
        font-weight: bold;
        color: #7f8c8d;
        margin-top: 25px;
        letter-spacing: 1px;
        text-align: center;
    }
    
    .guest-name {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: clamp(22px, 6vw, 28px);
        font-weight: bold;
        color: #1a1a2e;
        margin: 10px 0;
        text-align: center;
    }
    
    .msg-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: clamp(12px, 3.5vw, 14px);
        color: #555555;
        margin-bottom: 15px;
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
  # Search input box centered on mobile/desktop
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
