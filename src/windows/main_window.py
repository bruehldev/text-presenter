import tkinter as tk
from tts_manager import generate_tts
from src.windows.tk.base_window import BaseWindow
from src.windows.tk.text_input import TextInputWindow


class MainWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Options", "config/root.conf")

        self.frame.pack()
        self.text_input_window = TextInputWindow(tk.Toplevel(self.master))
        self.text_input_window_state = self.text_input_window.master.state()
        self.button1 = tk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_button("Text Input"),
        )
        if self.text_input_window_state == "normal":
            self.button1.config(text=f"Close Text Input")
        else:
            self.button1.config(text="Open Text Input")
        self.button1.pack()

    def toggle_button(self, name):
        if self.text_input_window.master.state() == "normal":
            self.text_input_window.master.withdraw()
            self.button1.config(text=f"Open {name}")
        else:
            self.text_input_window.master.deiconify()
            self.button1.config(text=f"Close {name}")
