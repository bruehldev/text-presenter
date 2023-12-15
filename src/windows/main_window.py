import tkinter as tk
from tts_manager import generate_tts
from src.windows.tk.base_window import BaseWindow
from src.windows.tk.text_input import TextInputWindow
from src.windows.tk.text_window import TextWindow


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

        # Text Input Window
        self.text_input_window = TextInputWindow(
            tk.Toplevel(self.master), self.text_window
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
