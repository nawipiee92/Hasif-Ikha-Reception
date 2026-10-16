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
    """
    <style>
    .main {
        background-color: #f5f6f8;
    }
    .title-text {
        text-align: center;
        font-family: 'Ink Free', cursive, sans-serif;
        font-size: 28px;
        font-weight: bold;
        color: #4a235a;
    }
    .welcome-text {
        text-align: center;
        font-size: 14px;
        font-weight: bold;
        color: #7f8c8d;
        letter-spacing: 2px;
        margin-top: 20px;
    }
    .guest-name {
        text-align: center;
        font-family: 'Century Gothic', sans-serif;
        font-size: 24px;
        font-weight: bold;
        color: #1a1a2e;
        margin-top: 10px;
    }
    .message-text {
        text-align: center;
        font-size: 14px;
        color: #555555;
        margin-top: 10px;
    }
    .table-text {
        text-align: center;
        font-size: 26px;
        font-weight: bold;
        color: #c70039;
        margin-top: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- APP UI ---
st.markdown(
    '<div class="title-text">✦ Hasif & Ikha Reception ✦</div>',
    unsafe_allow_html=True,
)
st.markdown(
    "<div style='text-align: center; color: #4a235a;'>══════════════════</div>",
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
            [f"• <b>{m['guest']}</b> -> {m['table']}" for m in matches]
        )
        st.markdown(
            f'<div style="text-align: center; color: #c70039;'
            f' font-size:16px;">{results_list}</div>',
            unsafe_allow_html=True,
        )
        st.info('Please check the list above for the correct name.')

  # --- IMAGES SECTION ---
  st.write('')
  col1, col2 = st.columns(2)
  with col1:
    if os.path.exists('123.png'):
      st.image('123.png', use_container_width=True)
  with col2:
    if os.path.exists('234.png'):
      st.image('234.png', use_container_width=True)
