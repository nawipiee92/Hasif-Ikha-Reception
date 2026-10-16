import base64
import os
import pandas as pd
from PIL import Image, ImageOps
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title='Hasif & Ikha Reception 🌸',
    page_icon='🌸',
    layout='centered',
)

# --- FUNCTION TO CONVERT IMAGE TO BASE64 FOR CSS BACKGROUND ---
def get_base64_image(image_path):
  if os.path.exists(image_path):
    with open(image_path, 'rb') as f:
      data = f.read()
    return base64.b64encode(data).decode()
  return ''

bg_base64 = get_base64_image('Border.png')

# --- LOAD EXCEL FILE SAFELY ---
@st.cache_data
def load_data():
  try:
    return pd.read_excel('names.xlsx', header=None)
  except Exception as e:
    return None

df_raw = load_data()

# --- CUSTOM CSS STYLING (Mobile optimized & clean header layout) ---
st.markdown(
    f"""
    <style>
    /* Remove default Streamlit top header whitespace */
    header, [data-testid="stHeader"] {{
        display: none !important;
        height: 0px !important;
    }}
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }}

    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* Main Content Container Card - perfectly centered and mobile friendly */
    .main-card {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 20px 15px;
        border-radius: 20px;
        box-shadow: 0px 4px 25px rgba(0,0,0,0.15);
        max-width: 480px;
        margin: 0 auto;
    }}

    /* Single Clean Title Box */
    .title-box {{
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 10px 15px;
        border-radius: 50px;
        text-align: center;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }}

    .title-text {{
        font-family: 'Ink Free', cursive, sans-serif;
        font-size: 20px;
        font-weight: bold;
        color: #4a235a;
        margin: 0;
    }}
    
    .welcome-text {{
        text-align: center;
        font-size: 13px;
        font-weight: bold;
        color: #7f8c8d;
        letter-spacing: 2px;
        margin-top: 15px;
    }}
    .guest-name {{
        text-align: center;
        font-family: 'Century Gothic', sans-serif;
        font-size: 18px;
        font-weight: bold;
        color: #1a1a2e;
        margin-top: 6px;
        word-break: break-word;
    }}
    .message-text {{
        text-align: center;
        font-size: 12px;
        color: #555555;
        margin-top: 6px;
    }}
    .table-text {{
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: #c70039;
        margin-top: 10px;
    }}

    /* Extra responsive styling for small mobile screens */
    @media (max-width: 480px) {{
        .main-card {{
            padding: 15px 10px;
            border-radius: 15px;
        }}
        .title-text {{
            font-size: 18px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- START OF MAIN WHITE CARD BOX ---
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Title neatly inside a single clean container box
st.markdown(
    """
    <div class="title-box">
        <div class="title-text">✦ Hasif & Ikha Reception ✦</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if df_raw is None:
  st.error(
      'Could not find "names.xlsx". Make sure it is uploaded in your GitHub'
      ' repository!'
  )
else:
  # Form allowing search via pressing Enter or clicking button
  with st.form(key='search_form'):
    query = st.text_input(
        'Enter Guest Name:', placeholder='Type guest name here...'
    ).strip().lower()
    
    submit_button = st.form_submit_button('Find Seating ✨', use_container_width=True)

  if submit_button:
    if not query:
      st.warning('Please enter a name to search.')
    else:
      matches = []
      current_table = 'TABLE VIP Z1'

      # Scan through the Excel rows
      for index, row in df_raw.iterrows():
        row_str_values = [str(val).strip() for val in row.values if pd.notna(val)]

        # Update table header if found
        for val in row_str_values:
          if 'table' in val.lower():
            current_table = val
            break

        # Check cells for matching guest name
        for val in row.values:
          if pd.notna(val):
            cell_text = str(val).strip()
            cell_lower = cell_text.lower()
            if (
                query in cell_lower
                and 'table' not in cell_lower
                and cell_lower != 'no'
            ):
              if not any(
                  m['guest'] == cell_text and m['table'] == current_table
                  for m in matches
              ):
                matches.append({'guest': cell_text, 'table': current_table})

      if not matches:
        st.markdown(
            '<div class="welcome-text" style="color: #c70039;">❌ Guest not'
            ' found</div>',
            unsafe_allow_html=True,
        )
        st.info('Please check the spelling and try again.')
      elif len(matches) == 1:
        st.
