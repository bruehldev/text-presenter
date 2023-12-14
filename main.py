import tkinter as tk

from tkinter import messagebox, ttk

from tts_manager import generate_tts
from audio_manager import play_audio, stop_audio
from config_manager import load_size, save_size


### Tkinter setup ###
root = tk.Tk()
root.title("Text Presenter")


def process_text(words):
    generate_tts(words)
    # Show the processed text in a new window
    messagebox.showinfo("TTS Generated", "TTS audio generated successfully!")


def display_words(
    speed, words, target_text_widget, target_word_label, target_word_window
):
    # add text to the widget
    target_text_widget.insert("1.0", words)
    # create text index
    word_pointer_start = "1.0"
    word_pointer_end = "1.0"

    # Iterate through words and display them
    words_split = words.split()
    for i in range(len(words_split)):
        word = words_split[i]
        target_word_label.config(text=word)
        target_word_window.update()

        # use index to highlight the word in the text widget
        # print word in the text widget
        word_pointer_start = target_text_widget.search(
            word, word_pointer_end, stopindex="end"
        )
        word_pointer_end = f"{word_pointer_start}+{len(word)}c"

        target_text_widget.tag_add("highlight", word_pointer_start, word_pointer_end)
        target_text_widget.tag_config("highlight", background="yellow")

        # unmark previous word
        if i > 0:
            target_text_widget.tag_remove(
                "highlight",
                f"{word_pointer_start}-{len(words_split[i-1])+1}c",
                word_pointer_start,
            )
        target_text_widget.pack()
        target_text_widget.update()

        delay = int(1000 / speed)
        target_word_window.after(delay)


# Text input
text_input = tk.Text(root, height=50, width=80)
text_input.pack()

# Process button
process_button = tk.Button(
    root,
    text="Process",
    command=lambda: process_text(
        text_input.get("1.0", "end-1c"),
    ),
)
process_button.pack()

# Separate window for playing audio
play_window = tk.Toplevel(root, height=10, width=10)
play_window.title("Play Audio")

# Play button in the separate window
play_button = tk.Button(play_window, text="Play TTS Audio", command=play_audio)
play_button.pack()

# Stop button in the separate window
stop_button = tk.Button(play_window, text="Stop Audio", command=stop_audio)
stop_button.pack()

# New window for word display
word_display_window = tk.Toplevel(root, height=100, width=100)
word_display_window.title("Word Display")

word_window = tk.Toplevel(root, height=100, width=100)
word_window.title("Word")

# Create a label to display words
word_label = tk.Label(word_window, text="")
word_label.pack()

processed_text_window = tk.Toplevel(root, height=100, width=100)
processed_text_window.title("Processed Text")


processed_text_widget = tk.Text(processed_text_window, wrap="word", height=10, width=50)

# Load window sizes from file
load_size(root, "config/root.conf")
load_size(play_window, "config/play_window.conf")
load_size(word_display_window, "config/word_display_window.conf")
load_size(word_window, "config/word_window.conf")
load_size(processed_text_window, "config/processed_text_window.conf")


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
word_window.bind(
    "<Configure>",
    lambda event: configure_and_save_size(
        event, word_window, "config/word_window.conf"
    ),
)
processed_text_window.bind(
    "<Configure>",
    lambda event: configure_and_save_size(
        event, processed_text_window, "config/processed_text_window.conf"
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
    command=lambda: display_words(
        speed_var.get(),
        text_input.get("1.0", "end-1c"),
        processed_text_widget,
        word_label,
        word_window,
    ),
)
display_button.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
