import tkinter as tk
from src.windows.tk.base_window import BaseWindow
from src.services.config_manager import get_config_parameter, set_config_parameter


class rsvpWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "rsvp Window", "config/rsvp_window.conf")
        self.word = "A sentence example for testing wraplength; it's quite lengthy, demonstrating how the feature adjusts text in the Tkinter window."

        # Initial wraplength
        self.wraplength = 300
        self.font_size = 24  # Initial font size

        # Frame to hold the label with a border
        self.frame = tk.Frame(self.master, bd=2, relief=tk.SOLID)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.word_label = tk.Label(
            self.frame,
            text=self.word,
            font=("Helvetica", self.font_size),
            wraplength=self.wraplength,
            justify=tk.LEFT,
        )
        self.word_label.pack(fill=tk.BOTH, expand=True)

        # Label to display wraplength
        self.wraplength_label = tk.Label(
            self.master, text=f"Wraplength: {self.wraplength}"
        )
        self.wraplength_label.pack(side=tk.TOP)

        # Label to display font size
        self.font_size_label = tk.Label(
            self.master, text=f"Text Size: {self.font_size}"
        )
        self.font_size_label.pack(side=tk.TOP)

        # Button to increase wraplength
        self.increase_wraplength_button = tk.Button(
            self.master, text="Increase Wraplength", command=self.increase_wraplength
        )
        self.increase_wraplength_button.pack(side=tk.LEFT)

        # Button to decrease wraplength
        self.decrease_wraplength_button = tk.Button(
            self.master, text="Decrease Wraplength", command=self.decrease_wraplength
        )
        self.decrease_wraplength_button.pack(side=tk.LEFT)

        # Button to increase text size
        self.increase_text_size_button = tk.Button(
            self.master, text="Increase Text Size", command=self.increase_text_size
        )
        self.increase_text_size_button.pack(side=tk.LEFT)

        # Button to decrease text size
        self.decrease_text_size_button = tk.Button(
            self.master, text="Decrease Text Size", command=self.decrease_text_size
        )
        self.decrease_text_size_button.pack(side=tk.LEFT)

        self.load_wraplength()
        self.load_font_size()

    def update_wraplength_label(self):
        self.wraplength_label.config(text=f"Wraplength: {self.wraplength}")

    def update_font_size_label(self):
        self.font_size_label.config(text=f"Text Size: {self.font_size}")
        self.word_label.config(font=("Helvetica", self.font_size))

    def increase_wraplength(self):
        self.wraplength += 50
        self.word_label.config(wraplength=self.wraplength)
        self.update_wraplength_label()
        self.save_wraplength()

    def decrease_wraplength(self):
        if self.wraplength > 50:
            self.wraplength -= 50
            self.word_label.config(wraplength=self.wraplength)
            self.update_wraplength_label()
            self.save_wraplength()

    def increase_text_size(self):
        self.font_size += 2
        self.word_label.config(font=("Helvetica", self.font_size))
        self.update_font_size_label()
        self.save_font_size()

    def decrease_text_size(self):
        if self.font_size > 2:
            self.font_size -= 2
            self.word_label.config(font=("Helvetica", self.font_size))
            self.update_font_size_label()
            self.save_font_size()

    def save_wraplength(self):
        set_config_parameter("rsvp_window", "wraplength", self.wraplength)

    def save_font_size(self):
        set_config_parameter("rsvp_window", "font_size", self.font_size)

    def load_wraplength(self):
        loaded_wraplength = get_config_parameter("rsvp_window", "wraplength")
        if loaded_wraplength is not None:
            self.wraplength = loaded_wraplength
            self.word_label.config(wraplength=self.wraplength)
            self.update_wraplength_label()

    def load_font_size(self):
        loaded_font_size = get_config_parameter("rsvp_window", "font_size")
        if loaded_font_size is not None:
            self.font_size = loaded_font_size
            self.word_label.config(font=("Helvetica", self.font_size))
            self.update_font_size_label()
