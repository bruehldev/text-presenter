from tkinter import ttk

import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from src.windows.tk.base_window import BaseWindow


class PlotWindow(BaseWindow):
    def __init__(self, master, color_dict):
        super().__init__(master, "Plot", "config/plot.conf")
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)
        self.color_dict = color_dict
        self.sentence_structure = None
        self.cluster_name_mappings = None
        # {1: 'name', 0: 'using', 3: 'word', 2: 'tf'}
        self.canvas = None
        self.figure = self.plot_embeddings(False)

    def get_range_from_dict(self, d, start, end):
        return {k: v for k, v in d.items() if start <= k <= end}

    def plot_embeddings(self, override=False, marker="o", sentence_range=None):
        # delete the old plot
        if override:
            self.destroy_plot()

        figure = plt.figure()
        if self.sentence_structure is None:
            return figure

        # TODO Rrmove this?
        # Define the color cycle
        color_cycle = cycler(color=["red", "green", "blue", "orange"])

        # Set the color cycle for the current axes
        plt.gca().set_prop_cycle(color_cycle)

        # determine which sentences to plot with range 0 till sentence_range
        sentences_to_plot = (
            self.sentence_structure.values()
            if sentence_range is None
            else self.get_range_from_dict(
                self.sentence_structure, 0, sentence_range
            ).values()
        )
        # print("sentences_to_plot")
        # print(sentences_to_plot)

        all_embeddings = []
        all_cluster = []
        all_occurrences = []
        all_labels = []

        for sentence in sentences_to_plot:
            words = sentence["words"]
            embeddings = sentence["embeddings"]
            occurrences = sentence["occurrences"]
            cluster_labels = sentence["cluster_labels"]

            for word, embedding, occurrence, cluster_label in zip(
                words, embeddings, occurrences, cluster_labels
            ):
                all_embeddings.append(embedding)
                all_cluster.append(cluster_label)
                all_occurrences.append(occurrence * 20)
                all_labels.append(word)

        # scatter for each cluster and -1
        for cluster in set(all_cluster):
            cluster_embeddings = []
            cluster_occurrences = []
            cluster_labels = []
            for embedding, occurrence, cluster_label in zip(
                all_embeddings, all_occurrences, all_cluster
            ):
                if cluster_label == cluster:
                    cluster_embeddings.append(embedding)
                    cluster_occurrences.append(occurrence)
                    cluster_labels.append(cluster_label)

            # if cluster occurrence is 0 (different spelling as token), set it to 20
            cluster_occurrences = [
                occurrence if occurrence > 0 else 20
                for occurrence in cluster_occurrences
            ]
            plt.scatter(
                *zip(*cluster_embeddings),
                s=cluster_occurrences,
                c=[self.color_dict.get(label, "gray") for label in cluster_labels],
                marker=marker,
                label=self.cluster_name_mappings[cluster],
            )

        plt.legend(loc="best", fontsize=7)

        for label, (x, y) in zip(all_labels, all_embeddings):
            plt.text(x, y, label, fontsize=9)

        self.figure = figure
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)

        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, self.frame)
        toolbar.update()

        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        return figure

    def destroy_plot(self):
        if self.canvas is None:
            return
        self.figure.clf()
        plt.close(self.figure)
        self.canvas.get_tk_widget().destroy()
        self.canvas = None
        # delete old navigation toolbar
        for child in self.frame.winfo_children():
            if isinstance(child, NavigationToolbar2Tk):
                child.destroy()

    def reset(self):
        self.destroy_plot()
        self.sentence_structure = None
        self.cluster_name_mappings = None
        self.canvas = None
        self.figure = self.plot_embeddings(False)
