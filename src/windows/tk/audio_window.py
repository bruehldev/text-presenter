import os
import threading
from tkinter import ttk, StringVar, BOTTOM, NORMAL, DISABLED
from tkinter import messagebox
from src.services.tts_manager import generate_tts, generate_tts_title, get_model_names
from src.services.audio_manager import (
    play_audio_file,
    delete_audio_files,
    play_audio_file_channel,
    stop_audio_channel,
)
from src.windows.tk.base_window import BaseWindow
from src.services.config_manager import get_config_parameter, set_config_parameter


class AudioWindow(BaseWindow):
    def __init__(
        self,
        master,
        target_text_widget,
        target_rsvp_window,
        target_plot_window,
    ):
        super().__init__(master, "Audio Window", "config/audio_window.conf")
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)
        self.audio_thread = None
        self.title = None
        self.sentences = None
        self.target_text_widget = target_text_widget
        self.target_rsvp_window = target_rsvp_window
        self.target_plot_window = target_plot_window
        self.stop_audio = False

        # Dropdown to select the model
        self.model_names = get_model_names()
        self.selected_model = StringVar()
        self.load_model_name()
        self.model_dropdown = ttk.Combobox(
            self.frame,
            textvariable=self.selected_model,
            values=self.model_names,
            state="readonly",
            width=50,
        )
        self.model_dropdown.pack()

        self.model_dropdown.bind(
            "<<ComboboxSelected>>", lambda event: self.save_model_name()
        )

        self.play_button = ttk.Button(
            self.frame,
            text="Play",
            command=lambda: self.play_audio(),
        )
        self.play_button.pack()

        self.stop_button = ttk.Button(
            self.frame,
            text="Stop",
            command=lambda: self.stop_audio_thread(),
        )
        self.stop_button.pack()

        self.process_button = ttk.Button(
            self.frame,
            text="Process",
            command=lambda: self.generate_audio(self.sentences, self.title),
        )
        self.process_button.pack()

        # Label to display font size
        self.font_size_label = ttk.Label(
            self.frame, text=f"Text Size: {self.target_rsvp_window.font_size}"
        )
        self.font_size_label.pack(side=BOTTOM)

        # Button to decrease text size
        self.decrease_text_size_button = ttk.Button(
            self.frame, text="Decrease Text Size", command=self.decrease_text_size
        )
        self.decrease_text_size_button.pack(side=BOTTOM)

        # Button to increase text size
        self.increase_text_size_button = ttk.Button(
            self.frame, text="Increase Text Size", command=self.increase_text_size
        )
        self.increase_text_size_button.pack(side=BOTTOM)

    def update_font_size_label(self):
        self.font_size_label.config(
            text=f"Text Size: {self.target_rsvp_window.font_size}"
        )

    def increase_text_size(self):
        self.target_rsvp_window.increase_text_size()
        self.update_font_size_label()

    def decrease_text_size(self):
        self.target_rsvp_window.decrease_text_size()
        self.update_font_size_label()

    def load_model_name(self):
        self.selected_model.set(get_config_parameter("audio_window", "model_name"))

    def save_model_name(self):
        set_config_parameter("audio_window", "model_name", self.selected_model.get())

    def _play_audio_files_thread(self, audio_files, folder):
        # only use sentences_structure

        for index, filename in enumerate(audio_files):
            file = os.path.join(folder, filename)

            if self.sentences is None:
                messagebox.showerror("No Text", "No text to process!")
                return
            # update rsvp
            sentence = self.sentences[index]
            self.target_rsvp_window.update_text_display(sentence)
            self.target_rsvp_window.underline_keyphrases()
            self.target_rsvp_window.highlight_words()

            # update text widget with highlighted sentence
            pointer_start = "1.0"
            pointer_end = "1.0"
            sentence = self.sentences[index]
            pointer_start = self.target_text_widget.search(
                sentence, pointer_end, stopindex="end"
            )
            pointer_end = f"{pointer_start}+{len(sentence)}c"

            self.target_text_widget.tag_add("highlight", pointer_start, pointer_end)

            self.target_text_widget.tag_config("highlight", background="#646e6d")

            #  plot
            self.target_plot_window.plot_embeddings(
                True, marker="o", sentence_range=index
            )

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
            if self.stop_audio:
                break

        # remove highlight
        self.target_text_widget.tag_remove("highlight", "1.0", "end")

        self.stop_audio = False
        self.audio_thread = None

    def play_audio(self):
        # play every audio file in the folder
        folder = "audios/sentences"
        if not os.path.exists(folder):
            os.makedirs(folder)
        audio_files = os.listdir(folder)
        if len(audio_files) == 0:
            messagebox.showerror("No Audio", "No audio to play!")
            return
        audio_files.sort()

        # update rsvp with title
        # self.target_rsvp_window.word_text.delete("1.0", "end")
        # self.target_rsvp_window.word_text.insert("1.0", self.title)
        # self.target_rsvp_window.word_text.config(text=self.title)

        self.target_rsvp_window.master.update()

        # play title
        # play_audio_file_channel(f"{folder}/title.wav")
        self.audio_thread = threading.Thread(
            target=self._play_audio_files_thread, args=(audio_files, folder)
        )
        self.audio_thread.start()

    def stop_audio_thread(self):
        self.stop_audio = True
        stop_audio_channel()

    def generate_audio(self, sentences, title):
        # delete previous audio files
        delete_audio_files()

        if sentences is None:
            messagebox.showerror("No Text", "No text to process!")
            return
        generate_tts(sentences, self.selected_model.get())
        # generate_tts_title(title, self.selected_model.get())
