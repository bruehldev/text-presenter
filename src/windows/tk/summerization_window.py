from tkinter import ttk, Text, NORMAL, DISABLED, END
from src.windows.tk.base_window import BaseWindow
from src.services.text_summerization import summarize
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")


class SummerizationWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(
            master, "Summerization Window", "config/summerization_window.conf"
        )
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)
        self.keyphrases = []
        self.text = ""

        self.text_widget = Text(self.frame, wrap="word")
        self.text_widget.configure(bg="black", fg="white")
        self.text_widget.pack(fill="both", expand=True)

        self.text_widget.config(state=DISABLED)

    def summarize(self, text):
        self.text = text
        summary_text = summarize(text)
        self.update_text_display(summary_text)

        sentences = nltk.sent_tokenize(summary_text)
        important_words = []
        for sentence in sentences:
            # Tokenize the sentence and keep track of the original positions of the words
            words_with_positions = [
                (word, i) for i, word in enumerate(nltk.word_tokenize(sentence))
            ]

            # Remove stop words and punctuation
            words_with_positions = [
                (word, pos)
                for word, pos in words_with_positions
                if word not in stopwords.words("english") and word.isalpha()
            ]

            # Initialize the list of important words for this sentence
            important_words_for_sentence = []

            # Iterate over the words and their original positions
            for i in range(len(words_with_positions)):
                word, pos = words_with_positions[i]

                # If this is not the last word and the next word is consecutive in the original sentence, join them together
                if (
                    i < len(words_with_positions) - 1
                    and words_with_positions[i + 1][1] == pos + 1
                ):
                    word += " " + words_with_positions[i + 1][0]
                    important_words_for_sentence.append(word)
                    continue

                important_words_for_sentence.append(word)

            important_words.append(important_words_for_sentence)

        # merge important words and create set
        merged_important_words = set()
        for words in important_words:
            for word in words:
                merged_important_words.add(word)

        return merged_important_words

    def update_text_display(self, text):
        self.text_widget.config(state=NORMAL)
        self.text_widget.delete("1.0", END)
        self.text_widget.insert("1.0", text)
        self.text_widget.config(state=DISABLED)
