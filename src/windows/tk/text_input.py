import tkinter as tk
from src.windows.tk.base_window import BaseWindow
import nltk

nltk.download("punkt")


class TextInputWindow(BaseWindow):
    def __init__(self, master, text_window, audio_window):
        super().__init__(master, "Text Input", "config/text_input.conf")
        self.text_input = tk.Text(self.master)
        self.text_input.pack()
        self.text_window = text_window
        self.audio_window = audio_window

        self.send_button = tk.Button(
            self.master,
            text="Apply",
            command=self.update_text_window,
        )
        self.send_button.pack()

    def update_text_window(self):
        self.text = self.text_input.get("1.0", "end-1c")
        self.sentences = nltk.sent_tokenize(self.text)
        self.text_window.text_widget.delete("1.0", "end")
        self.text_window.text_widget.insert("1.0", self.text_input.get("1.0", "end-1c"))
        self.audio_window.sentences = self.sentences
