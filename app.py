import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd

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


# --- UI Setup ---
root = tk.Tk()
root.title('Hasif & Ikha Reception 🌸')
root.geometry('1024x700')
root.state('zoomed')  # Full screen / maximized mode

# --- BACKGROUND IMAGE SETUP ---
try:
  img_path = 'FBorder.png'
  original_image = Image.open(img_path)
except Exception as e:
  original_image = None
  print(
      'Could not load FBorder.png. Make sure it is in the exact same folder as'
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


# --- MAIN CONTENT CARD CONTAINER (Placed cleanly on top of the canvas) ---
card_frame = tk.Frame(root, bg='#ffffff', bd=0)
# We use canvas.create_window so the white card stays securely on top of the background image
card_window = canvas.create_window(
    500, 300, window=card_frame, anchor='center', width=680, height=380
)


def center_card(event):
  # Automatically keeps the card perfectly centered when the window resizes
  canvas.coords(card_window, event.width / 2, event.height / 2)


canvas.bind('<Configure>', center_card, add='+')


# --- TITLE HEADER ---
title_label = tk.Label(
    card_frame,
    text='✦ Hasif & Ikha Reception ✦',
    font=('Segoe UI', 16, 'bold'),
    bg='#ffffff',
    fg='#4a235a',
)
title_label.pack(pady=(15, 8))

# --- SEARCH INPUT AREA ---
search_sub_frame = tk.Frame(card_frame, bg='#ffffff')
search_sub_frame.pack(pady=4)

entry = tk.Entry(
    search_sub_frame,
    width=30,
    font=('Segoe UI', 12),
    relief='solid',
    bd=1,
    justify='center',
)
entry.pack(ipady=3, pady=(0, 4))
entry.bind('<Return>', search_name)

search_btn = tk.Button(
    search_sub_frame,
    text='Find Table ✨',
    command=search_name,
    font=('Segoe UI', 10, 'bold'),
    bg='#6c3483',
    fg='white',
    relief='flat',
    padx=14,
    pady=4,
    cursor='hand2',
)
search_btn.pack()

# --- RESULT SECTION ---
welcome_label = tk.Label(
    card_frame, text='', font=('Segoe UI', 10, 'bold'), bg='#ffffff', fg='#7f8c8d'
)
welcome_label.pack(pady=(10, 0))

guest_name_label = tk.Label(
    card_frame,
    text='',
    font=('Segoe UI', 16, 'bold'),
    bg='#ffffff',
    fg='#1a1a2e',
    wraplength=620,
    justify='center',
)
guest_name_label.pack(pady=(2, 2))

message_label = tk.Label(
    card_frame, text='', font=('Segoe UI', 9), bg='#ffffff', fg='#555555'
)
message_label.pack(pady=(0, 6))

result_table_label = tk.Label(
    card_frame, text='', font=('Segoe UI', 22, 'bold'), bg='#ffffff', fg='#c70039'
)
result_table_label.pack(pady=(4, 0))

root.mainloop()