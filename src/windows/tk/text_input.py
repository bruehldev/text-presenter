import tkinter as tk
from src.windows.tk.base_window import BaseWindow


class TextInputWindow(BaseWindow):
    def __init__(self, master, text_window):
        super().__init__(master, "Text Input", "config/text_input.conf")
        self.text_input = tk.Text(self.master)
        self.text_input.pack()
        self.text_window = text_window

        self.send_button = tk.Button(
            self.master,
            text="Send",
            command=self.update_text_window,
        )
        self.send_button.pack()

    def update_text_window(self):
        self.text_window.text_widget.delete("1.0", "end")
        self.text_window.text_widget.insert("1.0", self.text_input.get("1.0", "end"))
