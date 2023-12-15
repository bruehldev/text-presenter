import tkinter as tk
from tkinter import messagebox, ttk
from tts_manager import generate_tts
from src.windows.tk.base_window import BaseWindow


class TextWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Text Presenter", "config/root.conf")
        self.text_input = None
        self.process_button = None
        self.play_window = None
        self.word_display_window = None
        self.processed_text_window = None

    def create_window(self):
        super().create_window()
        self.text_input = tk.Text(self.top_level)
        self.text_input.pack()

        self.process_button = tk.Button(
            self.top_level,
            text="Process",
            command=lambda: self.process_text(
                self.text_input.get("1.0", "end-1c"),
            ),
        )
        self.process_button.pack()
        self.bind_configure_and_save_size()

    def process_text(self, words):
        generate_tts(words)
        messagebox.showinfo("TTS Generated", "TTS audio generated successfully!")
