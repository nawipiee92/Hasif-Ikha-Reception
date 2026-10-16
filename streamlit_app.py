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

# --- CUSTOM DESIGN & BACKGROUND STYLING ---
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("FBorder.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    
    /* Cloud Card Container styling */
    .cloud-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 35px 25px;
        border-radius: 40px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.15);
        text-align: center;
        max-width: 600px;
        margin: 40px auto;
    }
    
    .title-text {
        font-family: 'Segoe UI', sans-serif;
        font-size: 22px;
        font-weight: bold;
        color: #4a235a;
        margin-bottom: 20px;
    }
    
    .welcome-text {
        font-family: 'Segoe UI', sans-serif;
        font-size: 15px;
        font-weight: bold;
        color: #7f8c8d;
        margin-top: 20px;
        letter-spacing: 2px;
    }
    
    .guest-name {
        font-family: 'Segoe UI', sans-serif;
        font-size: 20px;
        font-weight: bold;
        color: #1a1a2e;
        margin: 12px 0;
    }
    
    .msg-text {
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
        color: #555555;
        margin-bottom: 15px;
    }
    
    .table-badge {
        font-family: 'Segoe UI', sans-serif;
        font-size: 26px;
        font-weight: bold;
        color: #c70039;
        margin-top: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- APP LAYOUT & INTERACTIVE SEARCH ---
st.markdown('<div class="cloud-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="title-text">✦ Hasif & Ikha Reception ✦</div>',
    unsafe_allow_html=True,
)

if df is None:
  st.error(
      '⚠️ Could not find "names.xlsx". Make sure it is uploaded alongside your'
      ' app!'
  )
else:
  # Search input box for guests to type their name
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