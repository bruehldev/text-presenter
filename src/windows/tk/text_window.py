import tkinter as tk
from src.windows.tk.base_window import BaseWindow


class TextWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Text Window", "config/text_window.conf")
        # headline
        self.headline = tk.Label(self.master, text="Generated Headline")
        self.headline.pack()

        self.text_widget = tk.Text(self.master, wrap="word")
        self.text_widget.pack(fill="both", expand=True)
