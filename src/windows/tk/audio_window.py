import os
import tkinter as tk
from tkinter import messagebox
from src.services.tts_manager import generate_tts, generate_tts_title
from src.services.audio_manager import (
    stop_audio,
    play_audio_file,
    delete_audio_files,
    play_audio_file_channel,
    stop_audio_channel,
)
from src.windows.tk.base_window import BaseWindow


class AudioWindow(BaseWindow):
    def __init__(
        self,
        master,
        target_text_widget,
        target_word_window,
        target_word_label,
        speed,
    ):
        super().__init__(master, "Audio Window", "config/audio_window.conf")
        self.title = None
        self.sentences = None
        self.target_text_widget = target_text_widget
        self.target_word_window = target_word_window
        self.target_word_label = target_word_label
        self.speed = speed

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
            command=lambda: self.generate_audio(self.sentences, self.title),
        )
        self.process_button.pack()

    def play_audio(self):
        # play every audio file in the folder
        folder = "audios/sentences"
        audio_files = os.listdir(folder)
        audio_files.sort()

        # update rsvp with title
        self.target_word_label.config(text="Title: " + self.title)
        self.target_word_window.update()

        # play title
        # play_audio_file_channel(f"{folder}/title.wav")

        for index, filename in enumerate(audio_files):
            file = os.path.join(folder, filename)
            # update rsvp with sentence
            self.target_word_label.config(text=self.sentences[index])
            self.target_word_window.update()

            # update text widget with highlighted sentence
            pointer_start = "1.0"
            pointer_end = "1.0"
            sentence = self.sentences[index]
            pointer_start = self.target_text_widget.search(
                sentence, pointer_end, stopindex="end"
            )
            pointer_end = f"{pointer_start}+{len(sentence)}c"

            self.target_text_widget.tag_add("highlight", pointer_start, pointer_end)

            self.target_text_widget.tag_config("highlight", background="yellow")

            # unmark previous sentence
            if index > 0:
                self.target_text_widget.tag_remove(
                    "highlight",
                    f"{pointer_start}-{len(self.sentences[index-1])+2}c",
                    pointer_start,
                )
            self.target_text_widget.pack()
            self.target_text_widget.update()

            play_audio_file_channel(file)

        # remove highlight
        self.target_text_widget.tag_remove("highlight", "1.0", "end")

    def stop_audio(self):
        stop_audio()

    def generate_audio(self, sentences, title):
        # delete previous audio files
        delete_audio_files()

        if sentences is None:
            messagebox.showerror("No Text", "No text to process!")
            return
        generate_tts(sentences)
        generate_tts_title(title)
        messagebox.showinfo("TTS Generated", "TTS audio generated successfully!")
