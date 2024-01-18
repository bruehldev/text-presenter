from tkinter import ttk, Text
from src.windows.tk.base_window import BaseWindow


class TextWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Text Window", "config/text_window.conf")
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)

        # headline
        self.headline = ttk.Label(self.frame, text="Generated Headline")
        self.headline.pack()

        self.text_widget = Text(self.frame, wrap="word")
        self.text_widget.configure(bg="black", fg="white")
        self.text_widget.pack(fill="both", expand=True)
