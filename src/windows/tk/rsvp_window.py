import tkinter as tk
from src.windows.tk.base_window import BaseWindow


class rsvpWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "rsvp Window", "config/rsvp_window.conf")
        self.word = "A sentence example for testing wraplength; it's quite lengthy, demonstrating how the feature adjusts text in the Tkinter window."

        # Initial wraplength
        self.wraplength = 300

        # Frame to hold the label with a border
        self.frame = tk.Frame(self.master, bd=2, relief=tk.SOLID)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.word_label = tk.Label(
            self.frame,
            text=self.word,
            font=("Helvetica", 24),
            wraplength=self.wraplength,
            justify=tk.LEFT,
        )
        self.word_label.pack(fill=tk.BOTH, expand=True)

        # Label to display wraplength
        self.wraplength_label = tk.Label(
            self.master, text=f"Wraplength: {self.wraplength}"
        )
        self.wraplength_label.pack(side=tk.TOP)

        # Button to increase wraplength
        self.increase_button = tk.Button(
            self.master, text="Increase Wraplength", command=self.increase_wraplength
        )
        self.increase_button.pack(side=tk.LEFT)

        # Button to decrease wraplength
        self.decrease_button = tk.Button(
            self.master, text="Decrease Wraplength", command=self.decrease_wraplength
        )
        self.decrease_button.pack(side=tk.LEFT)

    def update_wraplength_label(self):
        self.wraplength_label.config(text=f"Wraplength: {self.wraplength}")

    def increase_wraplength(self):
        self.wraplength += 50
        self.word_label.config(wraplength=self.wraplength)
        self.update_wraplength_label()

    def decrease_wraplength(self):
        if self.wraplength > 50:
            self.wraplength -= 50  # You can adjust the decrement as needed
            self.word_label.config(wraplength=self.wraplength)
            self.update_wraplength_label()
