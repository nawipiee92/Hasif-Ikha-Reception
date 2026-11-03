import base64
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title='Hasif & Ikha Reception 🌸', page_icon='🌸', layout='centered')

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return ''

bg_base64 = get_base64_image('Border.png')

@st.cache_data
def load_data():
    try:
        return pd.read_excel('names.xlsx', header=None)
    except:
        return None

df_raw = load_data()

st.markdown(f"""
    <style>
    header, [data-testid="stHeader"] {{ display: none !important; height: 0px !important; }}
    .block-container {{ padding-top: 0rem !important; padding-bottom: 2rem !important; margin-top: -20px !important; }}
    .stApp {{ background-image: url("data:image/png;base64,{bg_base64}"); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed; }}
    .main-card {{ background-color: rgba(255, 255, 255, 0.95); padding: 20px 15px; border-radius: 20px; box-shadow: 0px 4px 25px rgba(0,0,0,0.15); max-width: 520px; margin: 0 auto; }}
    .title-box {{ background-color: #ffffff; border: 1.5px solid #e0e0e0; padding: 16px 20px; border-radius: 50px; text-align: center; box-shadow: 0px 3px 15px rgba(0,0,0,0.1); margin-bottom: 18px; }}
    .title-text {{ font-family: 'Ink Free', cursive, sans-serif; font-size: 32px; font-weight: bold; color: #4a235a; margin: 0; }}
    div[data-testid="stTextInput"] label {{ color: #000000 !important; font-weight: 900 !important; font-size: 26px !important; background-color: #ffffff !important; padding: 6px 14px !important; border-radius: 8px !important; border: 2px solid #1a1a2e !important; display: inline-block !important; margin-bottom: 8px !important; box-shadow: 0px 2px 6px rgba(0,0,0,0.1) !important; }}
    div[data-testid="stTextInput"] input {{ color: #000000 !important; font-size: 24px !important; font-weight: bold !important; }}
    div[data-testid="stFormSubmitButton"] button {{ font-size: 24px !important; font-weight: bold !important; padding: 12px 0px !important; }}
    .welcome-text {{ text-align: center; font-size: 24px; font-weight: bold; color: #7f8c8d; letter-spacing: 2px; margin-top: 15px; }}
    .guest-name {{ text-align: center; font-family: 'Century Gothic', sans-serif; font-size: 38px; font-weight: bold; color: #1a1a2e; margin-top: 8px; background-color: #ffffff; padding: 12px; border-radius: 12px; border: 2px solid #e0e0e0; }}
    .message-text {{ text-align: center; font-size: 22px; color: #333333; margin-top: 12px; font-weight: bold; }}
    .table-text {{ text-align: center; font-size: 40px; font-weight: bold; color: #c70039; margin-top: 14px; background-color: #ffffff; padding: 12px; border-radius: 12px; border: 2px solid #c70039; }}
    .result-item-text {{ font-size: 28px !important; color: #000000 !important; font-weight: bold !important; line-height: 1.8; text-align: center; }}
    .total-badge-text {{ text-align: center; font-weight: bold; color: #4a235a; font-size: 30px; margin-top: 20px; margin-bottom: 10px; }}
    .stImage img {{ border-radius: 12px; object-fit: contain !important; width: 100% !important; height: auto !important; }}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<div class="title-box"><div class="title-text">✦ Hasif & Ikha Reception ✦</div></div>', unsafe_allow_html=True)

if df_raw is None:
    st.error('Could not find "names.xlsx". Make sure it is uploaded in your GitHub repository!')
else:
    with st.form(key='search_form'):
        query = st.text_input('Enter Guest Name:', placeholder='Type guest name here...').strip().lower()
        submit_button = st.form_submit_button('Find Seating ✨', use_container_width=True)

    if submit_button:
        if not query:
            st.warning('Please enter a name to search.')
        else:
            matches = []
            current_table = 'TABLE VIP Z1'

            for index, row in df_raw.iterrows():
                row_str_values = [str(val).strip() for val in row.values if pd.notna(val)]
                is_table_header_row = False
                for val in row_str_values:
                    if 'table' in val.lower() or 'meja' in val.lower():
                        current_table = val
                        is_table_header_row = True
                        break
                
                if is_table_header_row and len(row_str_values) <= 2:
                    continue

                for val in row.values:
                    if pd.notna(val):
                        cell_text = str(val).strip()
                        cell_lower = cell_text.lower()
                        
                        if query in cell_lower and 'table' not in cell_lower and 'meja' not in cell_lower and cell_lower != 'no' and not cell_text.isdigit():
                            row_table = current_table
                            for inline_val in row_str_values:
                                if ('table' in inline_val.lower() or 'meja' in inline_val.lower()) and inline_val != cell_text:
                                    row_table = inline_val
                                    break
                            matches.append({'guest': cell_text, 'table': row_table})

            if not matches:
                st.markdown('<div class="welcome-text" style="color: #c70039; font-size: 26px;">❌ Guest not found</div>', unsafe_allow_html=True)
                st.info('Please check the spelling and try again.')
            elif len(matches) == 1:
                st.markdown('<div class="welcome-text">— W E L C O M E —</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="guest-name">{matches[0]["guest"]}</div>', unsafe_allow_html=True)
                st.markdown('<div class="message-text">We are overjoyed to celebrate our special day with you! 💕</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="table-text">⭐ {matches[0]["table"]} ⭐</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="welcome-text" style="font-size: 26px;">— MULTIPLE GUESTS FOUND —</div>', unsafe_allow_html=True)
                results_list = '<br>'.join([f"• <b>{m['guest']}</b> -> <span style='color: #c70039;'>{m['table']}</span>" for m in matches])
                st.markdown(f'<div class="result-item-text">{results_list}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="total-badge-text">(Total - {len(matches)})</div>', unsafe_allow_html=True)
                st.info('Multiple matches found. Please find your full name in the list above!')

    st.write('')
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists('123.png'): st.image('123.png', use_container_width=True)
    with col2:
        if os.path.exists('234.png'): st.image('234.png', use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
