from tkinter import ttk
from src.windows.tk.base_window import BaseWindow
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from cycler import cycler


class PlotWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Plot", "config/plot.conf")
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)
        self.sentence_structure = None
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
        all_colors = []
        all_sizes = []
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
                all_colors.append(cluster_label)
                all_sizes.append(occurrence * 20)
                all_labels.append(word)

        plt.scatter(
            *zip(*all_embeddings),
            s=all_sizes,
            c=all_colors,
            cmap="viridis",
            marker=marker
        )
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
