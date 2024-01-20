from tkinter import ttk, END, StringVar, Listbox
from src.windows.tk.base_window import BaseWindow


class InformationWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Information Retrival", "config/information.conf")
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)

        # Dropdown (Combobox)
        self.dropdown_var = StringVar(value="Keyphrases")
        self.dropdown = ttk.Combobox(
            self.frame,
            textvariable=self.dropdown_var,
            values=[
                "Keyphrases",
                "Listbox2",
                "Frequent Words",
                "Bulletpoints",
                "Topics",
            ],
        )
        self.dropdown.pack()

        # Bind a function to the dropdown selection change event
        self.dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_change)

        # Keyphrases
        self.keyphrases = None
        self.keyphrases_listbox = Listbox(self.frame)
        self.keyphrases_listbox.configure(bg="black", fg="white")
        self.keyphrases_listbox.pack(fill="both", expand=True)

        # Frequent words
        self.frequent_words = None
        self.frequent_words_listbox = Listbox(self.frame)
        self.frequent_words_listbox.configure(bg="black", fg="white")
        self.keyphrases_listbox.pack(fill="both", expand=True)

        # Possible bulletpoints
        self.bulletpoints = None
        self.bulletpoints_listbox = Listbox(self.frame)
        self.bulletpoints_listbox.configure(bg="black", fg="white")
        self.bulletpoints_listbox.pack(fill="both", expand=True)

        # Topics
        self.topics = None
        self.topics_listbox = Listbox(self.frame)
        self.topics_listbox.configure(bg="black", fg="white")
        self.topics_listbox.pack(fill="both", expand=True)

        # TODO REMOVE THIS
        # Additional listbox for Listbox2
        self.listbox2 = Listbox(self.frame)
        self.listbox2.configure(bg="black", fg="white")

        # Initial setting
        self.on_dropdown_change(None)

    def on_dropdown_change(self, event):
        selected_value = self.dropdown_var.get()

        # Hide both listboxes initially
        self.keyphrases_listbox.pack_forget()
        self.frequent_words_listbox.pack_forget()
        self.listbox2.pack_forget()
        self.bulletpoints_listbox.pack_forget()
        self.topics_listbox.pack_forget()

        if selected_value == "Keyphrases":
            self.keyphrases_listbox.delete(0, END)
            self.frequent_words_listbox.delete(0, END)
            if self.keyphrases is None:
                return
            for keyphrase in self.keyphrases:
                self.keyphrases_listbox.insert(END, keyphrase)

            self.keyphrases_listbox.pack(fill="both", expand=True)
        elif selected_value == "Frequent Words":
            self.keyphrases_listbox.delete(0, END)
            self.frequent_words_listbox.delete(0, END)
            if self.frequent_words is None:
                return
            for word, frequency in self.frequent_words:
                # if frequency is 1, keyphrase is not important
                if frequency == 1:
                    continue
                self.frequent_words_listbox.insert(END, f"{word}: {frequency} times")
            self.frequent_words_listbox.pack(fill="both", expand=True)
        elif selected_value == "Listbox2":
            # Show the second listbox with items 1, 2, 3
            self.listbox2.pack(fill="both", expand=True)
            self.listbox2.delete(0, END)
            for item in ["1", "2", "3"]:
                self.listbox2.insert(END, item)
        elif selected_value == "Bulletpoints":
            self.bulletpoints_listbox.delete(0, END)
            if self.bulletpoints is None:
                return
            for bulletpoint in self.bulletpoints:
                self.bulletpoints_listbox.insert(END, bulletpoint)
            self.bulletpoints_listbox.pack(fill="both", expand=True)
        elif selected_value == "Topics":
            self.topics_listbox.delete(0, END)
            if self.topics is None:
                return
            for topic in self.topics:
                self.topics_listbox.insert(END, topic)
            self.topics_listbox.pack(fill="both", expand=True)

    def reset(self):
        self.keyphrases_listbox.delete(0, END)
        self.frequent_words_listbox.delete(0, END)
        self.bulletpoints_listbox.delete(0, END)
        self.listbox2.delete(0, END)
        self.topics_listbox.delete(0, END)
        self.dropdown_var.set("Keyphrases")
