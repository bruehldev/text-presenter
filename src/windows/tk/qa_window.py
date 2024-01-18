from src.services.qa_manager import generate_answer
from src.windows.tk.base_window import BaseWindow
from tkinter import ttk, END, NORMAL, Text


class QAWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Question Answer Window", "config/qa_window.conf")
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)

        self.text_widget = Text(self.frame, wrap="word")
        self.text_widget.configure(bg="black", fg="white")
        self.text_widget.pack()

        self.text = ""
        self.answer = ""
        self.question = ""

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
        self.answer = generate_answer(self.question, self.text)
        self.display_answer()

    def display_answer(self):
        self.text_widget.delete("1.0", END)
        self.text_widget.insert(END, self.answer)
