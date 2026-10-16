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

# --- CUSTOM CSS MATCHING YOUR EXACT DESKTOP APP DESIGN ---
st.markdown(
    """
    <style>
    /* Force full-screen floral background using direct GitHub raw image link */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/nawipiee92/Hasif-Ikha-Reception/main/FBorder.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    
    /* Hide Streamlit header/footer elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Adjust spacing at the top to center the card nicely */
    .block-container {
        padding-top: 4rem;
        max-width: 750px;
    }

    /* Single Clean White Cloud Card Container */
    .cloud-card {
        background-color: #ffffff;
        padding: 45px 35px;
        border-radius: 35px;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.25);
        text-align: center;
        margin: auto;
    }
    
    .title-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 24px;
        font-weight: bold;
        color: #4a235a;
        margin-bottom: 20px;
    }
    
    .welcome-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 15px;
        font-weight: bold;
        color: #7f8c8d;
        margin-top: 20px;
        letter-spacing: 1px;
    }
    
    .guest-name {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 24px;
        font-weight: bold;
        color: #1a1a2e;
        margin: 10px 0;
    }
    
    .msg-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 13px;
        color: #555555;
        margin-bottom: 15px;
    }
    
    .table-badge {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 30px;
        font-weight: bold;
        color: #c70039;
        margin-top: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- APP LAYOUT ---
st.markdown('<div class="cloud-card">', unsafe_allow_html=True)

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
  # Search input box neatly inside the cloud card
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
