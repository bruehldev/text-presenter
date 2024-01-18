import tkinter as tkk
from src.windows.tk.base_window import BaseWindow


class TextWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Text Window", "config/text_window.conf")
        self.frame = tkk.Frame(self.master)

        # headline
        self.headline = tkk.Label(self.master, text="Generated Headline")
        self.headline.pack()

        self.text_widget = tkk.Text(self.master, wrap="word")
        self.text_widget.configure(bg="black", fg="white")
        self.text_widget.pack(fill="both", expand=True)
