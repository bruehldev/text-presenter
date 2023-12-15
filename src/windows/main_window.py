from tts_manager import generate_tts
from src.windows.tk.base_window import BaseWindow
from src.windows.tk.text_input import TextInputWindow
import tkinter as tk


class MainWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Options", "config/root.conf")
        self.button1 = tk.Button(
            self.frame, text="New Window", width=25, command=self.toggle_text_input
        )
        self.button1.pack()
        self.frame.pack()
        self.text_input_window = TextInputWindow(tk.Toplevel(self.master))

    def toggle_text_input(self):
        if self.text_input_window.master.state() == "normal":
            self.text_input_window.master.withdraw()
        else:
            self.text_input_window.master.deiconify()
