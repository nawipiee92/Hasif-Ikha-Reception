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

# --- CUSTOM CSS STYLING ---
st.markdown(
    f"""
    <style>
    /* Remove default Streamlit top header whitespace and pull everything right to the top */
    header, [data-testid="stHeader"] {{
        display: none !important;
        height: 0px !important;
    }}
    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 2rem !important;
        margin-top: -20px !important;
    }}

    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* Main Content Container Card */
    .main-card {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 20px 15px;
        border-radius: 20px;
        box-shadow: 0px 4px 25px rgba(0,0,0,0.15);
        max-width: 480px;
        margin: 0 auto;
    }}

    /* Larger & Prominent Title Box brought further up */
    .title-box {{
        background-color: #ffffff;
        border: 1.5px solid #e0e0e0;
        padding: 16px 20px;
        border-radius: 50px;
        text-align: center;
        box-shadow: 0px 3px 15px rgba(0,0,0,0.1);
        margin-bottom: 18px;
    }}

    .title-text {{
        font-family: 'Ink Free', cursive, sans-serif;
        font-size: 27px;
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

    /* Full side-by-side images without cropping */
    .stImage img {{
        border-radius: 12px;
        object-fit: contain !important;
        width: 100% !important;
        height: auto !important;
    }}

    @media (max-width: 480px) {{
        .main-card {{
            padding: 15px 10px;
            border-radius: 15px;
        }}
        .title-text {{
            font-size: 23px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- START OF MAIN WHITE CARD BOX ---
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Larger Title Box brought up
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

  # --- SIDE-BY-SIDE FULL IMAGES SECTION ---
  st.write('')
  col1, col2 = st.columns(2)
  with col1:
    if os.path.exists('123.png'):
      st.image('123.png', use_container_width=True)
  with col2:
    if os.path.exists('234.png'):
      st.image('234.png', use_container_width=True)

# --- END OF MAIN WHITE CARD BOX ---
st.markdown('</div>', unsafe_allow_html=True)
