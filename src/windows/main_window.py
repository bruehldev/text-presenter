import tkinter as tk
from src.windows.tk.base_window import BaseWindow
from src.windows.tk.text_input import TextInputWindow
from src.windows.tk.text_window import TextWindow
from src.windows.tk.audio_window import AudioWindow
from src.windows.tk.rsvp_window import rsvpWindow


class MainWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Options", "config/root.conf")

        self.frame.pack()

        # Text Window
        self.text_window = TextWindow(tk.Toplevel(self.master))
        self.text_window_button = tk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_text_window_button("Text Window"),
        )
        if self.text_window.master.state() == "normal":
            self.text_window_button.config(text=f"Close Text Window")
        else:
            self.text_window_button.config(text="Open Text Window")
        self.text_window_button.pack()

        # RSVP Window
        self.rsvp_window = rsvpWindow(tk.Toplevel(self.master))
        self.rsvp_window_button = tk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_rsvp_window_button("RSVP Window"),
        )
        if self.rsvp_window.master.state() == "normal":
            self.rsvp_window_button.config(text=f"Close RSVP Window")
        else:
            self.rsvp_window_button.config(text="Open RSVP Window")
        self.rsvp_window_button.pack()

        # Speed control slider
        self.speed_label = tk.Label(self.frame, text="Speed:")
        self.speed_label.pack()

        self.speed_var = tk.DoubleVar()
        self.speed_slider = tk.Scale(
            self.frame,
            from_=0.1,
            to=2.0,
            variable=self.speed_var,
            length=200,
            orient="horizontal",
        )
        self.speed_slider.set(1.0)
        self.speed_slider.pack()

        # Audio Window
        self.audio_window = AudioWindow(
            tk.Toplevel(self.master),
            self.text_window.text_widget,
            self.rsvp_window.master,
            self.rsvp_window.word_label,
            self.speed_var.get(),
        )
        self.audio_window_button = tk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_audio_window_button("Audio Window"),
        )
        if self.audio_window.master.state() == "normal":
            self.audio_window_button.config(text=f"Close Audio Window")
        else:
            self.audio_window_button.config(text="Open Audio Window")

        self.audio_window_button.pack()

        # Text Input Window
        self.text_input_window = TextInputWindow(
            tk.Toplevel(self.master), self.text_window, self.audio_window
        )
        self.text_input_button = tk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_text_input_window_button("Text Input"),
        )
        if self.text_input_window.master.state() == "normal":
            self.text_input_button.config(text=f"Close Text Input")
        else:
            self.text_input_button.config(text="Open Text Input")
        self.text_input_button.pack()

        # Start display words button
        self.start_button = tk.Button(
            self.frame,
            text="Start",
            command=lambda: self.display_words(
                self.speed_var.get(),
                self.text_input_window.text_input.get("1.0", "end-1c"),
                self.text_window.text_widget,
                self.rsvp_window.word_label,
                self.rsvp_window.master,
            ),
        )
        self.start_button.pack()

    def display_words(
        self, speed, words, target_text_widget, target_word_label, target_word_window
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
            word_pointer_start = target_text_widget.search(
                word, word_pointer_end, stopindex="end"
            )
            word_pointer_end = f"{word_pointer_start}+{len(word)}c"

            target_text_widget.tag_add(
                "highlight", word_pointer_start, word_pointer_end
            )
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

    def toggle_text_input_window_button(self, name):
        if self.text_input_window.master.state() == "normal":
            self.text_input_window.master.withdraw()
            self.text_input_button.config(text=f"Open {name}")
        else:
            self.text_input_window.master.deiconify()
            self.text_input_button.config(text=f"Close {name}")

    def toggle_text_window_button(self, name):
        if self.text_window.master.state() == "normal":
            self.text_window.master.withdraw()
            self.text_window_button.config(text=f"Open {name}")
        else:
            self.text_window.master.deiconify()
            self.text_window_button.config(text=f"Close {name}")

    def toggle_audio_window_button(self, name):
        if self.audio_window.master.state() == "normal":
            self.audio_window.master.withdraw()
            self.audio_window_button.config(text=f"Open {name}")
        else:
            self.audio_window.master.deiconify()
            self.audio_window_button.config(text=f"Close {name}")

    def toggle_rsvp_window_button(self, name):
        if self.rsvp_window.master.state() == "normal":
            self.rsvp_window.master.withdraw()
            self.rsvp_window_button.config(text=f"Open {name}")
        else:
            self.rsvp_window.master.deiconify()
            self.rsvp_window_button.config(text=f"Close {name}")
