from tkinter import ttk, NORMAL, DISABLED, IntVar, NORMAL, Text, END, DISABLED
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
import random


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
        rsvp_window,
        summerization_window,
    ):
        super().__init__(master, "Text Input", "config/text_input.conf")
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)
        self.keyphrases = None
        self.rsvp_window = rsvp_window
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
        self.summerization_window = summerization_window
        self.audio_window = audio_window
        self.information_window = information_window
        self.qa_window = qa_window
        self.plot_window = plot_window

        self.load_checkbox_states()

        self.audio_processing_var = IntVar(value=self.audio_checkbox_state)
        self.information_processing_var = IntVar(value=self.information_checkbox_state)
        self.topic_clustering_var = IntVar(value=self.information_checkbox_state)
        self.summerization_var = IntVar(value=self.summerization_checkbox_state)

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
        ttk.Checkbutton(
            self.frame,
            text="Topic Clustering",
            variable=self.topic_clustering_var,
            command=self.save_checkbox_states,
        ).pack()
        ttk.Checkbutton(
            self.frame,
            text="Summerization",
            variable=self.summerization_var,
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

        self.summerization_checkbox_state = get_config_parameter(
            "text_input", "summerization"
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

        # set summerization checkbox
        set_config_parameter(
            "text_input", "summerization", self.summerization_var.get()
        )

    def process_text(self):
        # check if text is to short
        min_text_length = 50
        print(len(self.text_input.get("1.0", END)))
        if len(self.text_input.get("1.0", END)) < min_text_length:
            messagebox.showerror(
                "Error",
                f"Text is to short. Please enter at least {min_text_length} characters.",
            )
            return

        # reset previous processing
        self.text_window.reset()
        self.audio_window.reset()
        self.information_window.reset()
        self.plot_window.reset()
        self.rsvp_window.reset()
        self.qa_window.reset()
        self.summerization_window.reset()

        self.update_text_display()

        # Update selected processing steps

        ### Audio ###
        if self.audio_processing_var.get():
            self.audio_window.generate_audio(self.sentences, self.title)

        ### Information Retrieval ###
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

            # remove stop words,  punctuation and other special characters for each sentence
            sentences_without_stopwords = []
            for sentence in self.sentences:
                words = word_tokenize(sentence)
                filtered_words = [
                    word for word in words if word.lower() not in stop_words
                ]
                filtered_words = [word for word in filtered_words if word.isalpha()]
                # make set
                filtered_words_set = set(filtered_words)
                sentences_without_stopwords.append(filtered_words_set)

            # TF-IDF
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform([text_without_stopwords])
            feature_names = tfidf_vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()[0]
            features_and_scores = list(zip(feature_names, tfidf_scores))
            sorted_features = sorted(
                features_and_scores, key=lambda x: x[1], reverse=True
            )
            # TODO use sorted_features
            # print(sorted_features)

            freq_dist_without_stopwords = FreqDist(text_without_stopwords_tokens)
            self.information_window.frequent_words = (
                freq_dist_without_stopwords.most_common()
            )

            # extract and set keyphrases
            self.keyphrases = extract_keyphrases(self.text)
            self.information_window.keyphrases = self.keyphrases
            self.text_window.keyphrases = self.keyphrases
            self.rsvp_window.keyphrases = self.keyphrases
            self.text_window.underline_keyphrases()

            # generate and set headline
            headline = generate_headline(self.text)
            self.text_window.headline.config(text=headline)
            self.text_window.master.update()
            self.audio_window.title = headline

            # update information window
            self.information_window.dropdown_var.set("Keyphrases")
            self.information_window.on_dropdown_change(None)
            self.information_window.master.update()
            # self.process_information()

        ### Topic Clustering ###
        if self.topic_clustering_var.get():
            self.sentence_structure = {}
            # update plot window
            words_and_embeddings = get_words_and_embeddings(self.text)

            # remove stop words and special characters from word_and_embeddigs
            for word in list(words_and_embeddings.keys()):
                if word.lower() in stop_words:
                    del words_and_embeddings[word]
                elif not word.isalpha():
                    del words_and_embeddings[word]

            cluster_labels = get_cluster_labels(words_and_embeddings)
            key_list = list(words_and_embeddings.keys())

            for index, sentence in enumerate(self.sentences):
                words = []
                cluster = []
                embeddings = []
                occurrences = []
                for word in words_and_embeddings.keys():
                    if word.lower() in sentence.lower():
                        words.append(word)
                        cluster.append(cluster_labels[key_list.index(word)])
                        embeddings.append(words_and_embeddings[word])

                        # if word occurs in this or previous sentences, add 1 to occurrences
                        occurrences.append(
                            len(
                                [
                                    sentence
                                    for sentence in self.sentences[: index + 1]
                                    if word in sentence.lower()
                                ]
                            )
                        )

                self.sentence_structure[index] = {
                    "words": words,
                    "cluster_labels": cluster,
                    "embeddings": embeddings,
                    "occurrences": occurrences,
                }

            # give each cluster a name based on the occurrence of the word. If multiple words have the same occurrence, pick 2 random words as title
            cluster_name_mappings = {}
            for sentence in self.sentence_structure.values():
                for word, cluster_label, occurrence in zip(
                    sentence["words"],
                    sentence["cluster_labels"],
                    sentence["occurrences"],
                ):
                    if cluster_label == -1:
                        continue
                    if cluster_label not in cluster_name_mappings.keys():
                        cluster_name_mappings[cluster_label] = {}
                    if occurrence not in cluster_name_mappings[cluster_label].keys():
                        cluster_name_mappings[cluster_label][occurrence] = []
                    cluster_name_mappings[cluster_label][occurrence].append(word)

            # print("cluster_name_mappings")
            # print(cluster_name_mappings)

            for cluster_label, occurrences in cluster_name_mappings.items():
                # get the most common occurrence
                most_common_occurrence = max(occurrences.keys())
                # get the words with the most common occurrence
                words_with_most_common_occurrence = occurrences[most_common_occurrence]
                # pick 2 random words
                if len(words_with_most_common_occurrence) > 2:
                    random.shuffle(words_with_most_common_occurrence)
                    words_with_most_common_occurrence = (
                        words_with_most_common_occurrence[:2]
                    )
                # join the words
                cluster_name = " ".join(words_with_most_common_occurrence)
                cluster_name_mappings[cluster_label] = cluster_name

            # if sentence has keyphrase, overwrite cluster name mapping of sentence
            for index, sentence in enumerate(self.sentences):
                for keyphrase in self.keyphrases:
                    if keyphrase.lower() in sentence.lower():
                        cluster_name_mappings[index] = keyphrase
                        break

            # add outliers
            cluster_name_mappings[-1] = "Outliers"
            print("cluster_name_mappings")
            print(cluster_name_mappings)

            # add topics from cluster names to information window except outliers
            self.information_window.topics = [
                topic for topic in cluster_name_mappings.values() if topic != "Outliers"
            ]

            # print each word in word_and_embeddigs
            # for word in words_and_embeddings.keys():
            # print(word)

            self.plot_window.word_to_embedding = words_and_embeddings
            self.plot_window.cluster_labels = cluster_labels
            self.plot_window.sentence_structure = self.sentence_structure
            self.text_window.sentence_structure = self.sentence_structure
            self.rsvp_window.sentence_structure = self.sentence_structure
            self.text_window.highlight_words()
            self.plot_window.cluster_name_mappings = cluster_name_mappings
            self.plot_window.figure = self.plot_window.plot_embeddings(True)

        ### Summerization ###
        if self.summerization_var.get():
            possible_bulletpoint = self.summerization_window.summarize(self.text)

            # Add bulletpoint information to information window
            self.information_window.bulletpoints = possible_bulletpoint
            # change view to bulletpoints when information retrieval is off
            if not self.information_processing_var.get():
                self.information_window.dropdown_var.set("Bulletpoints")
                self.information_window.on_dropdown_change(None)
                self.information_window.master.update()

        messagebox.showinfo("Done", "Text processed!")

    def update_text_display(self):
        # TODO: delete audio files or use Apply to Process Audio. I keep it for faster testing
        # TODO: make any processing window optional. Open/Close windows which are selected
        # delete_audio_files()
        self.text = self.text_input.get("1.0", "end-1c")
        self.sentences = nltk.sent_tokenize(self.text)
        self.text_window.update_text_display(self.text)
        self.audio_window.sentences = self.sentences
        # update question answer window
        self.qa_window.text = self.text
