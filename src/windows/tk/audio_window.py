import tkinter as tk
from tkinter import messagebox, ttk
from tts_manager import generate_tts
from audio_manager import play_audio, stop_audio
from src.windows.tk.base_window import BaseWindow


class AudioWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Audio Window", "config/audio_window.conf")
        self.words = None
        print(self.words)
        self.play_button = tk.Button(
            self.master,
            text="Play",
            command=lambda: self.play_audio(),
        )
        self.play_button.pack()

        self.stop_button = tk.Button(
            self.master,
            text="Stop",
            command=lambda: self.stop_audio(),
        )
        self.stop_button.pack()

        self.process_button = tk.Button(
            self.master,
            text="Process",
            command=lambda: self.process_text(self.words),
        )
        self.process_button.pack()

    def play_audio(self):
        play_audio()

    def stop_audio(self):
        stop_audio()

    def process_text(self, words):
        if words is None:
            messagebox.showerror("No Text", "No text to process!")
            return
        generate_tts(words)
        messagebox.showinfo("TTS Generated", "TTS audio generated successfully!")
