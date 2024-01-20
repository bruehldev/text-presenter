from tkinter import (
    ttk,
    BOTH,
    END,
    Text,
    DISABLED,
    NORMAL,
)

from src.windows.tk.base_window import BaseWindow
from src.services.config_manager import get_config_parameter, set_config_parameter


class rsvpWindow(BaseWindow):
    def __init__(self, master, color_dict):
        super().__init__(master, "rsvp Window", "config/rsvp_window.conf")
        # Frame to hold the label with a border
        self.frame = ttk.Frame(self.master, padding=10, border=1)
        self.frame.pack(fill=BOTH, expand=True)

        self.keyphrases = ["sentence", "testing", "screen"]
        self.text = "A sentence example for testing the font size and window; it's quite lengthy, demonstrating how the feature adjusts text in the Tkinter window to fit the screen size."
        self.color_dict = color_dict
        self.sentence_structure = None

        self.font_size = 24

        self.word_text = Text(
            self.frame,
            font=("Helvetica", self.font_size),
            wrap="word",
            width=50,
            height=2,
        )
        self.word_text.configure(bg="black", fg="white")

        self.update_text_display(self.text)
        self.underline_keyphrases()
        self.load_font_size()
        self.word_text.pack(fill=BOTH, expand=True)
        self.word_text.config(state=DISABLED)

    def update_text_display(self, text):
        self.word_text.config(state=NORMAL)
        self.word_text.delete("1.0", END)
        self.word_text.insert(END, text)

    def underline_keyphrases(self):
        if self.keyphrases is not None:
            # configure the "underline" tag
            self.word_text.tag_config("underline", underline=True)

            # underline keyphrases in text widget
            for keyphrase in self.keyphrases:
                start_idx = "1.0"
                while True:
                    start_idx = self.word_text.search(
                        r"\y" + keyphrase + r"\y",
                        start_idx,
                        stopindex=END,
                        regexp=True,
                    )
                    if not start_idx:
                        break
                    end_idx = f"{start_idx}+{len(keyphrase)}c"
                    self.word_text.tag_add("underline", start_idx, end_idx)
                    start_idx = end_idx

    def highlight_words(self):
        print("highlight_words")
        print(self.sentence_structure)
        if self.sentence_structure is None:
            return
        for sentence in self.sentence_structure.values():
            words = sentence["words"]
            cluster_labels = sentence["cluster_labels"]
            for word, cluster_label in zip(words, cluster_labels):
                if cluster_label == -1:
                    continue
                self.word_text.tag_config(
                    cluster_label,
                    background=self.color_dict[cluster_label],
                )
                start_idx = "1.0"
                while True:
                    start_idx = self.word_text.search(
                        r"\y" + word + r"\y",
                        start_idx,
                        stopindex=END,
                        regexp=True,
                    )
                    if not start_idx:
                        break
                    end_idx = f"{start_idx}+{len(word)}c"
                    self.word_text.tag_add(cluster_label, start_idx, end_idx)
                    start_idx = end_idx

    def increase_text_size(self):
        self.font_size += 2
        self.word_text.config(font=("Helvetica", self.font_size))
        self.save_font_size()

    def decrease_text_size(self):
        if self.font_size > 2:
            self.font_size -= 2
            self.word_text.config(font=("Helvetica", self.font_size))
            self.save_font_size()

    def save_font_size(self):
        set_config_parameter("rsvp_window", "font_size", self.font_size)

    def load_font_size(self):
        loaded_font_size = get_config_parameter("rsvp_window", "font_size")
        if loaded_font_size is not None:
            self.font_size = loaded_font_size
            self.word_text.config(font=("Helvetica", self.font_size))
