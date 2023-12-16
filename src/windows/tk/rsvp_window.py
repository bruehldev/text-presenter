# Rapid Serial Visual Presentation
import tkinter as tk
from src.windows.tk.base_window import BaseWindow


class rsvpWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "rsvp Window", "config/rsvp_window.conf")
        self.word = None
        self.word_label = tk.Label(self.master, text=self.word)
        self.word_label.pack()
