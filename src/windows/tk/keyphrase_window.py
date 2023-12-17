from transformers import (
    TokenClassificationPipeline,
    AutoModelForTokenClassification,
    AutoTokenizer,
)
from transformers.pipelines import AggregationStrategy
import numpy as np
import tkinter as tk
from src.windows.tk.base_window import BaseWindow


class KeyphraseWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Keyphrase Window", "config/keyphrase_window.conf")

        # listbox
        self.listbox = tk.Listbox(self.master)
        self.listbox.pack(fill="both", expand=True)
