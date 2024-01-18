from tkinter import ttk, NORMAL, DISABLED, IntVar, NORMAL, Text
from src.windows.tk.base_window import BaseWindow
import nltk
from src.services.headline_generator import generate_headline
from src.services.keyphrase_extraction import extract_keyphrases
from src.services.embeddings_manager import get_words_and_embeddings, get_cluster_labels
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from src.services.config_manager import get_config_parameter, set_config_parameter
from sklearn.feature_extraction.text import TfidfVectorizer
from tkinter import messagebox


nltk.download("punkt")
nltk.download("stopwords")


class TextInputWindow(BaseWindow):
    def __init__(
        self,
        master,
        text_window,
        audio_window,
        information_window,
        qa_window,
        plot_window,
    ):
        super().__init__(master, "Text Input", "config/text_input.conf")
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)
        bg_color = self.master.winfo_toplevel().cget("bg")
        self.text_input = Text(
            self.frame,
            state=NORMAL,
            background=bg_color,
            foreground="black",
            wrap="word",
        )
        self.text_input.pack(fill="both", expand=True)
        self.text_window = text_window
        self.audio_window = audio_window
        self.information_window = information_window
        self.qa_window = qa_window
        self.plot_window = plot_window

        self.load_checkbox_states()

        self.audio_processing_var = IntVar(value=self.audio_checkbox_state)
        self.information_processing_var = IntVar(value=self.information_checkbox_state)
        self.topic_clustering_var = IntVar(value=self.information_checkbox_state)

        # Checkboxes for processing windows
        ttk.Checkbutton(
            self.frame,
            text="Generate Audio",
            variable=self.audio_processing_var,
            command=self.save_checkbox_states,
        ).pack()
        ttk.Checkbutton(
            self.frame,
            text="Information Retrieval",
            variable=self.information_processing_var,
            command=self.save_checkbox_states,
        ).pack()
        topic_clustering_checkbox = ttk.Checkbutton(
            self.frame,
            text="Topic Clustering",
            variable=self.topic_clustering_var,
            command=self.save_checkbox_states,
        ).pack()

        self.send_button = ttk.Button(
            self.frame,
            text="Apply",
            command=self.process_text,
        )
        self.send_button.pack()

    def load_checkbox_states(self):
        self.audio_checkbox_state = get_config_parameter(
            "text_input", "audio_processing"
        )
        self.information_checkbox_state = get_config_parameter(
            "text_input", "information_processing"
        )
        # set topic clustering checkbox to 1 if information processing is 1
        if self.information_checkbox_state == 0:
            self.topic_clustering_checkbox_state = 0

            self.topic_clustering_checkbox_state = get_config_parameter(
                "text_input", "topic_clustering"
            )

    def save_checkbox_states(self):
        set_config_parameter(
            "text_input", "audio_processing", self.audio_processing_var.get()
        )
        set_config_parameter(
            "text_input",
            "information_processing",
            self.information_processing_var.get(),
        )
        # if information processing is 1, set topic clustering to 1
        if self.information_processing_var.get() == 0:
            set_config_parameter("text_input", "topic_clustering", 0)
            # update checkbox
            self.topic_clustering_var.set(0)

    def process_text(self):
        self.update_text_display()

        # Update selected processing steps
        if self.audio_processing_var.get():
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

            # TF-IDF
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform([text_without_stopwords])
            feature_names = tfidf_vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()[0]
            features_and_scores = list(zip(feature_names, tfidf_scores))
            sorted_features = sorted(
                features_and_scores, key=lambda x: x[1], reverse=True
            )
            print(sorted_features)

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
        if self.topic_clustering_var.get():
            # update plot window
            word_and_embeddigs = get_words_and_embeddings(text_without_stopwords)
            cluster_labels = get_cluster_labels(word_and_embeddigs)
            self.plot_window.word_to_embedding = word_and_embeddigs
            self.plot_window.cluster_labels = cluster_labels
            self.plot_window.figure = self.plot_window.plot_embeddings(True)

        messagebox.showinfo("Done", "Text processed!")

    def update_text_display(self):
        # TODO: delete audio files or use Apply to Process Audio. I keep it for faster testing
        # TODO: make any processing window optional. Open/Close windows which are selected
        # delete_audio_files()
        self.text = self.text_input.get("1.0", "end-1c")
        self.sentences = nltk.sent_tokenize(self.text)
        self.text_window.text_widget.config(state=NORMAL)
        self.text_window.text_widget.delete("1.0", "end")
        self.text_window.text_widget.insert("1.0", self.text_input.get("1.0", "end-1c"))
        self.text_window.text_widget.config(state=DISABLED)
        self.audio_window.sentences = self.sentences
        # update question answer window
        self.qa_window.text = self.text_input.get("1.0", "end-1c")
