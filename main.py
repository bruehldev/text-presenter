import tkinter as tk
from tkinter import messagebox, ttk
from TTS.api import TTS
import pygame
import os
import torch


def generate_tts():
    # Init
    text = text_input.get("1.0", "end-1c")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    # Generate TTS audio
    tts.tts_to_file(
        text=text, speaker_wav="example_1.wav", language="en", file_path="output.wav"
    )
    # wav = tts.tts(text="Hello world!", speaker_wav="example_1.wav", language="en")


def process_text():
    generate_tts()
    # Show the processed text in a new window
    text = text_input.get("1.0", "end-1c")

    processed_text_window = tk.Toplevel(root)
    processed_text_window.title("Processed Text")

    processed_text_label = tk.Label(processed_text_window, text=text)
    processed_text_label.pack()

    messagebox.showinfo("TTS Generated", "TTS audio generated successfully!")


def play_audio():
    if os.path.exists("output.wav"):
        # Init
        pygame.init()
        pygame.mixer.music.load("output.wav")

        # Play
        pygame.mixer.music.play()

        # Keep the window open until the audio is done playing
        # while pygame.mixer.music.get_busy():
        #     pygame.time.Clock().tick(10)

    else:
        messagebox.showwarning(
            "File Not Found", "No TTS audio file found. Please process the text first."
        )


def stop_audio():
    pygame.mixer.music.stop()


def display_words(speed):
    if os.path.exists("output.wav"):
        words = text_input.get("1.0", "end-1c").split()
        word_window = tk.Toplevel(root)
        word_window.title("Word Display")

        # Create a label to display words
        word_label = tk.Label(word_window, font=("Helvetica", 16))
        word_label.pack()

        # Iterate through words and display them
        for word in words:
            word_label.config(text=word)
            word_window.update()
            delay = int(1000 / speed)
            word_window.after(delay)

    else:
        messagebox.showwarning(
            "File Not Found", "No TTS audio file found. Please process the text first."
        )


# Tkinter setup
root = tk.Tk()
root.title("Text Presenter")

# Text input
text_input = tk.Text(root, height=10, width=50)
text_input.pack()

# Process button
process_button = tk.Button(root, text="Process", command=process_text)
process_button.pack()

# Separate window for playing audio
play_window = tk.Toplevel(root)
play_window.title("Play Audio")

# Play button in the separate window
play_button = tk.Button(play_window, text="Play TTS Audio", command=play_audio)
play_button.pack()

# Stop button in the separate window
stop_button = tk.Button(play_window, text="Stop Audio", command=stop_audio)
stop_button.pack()

# New window for word display
word_display_window = tk.Toplevel(root)
word_display_window.title("Word Display")

# Speed control slider
speed_label = tk.Label(word_display_window, text="Speed:")
speed_label.grid(row=0, column=0, padx=10, pady=10)

speed_var = tk.DoubleVar()
speed_slider = ttk.Scale(
    word_display_window,
    from_=0.1,
    to=2.0,
    variable=speed_var,
    length=200,
    orient="horizontal",
)
speed_slider.set(1.0)
speed_slider.grid(row=0, column=1, padx=10, pady=10)

# Button to display words
display_button = tk.Button(
    word_display_window,
    text="Display Words",
    command=lambda: display_words(speed_var.get()),
)
display_button.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
