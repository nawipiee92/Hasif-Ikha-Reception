import os
import pandas as pd
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.messagebox as messagebox

# Load the Excel file
try:
  df = pd.read_excel('names.xlsx')
except Exception as e:
  messagebox.showerror(
      'Error',
      'Could not find "names.xlsx". Make sure it is in the same folder!',
  )
  exit()


def search_name(event=None):
  query = entry.get().strip().lower()
  if not query:
    messagebox.showwarning('Warning', 'Please enter a name to search.')
    return

  try:
    results = df[df['Name'].astype(str).str.lower().str.contains(query, na=False)]
  except KeyError:
    messagebox.showerror(
        'Error', 'Could not find a column named "Name" in your Excel file.'
    )
    return

  if results.empty:
    welcome_label.config(text='❌ Guest not found')
    guest_name_label.config(text='')
    message_label.config(text='Please check spelling and try again.')
    result_table_label.config(text='')
  else:
    row = results.iloc[0]
    guest_name = row['Name']
    table_no = row['Table No.']

    # Update labels cleanly
    welcome_label.config(text='— W E L C O M E —')
    guest_name_label.config(text=f'✨ {guest_name} ✨')
    message_label.config(
        text='We are overjoyed to celebrate our special day with you! 💕'
    )
    result_table_label.config(text=f'⭐ Table {table_no} ⭐')


# --- UI Setup (Starts in Full Screen / Maximized) ---
root = tk.Tk()
root.title('Hasif & Ikha Reception 🌸')
root.state('zoomed')  # Opens automatically maximized in full screen!
root.minsize(450, 750)

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
      # Preserves smooth scaling across full screen without distorting aspect ratio
      resized_img = original_image.resize(
          (width, height), Image.Resampling.LANCZOS
      )
      bg_image_tk = ImageTk.PhotoImage(resized_img)
      canvas.create_image(0, 0, image=bg_image_tk, anchor='nw')


canvas.bind('<Configure>', redraw_background)


# --- MAIN CONTENT CARD CONTAINER (Frosted Translucent See-Through Box) ---
# '#f5f6f8' gives a subtle, frosted glass/see-through effect over the floral border
card_bg = '#f5f6f8'
card_frame = tk.Frame(root, bg=card_bg, bd=0)
card_window = canvas.create_window(
    0, 0, window=card_frame, anchor='center', width=430, height=520
)


def center_card(event):
  # Automatically keeps the card perfectly centered whether window is normal or full screen
  canvas.coords(card_window, event.width / 2, event.height / 2)


canvas.bind('<Configure>', center_card, add='+')


# --- TITLE HEADER ---
title_label = tk.Label(
    card_frame,
    text='✦ Hasif & Ikha Reception ✦',
    font=('Ink Free', 20, 'bold'),
    bg=card_bg,
    fg='#4a235a',
)
title_label.pack(pady=(18, 2))

# --- DOUBLE UNDERLINE EFFECT ---
underline_label = tk.Label(
    card_frame,
    text='══════════════════',
    font=('Segoe UI', 9, 'bold'),
    bg=card_bg,
    fg='#4a235a',
)
underline_label.pack(pady=(0, 15))

# --- SEARCH INPUT AREA ---
search_sub_frame = tk.Frame(card_frame, bg=card_bg)
search_sub_frame.pack(pady=4)

entry = tk.Entry(
    search_sub_frame,
    width=26,
    font=('Segoe UI', 11),
    relief='solid',
    bd=1,
    justify='center',
)
entry.pack(ipady=4, pady=(0, 6))
entry.bind('<Return>', search_name)

search_btn = tk.Button(
    search_sub_frame,
    text='Find Table ✨',
    command=search_name,
    font=('Segoe UI', 10, 'bold'),
    bg='#6c3483',
    fg='white',
    relief='flat',
    padx=16,
    pady=5,
    cursor='hand2',
)
search_btn.pack()

# --- RESULT SECTION ---
welcome_label = tk.Label(
    card_frame, text='', font=('Segoe UI', 10, 'bold'), bg=card_bg, fg='#7f8c8d'
)
welcome_label.pack(pady=(10, 0))

# Guest name uses Century Gothic
guest_name_label = tk.Label(
    card_frame,
    text='',
    font=('Century Gothic', 16, 'bold'),
    bg=card_bg,
    fg='#1a1a2e',
    wraplength=400,
    justify='center',
)
guest_name_label.pack(pady=(4, 2))

message_label = tk.Label(
    card_frame, text='', font=('Segoe UI', 9), bg=card_bg, fg='#555555', wraplength=400, justify='center'
)
message_label.pack(pady=(0, 6))

result_table_label = tk.Label(
    card_frame,
    text='',
    font=('Segoe UI', 24, 'bold'),
    bg=card_bg,
    fg='#c70039',
)
result_table_label.pack(pady=(4, 0))

root.mainloop()
