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

# --- CUSTOM CSS STYLING FOR MOBILE RESPONSIVENESS & CARD WRAPPER ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* Center Card Container */
    .main-card {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 25px 20px;
        border-radius: 20px;
        box-shadow: 0px 4px 25px rgba(0,0,0,0.15);
        max-width: 480px;
        margin: 20px auto;
    }}

    .title-text {{
        text-align: center;
        font-family: 'Ink Free', cursive, sans-serif;
        font-size: 24px;
        font-weight: bold;
        color: #4a235a;
    }}
    .welcome-text {{
        text-align: center;
        font-size: 13px;
        font-weight: bold;
        color: #7f8c8d;
        letter-spacing: 2px;
        margin-top: 20px;
    }}
    .guest-name {{
        text-align: center;
        font-family: 'Century Gothic', sans-serif;
        font-size: 20px;
        font-weight: bold;
        color: #1a1a2e;
        margin-top: 8px;
        word-break: break-word;
    }}
    .message-text {{
        text-align: center;
        font-size: 13px;
        color: #555555;
        margin-top: 8px;
    }}
    .table-text {{
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #c70039;
        margin-top: 12px;
    }}
    
    /* Mobile optimization for buttons and inputs */
    @media (max-width: 600px) {{
        .main-card {{
            padding: 15px 10px;
            margin: 10px;
        }}
        .title-text {{
            font-size: 20px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- START OF WHITE BOX CONTAINER ---
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Title & Divider INSIDE the white box
st.markdown(
    '<div class="title-text">✦ Hasif & Ikha Reception ✦</div>',
    unsafe_allow_html=True,
)
st.markdown(
    "<div style='text-align: center; color: #4a235a; margin-bottom: 15px;'>══════════════════</div>",
    unsafe_allow_html=True,
)

if df_raw is None:
  st.error(
      'Could not find "names.xlsx". Make sure it is uploaded in your GitHub'
      ' repository!'
  )
else:
  # Search input field
  query = st.text_input(
      'Enter Guest Name:', placeholder='Type guest name here...'
  ).strip().lower()

  if st.button('Find Table ✨', use_container_width=True):
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
        st.markdown(
            '<div class="welcome-text">— W E L C O M E —</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="guest-name">{matches[0]["guest"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="message-text">We are overjoyed to celebrate our'
            ' special day with you! 💕</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="table-text">⭐ {matches[0]["table"]} ⭐</div>',
            unsafe_allow_html=True,
        )
      else:
        st.markdown(
            '<div class="welcome-text">— MULTIPLE GUESTS FOUND —</div>',
            unsafe_allow_html=True,
        )
        results_list = '<br>'.join(
            [f"• <b>{m['guest']}</b> -> <span style='color: #c70039;'>{m['table']}</span>" for m in matches]
        )
        st.markdown(
            f'<div style="text-align: center; color: #1a1a2e;'
            f' font-size:15px; margin-top: 10px;">{results_list}</div>',
            unsafe_allow_html=True,
        )
        st.info('Please check the list above for the correct name.')

  # --- SIDE-BY-SIDE IMAGES SECTION INSIDE THE BOX ---
  st.write('')
  col1, col2 = st.columns(2)
  with col1:
    if os.path.exists('123.png'):
      st.image('123.png', use_container_width=True)
  with col2:
    if os.path.exists('234.png'):
      st.image('234.png', use_container_width=True)

# --- END OF WHITE BOX CONTAINER ---
st.markdown('</div>', unsafe_allow_html=True)
