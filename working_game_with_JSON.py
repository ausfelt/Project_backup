import tkinter as tk
from PIL import Image, ImageTk
import time
import json

#Load room data from JSON file

with open('rooms.json') as f:
    room_data = json.load(f)

# Convert room names to valid JSON keys
rooms = {name.replace(" ", "_"): info for name, info in room_data.items()}


#Game start

state = {
    'current_room': 'start',
    'hp': 100
}




# Function to update the GUI to reflect the current room and health

def update_room():
    room = rooms[state['current_room']]
    text.delete(1.0, tk.END)
    text.insert(tk.END, room['text'] + "\n\n")
    update_health_bar()
    for button in option_buttons:
        button.pack_forget()
    for i, option in enumerate(room['options']):
        button_text, _, _ = option
        command = lambda option=option: choose_option(option)
        button = tk.Button(frame, text=button_text, command=command, bg='teal', fg='black', font=('Arial', 12))
        button.pack(side=tk.TOP, fill=tk.X)
        option_buttons.append(button)


# Updating HP bar for current value

def update_health_bar():
    current_hp = state['hp']
    if current_hp >= 101:
        health_color = 'green'
    elif current_hp <= 99:
        health_color = 'red'
    else:
        health_color = 'blue'
    health_bar.delete('all')
    health_bar.create_rectangle(0, 0, 100, 20, fill=health_color)
    health_value.config(text=f"HP: {current_hp}")


# Function to update game state

def choose_option(option):
    _, next_room, hp_delta = option
    state['current_room'] = next_room
    state['hp'] += hp_delta
    update_room()
    message = ""
    if hp_delta < 0:
        message = "\nOOOF! That was not a wise choice."
    elif hp_delta > 0:
        message = "\nYay! You feel replenished."
    else:
        message = "\nGood choice! You chose wisely."
    text.insert(tk.END, message)
    text.after(3000, lambda: remove_text(message))


# removing the text from the widget

def remove_text(message):
    start_index = text.search(message, "1.0", tk.END)
    end_index = f"{start_index} + {len(message)} chars"
    text.delete(start_index, end_index)


# All GUI-stuff with TKinter

root = tk.Tk()
root.configure(bg='teal')

frame = tk.Frame(root, bg='teal')
frame.pack()

text = tk.Text(frame, wrap=tk.WORD, bg='black', fg='white', font=('Arial', 18))
text.pack()

health_frame = tk.Frame(frame, bg='black', pady=5)
health_frame.pack(side=tk.BOTTOM)
health_label = tk.Label(health_frame, text='Health:', fg='white', bg='black', font=('Arial', 12))
health_label.pack(side=tk.LEFT)
health_bar = tk.Canvas(health_frame, width=100, height=20, bg='black', highlightthickness=0)
health_bar.pack(side=tk.LEFT)
health_value = tk.Label(health_frame, text='HP: 100', fg='white', bg='black', font=('Arial', 12))
health_value.pack(side=tk.LEFT)


option_buttons = []

update_room()

root.mainloop()