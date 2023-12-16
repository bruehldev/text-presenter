import os
import tkinter as tk
from tkinter import messagebox
from tts_manager import generate_tts
from audio_manager import stop_audio, play_audio_file
from src.windows.tk.base_window import BaseWindow


class AudioWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Audio Window", "config/audio_window.conf")
        self.sentences = None
        print(self.sentences)
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
            command=lambda: self.process_text(self.sentences),
        )
        self.process_button.pack()

    def play_audio(self):
        # play every audio file in the folder
        folder = "audios"
        audio_files = os.listdir(folder)
        audio_files.sort()

        for index, filename in enumerate(audio_files):
            file = os.path.join(folder, filename)
            print(self.sentences[index])
            print(file)

            play_audio_file(file)

        # print also sentence

    def stop_audio(self):
        stop_audio()

    def process_text(self, sentences):
        if sentences is None:
            messagebox.showerror("No Text", "No text to process!")
            return
        generate_tts(sentences)
        messagebox.showinfo("TTS Generated", "TTS audio generated successfully!")
