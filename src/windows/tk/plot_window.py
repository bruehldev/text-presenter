import tkinter as tk
from tkinter import ttk
from src.windows.tk.base_window import BaseWindow
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class PlotWindow(BaseWindow):
    def __init__(self, master, word_to_embedding, cluster_labels):
        super().__init__(master, "Plot", "config/plot.conf")
        self.word_to_embedding = word_to_embedding
        self.cluster_labels = cluster_labels
        self.figure = self.plot_embeddings(False)

    def plot_embeddings(self, override=False):
        # delete the old plot
        if override:
            self.figure.clf()
            plt.close(self.figure)
            self.canvas.get_tk_widget().destroy()

        figure = plt.figure()
        if len(self.word_to_embedding) == 0:
            return figure
        plt.scatter(
            [emb[0] for emb in self.word_to_embedding.values()],
            [emb[1] for emb in self.word_to_embedding.values()],
            c=self.cluster_labels,
        )

        # Annotate the plot with the words
        for i, word in enumerate(self.word_to_embedding.keys()):
            plt.annotate(word, list(self.word_to_embedding.values())[i])

        self.figure = figure
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        return figure
