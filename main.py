import tkinter as tk
import pyperclip
import keyboard
import requests
from pynput import keyboard


def llm(text, single_answer=None):
    token = "" # Insert token from Google studio
    # URL and API key
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={token}"

    # Headers
    headers = {
        'Content-Type': 'application/json'
    }
    user_prefix = None
    if single_answer is not None:
        user_prefix = 'Question with single answer. ' if single_answer else 'Question with multiple answer. '
    data = {
        "contents": [
            {
                "role": "model",
                "parts": [
                    {
                        "text": ""} # Insert additional text here for model
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"{user_prefix} Answer VERY VERY shortly this {text}"}
                ]
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return reply
    except:
        return None


def get_text():
    # Get copied text from clipboard
    text = pyperclip.paste()
    return text


def update_text(text):
    label.config(text=text)
    window.update()  # Update window content


# Initialize the Tkinter window
window = tk.Tk()
window.overrideredirect(True)  # Remove window borders
window.geometry("50x50+100+100")  # Set window size and position
window.attributes("-topmost", True)  # Keep the window always on top
window.config(bg="white")
# Variables to store the window's position for dragging
start_x = None
start_y = None


# Function to start moving the window
def start_move(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y


# Function to drag the window
def drag_window(event):
    x = window.winfo_x() + (event.x - start_x)
    y = window.winfo_y() + (event.y - start_y)
    window.geometry(f"+{x}+{y}")


# Create and place a label to display text
label = tk.Label(window, text=".,", font=("Helvetica", 12),  bg="white", fg="black")
label.pack(expand=True)

# Bind mouse events for moving the window
window.bind("<Button-1>", start_move)  # Start moving on mouse button press
window.bind("<B1-Motion>", drag_window)  # Drag the window with the mouse


def on_press(key):
    try:
        if key.char == '.':
            text = get_text()
            answer = llm(text, True)
            update_text(answer)
        elif key.char == ',':
            text = get_text()
            answer = llm(text, False)
            update_text(answer)
        elif key.char == 'q':
            window.destroy()  # Close the window if 'q' is pressed
    except AttributeError:
        pass

# Start the listener for key presses
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Start checking for key presses

# Start the Tkinter main loop
window.mainloop()
