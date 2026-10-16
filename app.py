import os
import pandas as pd
from PIL import Image, ImageOps, ImageTk
import tkinter as tk
import tkinter.messagebox as messagebox

# Load the Excel file safely
try:
  df_raw = pd.read_excel('names.xlsx', header=None)
except Exception as e:
  messagebox.showerror(
      'Error',
      'Could not find "names.xlsx". Make sure it is in the same folder!',
  )
  exit()


def search_name(event=None):
  try:
    query = entry.get().strip().lower()
    if not query:
      messagebox.showwarning('Warning', 'Please enter a name to search.')
      return

    matches = []
    current_table = 'TABLE VIP Z1'

    # Scan through the Excel rows to find ALL matching guests
    for index, row in df_raw.iterrows():
      row_str_values = [str(val).strip() for val in row.values if pd.notna(val)]
      
      # Update table header if found
      for val in row_str_values:
        if 'table' in val.lower():
          current_table = val
          break
          
      # Check cells for matching guest name
      for col_idx, val in enumerate(row.values):
        if pd.notna(val):
          cell_text = str(val).strip()
          # If query matches and it's not a header/number
          if query in cell_text.lower() and 'table' not in cell_text.lower() and cell_text.lower() != 'no':
            # Avoid duplicate entries of the exact same name in the same table
            if not any(m['guest'] == cell_text and m['table'] == current_table for m in matches):
              matches.append({'guest': cell_text, 'table': current_table})

    if not matches:
      welcome_label.config(text='❌ Guest not found')
      guest_name_label.config(text='', font=('Century Gothic', 20, 'bold'), fg='#1a1a2e')
      message_label.config(text='Please check spelling and try again.')
      result_table_label.config(text='')
    elif len(matches) == 1:
      # Single match found (Stars removed from name, color set to black)
      welcome_label.config(text='— W E L C O M E —')
      guest_name_label.config(text=f"{matches[0]['guest']}", font=('Century Gothic', 20, 'bold'), fg='#1a1a2e')
      message_label.config(
          text='We are overjoyed to celebrate our special day with you! 💕'
      )
      result_table_label.config(text=f"⭐ {matches[0]['table']} ⭐")
    else:
      # Multiple matches found (e.g., Rogayah & Datin Rogayah)
      welcome_label.config(text='— MULTIPLE GUESTS FOUND —')
      
      # Format list of matching guests and their tables cleanly
      results_text = '\n'.join([f"• {m['guest']} ({m['table']})" for m in matches])
      
      guest_name_label.config(text=results_text, font=('Century Gothic', 12, 'bold'), fg='#1a1a2e')
      message_label.config(text='Please check the list above for the correct name.')
      result_table_label.config(text='')

  except Exception as err:
    messagebox.showerror('Search Error', f'An error occurred during search: {err}')


# --- UI Setup (Starts in Full Screen / Maximized) ---
root = tk.Tk()
root.title('Hasif & Ikha Reception 🌸')
root.state('zoomed')  # Opens automatically maximized in full screen!
root.minsize(450, 700)

# --- BACKGROUND IMAGE SETUP (Using Border.png) ---
try:
  img_path = 'Border.png'
  original_image = Image.open(img_path)
except Exception as e:
  original_image = None
  print(
      'Could not load Border.png. Make sure it is in the exact same folder as'
      ' app.py'
  )

# Use a canvas to make sure the background image scales smoothly and reliably
canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill='both', expand=True)

bg_image_tk = None


def redraw_background(event):
  global bg_image_tk
  if original_image:
    width = event.width
    height = event.height
    if width > 10 and height > 10:
      resized_img = original_image.resize(
          (width, height), Image.Resampling.LANCZOS
      )
      bg_image_tk = ImageTk.PhotoImage(resized_img)
      canvas.create_image(0, 0, image=bg_image_tk, anchor='nw')


canvas.bind('<Configure>', redraw_background)


# --- MAIN CONTENT CARD CONTAINER ---
card_bg = '#f5f6f8'
card_frame = tk.Frame(root, bg=card_bg, bd=0)
card_window = canvas.create_window(
    0, 0, window=card_frame, anchor='center', width=430, height=540
)


def center_card(event):
  canvas.coords(card_window, event.width / 2, event.height / 2)


canvas.bind('<Configure>', center_card, add='+')


# --- TOP SECTION (Title & Search) ---
top_frame = tk.Frame(card_frame, bg=card_bg)
top_frame.pack(side='top', fill='x', pady=(10, 0))

title_label = tk.Label(
    top_frame,
    text='✦ Hasif & Ikha Reception ✦',
    font=('Ink Free', 18, 'bold'),
    bg=card_bg,
    fg='#4a235a',
)
title_label.pack(pady=(5, 0))

underline_label = tk.Label(
    top_frame,
    text='══════════════════',
    font=('Segoe UI', 8, 'bold'),
    bg=card_bg,
    fg='#4a235a',
)
underline_label.pack(pady=(0, 4))

search_sub_frame = tk.Frame(top_frame, bg=card_bg)
search_sub_frame.pack(pady=2)

entry = tk.Entry(
    search_sub_frame,
    width=24,
    font=('Segoe UI', 10),
    relief='solid',
    bd=1,
    justify='center',
)
entry.pack(ipady=3, pady=(0, 3))
entry.bind('<Return>', search_name)

search_btn = tk.Button(
    search_sub_frame,
    text='Find Table ✨',
    command=search_name,
    font=('Segoe UI', 9, 'bold'),
    bg='#6c3483',
    fg='white',
    relief='flat',
    padx=14,
    pady=2,
    cursor='hand2',
)
search_btn.pack()


# --- DECORATIVE IMAGES SECTION (Anchored firmly at the bottom) ---
image_frame = tk.Frame(card_frame, bg=card_bg)
image_frame.pack(side='bottom', pady=(0, 10))


def load_curved_image(path, target_w, target_h, radius=20):
  """Resizes and crops image with smooth rounded corners."""
  try:
    img = Image.open(path).convert('RGBA')
    
    img_thumb = ImageOps.fit(
        img, (target_w, target_h), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5)
    )
    
    mask = Image.new('L', (target_w, target_h), 0)
    from PIL import ImageDraw
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (target_w, target_h)], radius=radius, fill=255)
    
    rounded_img = Image.new('RGBA', (target_w, target_h), (255, 255, 255, 0))
    rounded_img.paste(img_thumb, (0, 0), mask=mask)
    
    return ImageTk.PhotoImage(rounded_img)
  except Exception as e:
    print(f'Could not load {path}: {e}')
    return None


# Large dimensions (190px wide by 140px tall) with smooth 20px rounded corners
img1_tk = load_curved_image('123.png', 190, 140, radius=20)
if img1_tk:
  img_label1 = tk.Label(image_frame, image=img1_tk, bg=card_bg)
  img_label1.image = img1_tk
  img_label1.pack(side='left', padx=6)

img2_tk = load_curved_image('234.png', 190, 140, radius=20)
if img2_tk:
  img_label2 = tk.Label(image_frame, image=img2_tk, bg=card_bg)
  img_label2.image = img2_tk
  img_label2.pack(side='left', padx=6)


# --- MIDDLE SECTION (Welcome -> Guest Name -> Message -> Table Number) ---
middle_frame = tk.Frame(card_frame, bg=card_bg)
middle_frame.pack(side='top', fill='both', expand=True)

content_wrapper = tk.Frame(middle_frame, bg=card_bg)
content_wrapper.place(relx=0.5, rely=0.40, anchor='center')

# 1. WELCOME text on top
welcome_label = tk.Label(
    content_wrapper, text='', font=('Segoe UI', 9, 'bold'), bg=card_bg, fg='#7f8c8d'
)
welcome_label.pack(pady=(0, 2))

# 2. Guest Name / Multiple Names list right below WELCOME (Size 20, Solid Black color, No Stars)
guest_name_label = tk.Label(
    content_wrapper,
    text='',
    font=('Century Gothic', 20, 'bold'),
    bg=card_bg,
    fg='#1a1a2e',
    wraplength=400,
    justify='center',
)
guest_name_label.pack(pady=(2, 6))

message_label = tk.Label(
    content_wrapper, text='', font=('Segoe UI', 8), bg=card_bg, fg='#555555', wraplength=400, justify='center'
)
message_label.pack(pady=(0, 6))

# 3. Table Number at the bottom of the section (Size 20)
result_table_label = tk.Label(
    content_wrapper,
    text='',
    font=('Segoe UI', 20, 'bold'),
    bg=card_bg,
    fg='#c70039',
)
result_table_label.pack(pady=(2, 0))

root.mainloop()
