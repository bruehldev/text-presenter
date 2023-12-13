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


def process_text():
    generate_tts()
    # Show the processed text in a new window
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
        # pygame.time.Clock().tick(10)

    else:
        messagebox.showwarning(
            "File Not Found", "No TTS audio file found. Please process the text first."
        )


def stop_audio():
    pygame.mixer.music.stop()


def display_words(speed):
    words = text_input.get("1.0", "end-1c").split()
    word_window = tk.Toplevel(root)
    word_window.title("Word Display")

    processed_text_window = tk.Toplevel(root)
    processed_text_window.title("Processed Text")

    # Create a label to display words
    word_label = tk.Label(word_window, font=("Helvetica", 16))
    word_label.pack()

    processed_text_widget = tk.Text(
        processed_text_window, wrap="word", height=10, width=50
    )

    # add text to the widget
    processed_text_widget.insert("1.0", text_input.get("1.0", "end-1c"))
    # create text index
    word_pointer_start = "1.0"
    word_pointer_end = "1.0"

    # Iterate through words and display them
    for i in range(len(words)):
        word = words[i]
        word_label.config(text=word)
        word_window.update()

        # use index to highlight the word in the text widget
        # print word in the text widget
        word_pointer_start = processed_text_widget.search(
            word, word_pointer_end, stopindex="end"
        )
        word_pointer_end = f"{word_pointer_start}+{len(word)}c"

        processed_text_widget.tag_add("highlight", word_pointer_start, word_pointer_end)
        processed_text_widget.tag_config("highlight", background="yellow")

        # unmark previous word
        if i > 0:
            processed_text_widget.tag_remove(
                "highlight",
                f"{word_pointer_start}-{len(words[i-1])+1}c",
                word_pointer_start,
            )
        processed_text_widget.pack()
        processed_text_window.update()

        delay = int(1000 / speed)
        word_window.after(delay)


def create_config_folder():
    config_folder = "config"
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)


create_config_folder()

# Tkinter setup
root = tk.Tk()
root.title("Text Presenter")


def load_size(window, filename):
    try:
        with open(filename, "r") as conf:
            window.geometry(conf.read())
    except FileNotFoundError:
        pass


def save_size(window, filename):
    with open(filename, "w") as conf:
        conf.write(window.geometry())


# Text input
text_input = tk.Text(root, height=10, width=50)
text_input.pack()

# Process button
process_button = tk.Button(root, text="Process", command=process_text)
process_button.pack()

# Separate window for playing audio
play_window = tk.Toplevel(root)
play_window.title("Play Audio")

# New window for word display
word_display_window = tk.Toplevel(root)
word_display_window.title("Word Display")

# Load window sizes from file
load_size(root, "config/root.conf")
load_size(play_window, "config/play_window.conf")
load_size(word_display_window, "config/word_display_window.conf")


def configure_and_save_size(event, window, filename):
    window.update()
    save_size(window, filename)


root.bind(
    "<Configure>",
    lambda event: configure_and_save_size(event, root, "config/root.conf"),
)
play_window.bind(
    "<Configure>",
    lambda event: configure_and_save_size(
        event, play_window, "config/play_window.conf"
    ),
)
word_display_window.bind(
    "<Configure>",
    lambda event: configure_and_save_size(
        event, word_display_window, "config/word_display_window.conf"
    ),
)

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
