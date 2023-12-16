import tkinter as tk
from src.windows.tk.base_window import BaseWindow
import nltk
from src.services.headline_generator import generate_headline
from services.audio_manager import delete_audio_files

nltk.download("punkt")


class TextInputWindow(BaseWindow):
    def __init__(self, master, text_window, audio_window):
        super().__init__(master, "Text Input", "config/text_input.conf")
        self.text_input = tk.Text(self.master, state=tk.NORMAL)
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
        # TODO: delete audio files or use Apply to Process Audio. I keep it for faster testing
        # delete_audio_files()
        self.text = self.text_input.get("1.0", "end-1c")
        self.sentences = nltk.sent_tokenize(self.text)
        self.text_window.text_widget.config(state=tk.NORMAL)
        self.text_window.text_widget.delete("1.0", "end")
        self.text_window.text_widget.insert("1.0", self.text_input.get("1.0", "end-1c"))
        self.text_window.text_widget.config(state=tk.DISABLED)
        self.audio_window.sentences = self.sentences

        # generate headline
        headline = generate_headline(self.text)
        self.text_window.headline.config(text=headline)
        self.text_window.master.update()
