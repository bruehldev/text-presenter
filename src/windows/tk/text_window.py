import tkinter as tk
from tkinter import messagebox, ttk
from tts_manager import generate_tts
from src.windows.tk.base_window import BaseWindow


class TextWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Text Window", "config/text_window.conf")
        self.text_widget = tk.Text(self.master, wrap="word")
        self.text_widget.pack(fill="both", expand=True)
        # load text from clipboard
        self.text_widget.insert("1.0", self.master.clipboard_get())
