from tkinter import ttk, Text, NORMAL, DISABLED, END
from src.windows.tk.base_window import BaseWindow
from src.services.text_summerization import summarize


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

    def update_text_display(self, text):
        self.text_widget.config(state=NORMAL)
        self.text_widget.delete("1.0", END)
        self.text_widget.insert("1.0", text)
        self.text_widget.config(state=DISABLED)
