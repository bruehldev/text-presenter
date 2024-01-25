from tkinter import END, NORMAL, StringVar, Text, ttk
from src.services.qa_manager import generate_answer
from src.windows.tk.base_window import BaseWindow


class QAWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Question Answer Window", "config/qa_window.conf")
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)

        # Dropdown (Combobox)
        self.dropdown_var = StringVar(value="bert-large-uncased-whole-word-masking-finetuned-squad")
        self.dropdown = ttk.Combobox(
            self.frame,
            textvariable=self.dropdown_var,
            values=[
                "bert-large-uncased-whole-word-masking-finetuned-squad",
                "deepset/roberta-base-squad2",
                "distilbert-base-cased-distilled-squad",
            ],
        )
        self.dropdown.pack()

        # Bind a function to the dropdown selection change event
        self.dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_change)

        self.text_widget = Text(self.frame, wrap="word")
        self.text_widget.configure(bg="black", fg="white")
        self.text_widget.pack()

        self.text = ""
        self.answer = ""
        self.question = ""
        self.model =  self.dropdown_var.get()

        self.question_input = Text(self.frame, state=NORMAL)
        self.question_input.pack()

        self.send_button = ttk.Button(
            self.frame,
            text="Apply",
            command=self.process_question,
        )
        self.send_button.pack()

    def process_question(self):
        self.question = self.question_input.get("1.0", END).strip()
        self.answer = generate_answer(self.question, self.text, self.model)
        self.display_answer()

    def display_answer(self):
        self.text_widget.delete("1.0", END)
        self.text_widget.insert(END, self.answer)

    def reset(self):
        self.text_widget.delete("1.0", END)
        self.question_input.delete("1.0", END)
        self.text = ""
        self.answer = ""
        self.question = ""

    def on_dropdown_change(self, event):
        self.model = self.dropdown_var.get()
