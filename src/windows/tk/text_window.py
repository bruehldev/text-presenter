from tkinter import ttk, Text, NORMAL, DISABLED, END
from src.windows.tk.base_window import BaseWindow


class TextWindow(BaseWindow):
    def __init__(self, master, color_dict):
        super().__init__(master, "Text Window", "config/text_window.conf")
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)
        self.keyphrases = []
        self.text = ""

        # headline
        self.headline = ttk.Label(self.frame, text="Generated Headline")
        self.headline.pack()

        self.text_widget = Text(self.frame, wrap="word")
        self.text_widget.configure(bg="black", fg="white")
        self.text_widget.pack(fill="both", expand=True)

        self.text_widget.config(state=DISABLED)

    def update_text_display(self, text):
        self.text_widget.config(state=NORMAL)
        self.text_widget.delete("1.0", END)
        self.text_widget.insert("1.0", text)
        self.text_widget.config(state=DISABLED)

    def underline_keyphrases(self):
        if self.keyphrases is not None:
            # configure the "underline" tag
            self.text_widget.tag_config("underline", underline=True)

            # underline keyphrases in text widget
            for keyphrase in self.keyphrases:
                start_idx = "1.0"
                while True:
                    start_idx = self.text_widget.search(
                        r"\y" + keyphrase + r"\y",
                        start_idx,
                        stopindex=END,
                        regexp=True,
                    )
                    if not start_idx:
                        break
                    end_idx = f"{start_idx}+{len(keyphrase)}c"
                    self.text_widget.tag_add("underline", start_idx, end_idx)
                    start_idx = end_idx
