import tkinter as tk
from src.windows.tk.base_window import BaseWindow
import nltk
from src.services.headline_generator import generate_headline
from src.services.audio_manager import delete_audio_files
from src.services.keyphrase_extraction import extract_keyphrases
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import FreqDist

nltk.download("punkt")


class TextInputWindow(BaseWindow):
    def __init__(self, master, text_window, audio_window, information_window):
        super().__init__(master, "Text Input", "config/text_input.conf")
        self.text_input = tk.Text(self.master, state=tk.NORMAL)
        self.text_input.pack()
        self.text_window = text_window
        self.audio_window = audio_window
        self.information_window = information_window

        self.audio_processing_var = tk.IntVar()
        self.information_processing_var = tk.IntVar()

        # Checkboxes for processing windows
        tk.Checkbutton(
            self.master, text="Generate Audio", variable=self.audio_processing_var
        ).pack()
        tk.Checkbutton(
            self.master,
            text="Information Retrival",
            variable=self.information_processing_var,
        ).pack()

        self.send_button = tk.Button(
            self.master,
            text="Apply",
            command=self.update_text_window,
        )
        self.send_button.pack()

    def update_text_window(self):
        # Check the state of checkboxes before processing
        self.process_text()

        if self.audio_processing_var.get():
            # self.process_audio()
            self.audio_window.sentences = self.sentences
            self.audio_window.generate_audio(self.sentences, self.title)

        if self.information_processing_var.get():
            # extract and set frequent words
            words = word_tokenize(self.text)
            stop_words = set(stopwords.words("english"))
            # remove stop words
            filtered_words = [word for word in words if word.lower() not in stop_words]
            # remove punctuation and other special characters
            filtered_words = [word for word in filtered_words if word.isalpha()]
            text_without_stopwords = " ".join(filtered_words)
            text_without_stopwords_tokens = word_tokenize(text_without_stopwords)
            freq_dist_without_stopwords = FreqDist(text_without_stopwords_tokens)
            self.information_window.frequent_words = (
                freq_dist_without_stopwords.most_common()
            )

            # extract and set keyphrases
            keyphrases = extract_keyphrases(self.text)
            self.information_window.keyphrases = keyphrases

            # generate and set headline
            headline = generate_headline(self.text)
            self.text_window.headline.config(text=headline)
            self.text_window.master.update()
            self.audio_window.title = headline

            # update information window
            self.information_window.on_dropdown_change(None)
            self.information_window.master.update()
            # self.process_information()

    def process_text(self):
        # TODO: delete audio files or use Apply to Process Audio. I keep it for faster testing
        # TODO: make any processing window optional. Open/Close windows which are selected
        # delete_audio_files()
        self.text = self.text_input.get("1.0", "end-1c")
        self.sentences = nltk.sent_tokenize(self.text)
        self.text_window.text_widget.config(state=tk.NORMAL)
        self.text_window.text_widget.delete("1.0", "end")
        self.text_window.text_widget.insert("1.0", self.text_input.get("1.0", "end-1c"))
        self.text_window.text_widget.config(state=tk.DISABLED)
