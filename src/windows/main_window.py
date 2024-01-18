from tkinter import ttk, Toplevel, DoubleVar, BOTTOM, W, S
from src.windows.tk.base_window import BaseWindow
from src.windows.tk.text_input import TextInputWindow
from src.windows.tk.text_window import TextWindow
from src.windows.tk.audio_window import AudioWindow
from src.windows.tk.rsvp_window import rsvpWindow
from src.windows.tk.information_window import InformationWindow
from src.windows.tk.qa_window import QAWindow
from src.windows.tk.plot_window import PlotWindow


class MainWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Options", "config/root.conf")
        # Set the background color of the window
        bg_color = self.master.winfo_toplevel().cget("bg")
        self.master.configure(bg=bg_color)

        # Set the background color of the frame
        self.frame = ttk.Frame(master)
        self.frame.pack(fill="both", expand=True)
        # Text Window
        self.text_window = TextWindow(Toplevel(self.master))
        self.text_window_button = ttk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_text_window_button("Text Window"),
        )
        if self.text_window.master.state() == "normal":
            self.text_window_button.config(text=f"Close Text Window")
        else:
            self.text_window_button.config(text="Open Text Window")
        self.text_window_button.pack()

        # Question Answer Window
        self.qa_window = QAWindow(Toplevel(self.master))
        self.qa_window_button = ttk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_qa_window_button("Question Answer Window"),
        )
        if self.qa_window.master.state() == "normal":
            self.qa_window_button.config(text=f"Close Question Answer Window")
        else:
            self.qa_window_button.config(text="Open Question Answer Window")
        self.qa_window_button.pack()

        # RSVP Window
        self.rsvp_window = rsvpWindow(Toplevel(self.master))
        self.rsvp_window_button = ttk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_rsvp_window_button("RSVP Window"),
        )
        if self.rsvp_window.master.state() == "normal":
            self.rsvp_window_button.config(text=f"Close RSVP Window")
        else:
            self.rsvp_window_button.config(text="Open RSVP Window")
        self.rsvp_window_button.pack()

        # Information Window
        self.information_window = InformationWindow(Toplevel(self.master))
        self.information_window_button = ttk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_information_window_button("Information Window"),
        )
        if self.information_window.master.state() == "normal":
            self.information_window_button.config(text=f"Close Information Retrival")
        else:
            self.information_window_button.config(text="Open Information Retrival")
        self.information_window_button.pack()

        # Speed control slider
        self.speed_var = DoubleVar()
        self.speed_slider = ttk.Scale(
            self.frame,
            from_=0.1,
            to=2.0,
            variable=self.speed_var,
            length=200,
            orient="horizontal",
        )
        self.speed_slider.set(1.0)
        self.speed_slider.pack()

        # Audio Window
        self.audio_window = AudioWindow(
            Toplevel(self.master),
            self.text_window.text_widget,
            self.rsvp_window.master,
            self.rsvp_window.word_label,
            self.speed_var.get(),
        )
        self.audio_window_button = ttk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_audio_window_button("Audio Window"),
        )
        if self.audio_window.master.state() == "normal":
            self.audio_window_button.config(text=f"Close Audio Window")
        else:
            self.audio_window_button.config(text="Open Audio Window")

        self.audio_window_button.pack()

        # Plot Window
        # {'you': array([1.9070455, 1.8492087]}
        self.plot_window = PlotWindow(
            Toplevel(self.master),
            {"you": [1.9070455, 1.8492087]},
            [0],
        )

        self.plot_window_button = ttk.Button(
            self.frame,
            text="",
            command=lambda: self.toggle_plot_window_button("Plot Window"),
        )

        if self.plot_window.master.state() == "normal":
            self.plot_window_button.config(text=f"Close Plot Window")
        else:
            self.plot_window_button.config(text="Open Plot Window")

        self.plot_window_button.pack()

        # Text Input Window
        self.text_input_window = TextInputWindow(
            Toplevel(self.master),
            self.text_window,
            self.audio_window,
            self.information_window,
            self.qa_window,
            self.plot_window,
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
        self.text_input_button.pack()

        # Start display words button
        self.start_button = ttk.Button(
            self.frame,
            text="Start",
            command=lambda: self.display_words(
                self.speed_var.get(),
                self.text_input_window.text_input.get("1.0", "end-1c"),
                self.text_window.text_widget,
                self.rsvp_window.word_label,
                self.rsvp_window.master,
            ),
        )
        self.start_button.pack()

        # Place Speed label, Speed slider, and Start button at the bottom
        self.speed_slider.pack(side=BOTTOM, anchor=W)
        self.start_button.pack(side=BOTTOM, anchor=S)

    def display_words(
        self, speed, words, target_text_widget, target_word_label, target_word_window
    ):
        # create text index
        word_pointer_start = "1.0"
        word_pointer_end = "1.0"

        # Iterate through words and display them
        words_split = words.split()
        for i in range(len(words_split)):
            word = words_split[i]
            target_word_label.config(text=word)
            target_word_window.update()

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
        target_word_label.config(text="")

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
