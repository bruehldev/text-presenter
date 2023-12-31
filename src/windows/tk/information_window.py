import tkinter as tk
from tkinter import ttk
from src.windows.tk.base_window import BaseWindow


class InformationWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Information Retrival", "config/information.conf")

        # Dropdown (Combobox)
        self.dropdown_var = tk.StringVar(value="Keyphrases")
        self.dropdown = ttk.Combobox(
            self.master,
            textvariable=self.dropdown_var,
            values=["Keyphrases", "Listbox2", "Frequent Words"],
        )
        self.dropdown.pack()

        # Bind a function to the dropdown selection change event
        self.dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_change)

        # Keyphrases
        self.keyphrases = None
        self.keyphrases_listbox = tk.Listbox(self.master)
        self.keyphrases_listbox.pack(fill="both", expand=True)

        # Frequent words
        self.frequent_words = None
        self.frequent_words_listbox = tk.Listbox(self.master)
        self.keyphrases_listbox.pack(fill="both", expand=True)

        # Additional listbox for Listbox2
        self.listbox2 = tk.Listbox(self.master)

        # Initial setting
        self.on_dropdown_change(None)

    def on_dropdown_change(self, event):
        selected_value = self.dropdown_var.get()

        # Hide both listboxes initially
        self.keyphrases_listbox.pack_forget()
        self.frequent_words_listbox.pack_forget()
        self.listbox2.pack_forget()

        if selected_value == "Keyphrases":
            self.keyphrases_listbox.delete(0, tk.END)
            self.frequent_words_listbox.delete(0, tk.END)
            if self.keyphrases is None:
                return
            for keyphrase in self.keyphrases:
                self.keyphrases_listbox.insert(tk.END, keyphrase)

            self.keyphrases_listbox.pack(fill="both", expand=True)
        elif selected_value == "Frequent Words":
            self.keyphrases_listbox.delete(0, tk.END)
            self.frequent_words_listbox.delete(0, tk.END)
            if self.frequent_words is None:
                return
            for word, frequency in self.frequent_words:
                # if frequency is 1, keyphrase is not important
                if frequency == 1:
                    continue
                self.frequent_words_listbox.insert(tk.END, f"{word}: {frequency} times")
            self.frequent_words_listbox.pack(fill="both", expand=True)
        elif selected_value == "Listbox2":
            # Show the second listbox with items 1, 2, 3
            self.listbox2.pack(fill="both", expand=True)
            self.listbox2.delete(0, tk.END)
            for item in ["1", "2", "3"]:
                self.listbox2.insert(tk.END, item)
