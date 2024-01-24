from tkinter import (BOTTOM, BooleanVar, DoubleVar, S, Toplevel, W, messagebox,
                     ttk)

from src.windows.tk.audio_window import AudioWindow
from src.windows.tk.base_window import BaseWindow
from src.windows.tk.information_window import InformationWindow
from src.windows.tk.plot_window import PlotWindow
from src.windows.tk.qa_window import QAWindow
from src.windows.tk.rsvp_window import rsvpWindow
from src.windows.tk.summerization_window import SummerizationWindow
from src.windows.tk.text_input import TextInputWindow
from src.windows.tk.text_window import TextWindow

# Color dict for clustering - Add more colors as needed
color_dict = {
    -1: "gray",
    0: "green",
    1: "blue",
    2: "red",
    3: "orange",
    4: "purple",
    5: "brown",
    6: "pink",
    7: "olive",
    8: "cyan",
    9: "magenta",
    10: "yellow",
    11: "black",
    12: "lightblue",
    13: "lightgreen",
    14: "lightgray",
    15: "darkblue",
    16: "darkgreen",
}


class MainWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Window options", "config/root.conf")
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)
        # Text Window
        self.text_window = TextWindow(Toplevel(self.master), color_dict)
        self.text_window_button = ttk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_text_window_button("Text Window"),
        )
        if self.text_window.master.state() == "normal":
            self.text_window_button.config(text=f"Close Text")
        else:
            self.text_window_button.config(text="Open Text")
        self.text_window_button

        # Summerization Window
        self.summerization_window = SummerizationWindow(Toplevel(self.master))
        self.summerization_window_button = ttk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_summerization_window_button("Summerization"),
        )
        if self.summerization_window.master.state() == "normal":
            self.summerization_window_button.config(text=f"Close Summerization")
        else:
            self.summerization_window_button.config(text="Open Summerization")
        self.summerization_window_button

        # Question Answer Window
        self.qa_window = QAWindow(Toplevel(self.master))
        self.qa_window_button = ttk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_qa_window_button("QA"),
        )
        if self.qa_window.master.state() == "normal":
            self.qa_window_button.config(text=f"Close QA")
        else:
            self.qa_window_button.config(text="Open QA")
        self.qa_window_button

        # RSVP Window
        self.rsvp_window = rsvpWindow(Toplevel(self.master), color_dict)
        self.rsvp_window_button = ttk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_rsvp_window_button("RSVP"),
        )
        if self.rsvp_window.master.state() == "normal":
            self.rsvp_window_button.config(text=f"Close RSVP")
        else:
            self.rsvp_window_button.config(text="Open RSVP")
        self.rsvp_window_button

        self.word_display_running = BooleanVar()
        self.word_display_running.set(False)

        # Information Window
        self.information_window = InformationWindow(Toplevel(self.master))
        self.information_window_button = ttk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_information_window_button("Information"),
        )
        if self.information_window.master.state() == "normal":
            self.information_window_button.config(text=f"Close Information")
        else:
            self.information_window_button.config(text="Open Information")
        self.information_window_button

        # Plot Window
        self.plot_window = PlotWindow(Toplevel(self.master), color_dict)
        self.plot_window.sentence_structure = {
            "0": {
                "words": ["you"],
                "cluster_labels": [0],
                "embeddings": [[1.9070455, 1.8492087]],
                "occurrences": [1],
            }
        }.values()

        self.plot_window_button = ttk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_plot_window_button("Plot"),
        )

        if self.plot_window.master.state() == "normal":
            self.plot_window_button.config(text=f"Close Plot")
        else:
            self.plot_window_button.config(text="Open Plot")

        self.plot_window_button

        # Speed control slider
        self.speed_var = DoubleVar()
        # set middle
        self.speed_slider = ttk.Scale(
            self.frame,
            from_=3.0,
            to=13.0,
            variable=self.speed_var,
            length=400,
            orient="horizontal",
        )
        self.speed_slider.set(8.0)
        self.speed_slider

        # Audio Window
        self.audio_window = AudioWindow(
            Toplevel(self.master),
            self.text_window.text_widget,
            self.rsvp_window,
            self.plot_window,
        )
        self.audio_window_button = ttk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_audio_window_button("Audio"),
        )
        if self.audio_window.master.state() == "normal":
            self.audio_window_button.config(text=f"Close Audio")
        else:
            self.audio_window_button.config(text="Open Audio")

        self.audio_window_button

        # Text Input Window
        self.text_input_window = TextInputWindow(
            Toplevel(self.master),
            self.text_window,
            self.audio_window,
            self.information_window,
            self.qa_window,
            self.plot_window,
            self.rsvp_window,
            self.summerization_window,
        )
        self.text_input_button = ttk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_text_input_window_button("Text Input"),
        )
        if self.text_input_window.master.state() == "normal":
            self.text_input_button.config(text=f"Close Text Input")
        else:
            self.text_input_button.config(text="Open Text Input")
        self.text_input_button

        # use grid to pack buttons
        self.text_input_button.grid(row=0, column=0)
        self.text_window_button.grid(row=0, column=1)

        self.rsvp_window_button.grid(row=1, column=0)
        self.audio_window_button.grid(row=1, column=1)

        self.information_window_button.grid(row=2, column=0)
        self.plot_window_button.grid(row=2, column=1)

        self.summerization_window_button.grid(row=4, column=0)
        self.qa_window_button.grid(row=4, column=1)

        # Start display words button
        self.start_button = ttk.Button(
            self.frame,
            text="Start",
            command=lambda: self.display_words(
                self.speed_var.get(),
                self.text_input_window.text,
                self.text_window.text_widget,
                self.rsvp_window,
                self.rsvp_window.master,
            ),
        )
        # self.start_button.pack()

        # Stop display words button
        self.stop_button = ttk.Button(
            self.frame,
            text="Stop",
            command=lambda: self.stop_display_words(),
        )

        # Place Speed label, Speed slider, and Start button at the bottom
        """
        self.speed_slider.pack(side=BOTTOM, anchor=S)
        self.stop_button.pack(side=BOTTOM, anchor=S)
        self.start_button.pack(side=BOTTOM, anchor=S)
        """
        # grid
        # insert blank row
        ttk.Label(self.frame, text="").grid(row=5, column=0)
        self.start_button.grid(row=6, column=0)
        self.stop_button.grid(row=6, column=1)
        self.speed_slider.grid(row=7, column=0, columnspan=2)

    def display_words(
        self, speed, words, target_text_widget, target_word_label, target_word_window
    ):
        if words == "":
            messagebox.showerror("Error", "Please enter text to display")
            return
        # create text index
        word_pointer_start = "1.0"
        word_pointer_end = "1.0"

        self.word_display_running.set(True)

        # Iterate through words and display them
        words_split = words.split()
        for i in range(len(words_split)):
            if not self.word_display_running.get():
                break
            word = words_split[i]
            target_word_label.update_text_display(word, True)
            # underline and highlight
            target_word_label.underline_keyphrases()
            target_word_label.highlight_words()

            # use index to highlight the word in the text widget
            word_pointer_start = target_text_widget.search(
                word, word_pointer_end, stopindex="end"
            )
            word_pointer_end = f"{word_pointer_start}+{len(word)}c"

            target_text_widget.tag_add(
                "highlight", word_pointer_start, word_pointer_end
            )
            target_text_widget.tag_config("highlight", background="yellow")

            # unmark previous word
            if i > 0:
                target_text_widget.tag_remove(
                    "highlight",
                    f"{word_pointer_start}-{len(words_split[i-1])+1}c",
                    word_pointer_start,
                )
            target_text_widget.pack()
            target_text_widget.update()

            delay = int(1000 / speed)
            target_word_window.after(delay)

        # unmark all
        target_text_widget.tag_remove("highlight", "1.0", "end")
        # reset word label
        target_word_label.update_text_display("")

    def stop_display_words(self):
        self.word_display_running.set(False)

    def toggle_text_input_window_button(self, name):
        if self.text_input_window.master.state() == "normal":
            self.text_input_window.master.withdraw()
            self.text_input_button.config(text=f"Open {name}")
        else:
            self.text_input_window.master.deiconify()
            self.text_input_button.config(text=f"Close {name}")

    def toggle_text_window_button(self, name):
        if self.text_window.master.state() == "normal":
            self.text_window.master.withdraw()
            self.text_window_button.config(text=f"Open {name}")
        else:
            self.text_window.master.deiconify()
            self.text_window_button.config(text=f"Close {name}")

    def toggle_summerization_window_button(self, name):
        if self.summerization_window.master.state() == "normal":
            self.summerization_window.master.withdraw()
            self.summerization_window_button.config(text=f"Open {name}")
        else:
            self.summerization_window.master.deiconify()
            self.summerization_window_button.config(text=f"Close {name}")

    def toggle_audio_window_button(self, name):
        if self.audio_window.master.state() == "normal":
            self.audio_window.master.withdraw()
            self.audio_window_button.config(text=f"Open {name}")
        else:
            self.audio_window.master.deiconify()
            self.audio_window_button.config(text=f"Close {name}")

    def toggle_rsvp_window_button(self, name):
        if self.rsvp_window.master.state() == "normal":
            self.rsvp_window.master.withdraw()
            self.rsvp_window_button.config(text=f"Open {name}")
        else:
            self.rsvp_window.master.deiconify()
            self.rsvp_window_button.config(text=f"Close {name}")

    def toggle_information_window_button(self, name):
        if self.information_window.master.state() == "normal":
            self.information_window.master.withdraw()
            self.information_window_button.config(text=f"Open {name}")
        else:
            self.information_window.master.deiconify()
            self.information_window_button.config(text=f"Close {name}")

    def toggle_qa_window_button(self, name):
        if self.qa_window.master.state() == "normal":
            self.qa_window.master.withdraw()
            self.qa_window_button.config(text=f"Open {name}")
        else:
            self.qa_window.master.deiconify()
            self.qa_window_button.config(text=f"Close {name}")

    def toggle_plot_window_button(self, name):
        if self.plot_window.master.state() == "normal":
            self.plot_window.master.withdraw()
            self.plot_window_button.config(text=f"Open {name}")
        else:
            self.plot_window.master.deiconify()
            self.plot_window_button.config(text=f"Close {name}")
