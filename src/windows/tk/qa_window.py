import tkinter as tk
from src.services.qa_manager import generate_answer
from src.windows.tk.base_window import BaseWindow

class QAWindow(BaseWindow):
    def __init__(self, master):
        super().__init__(master, "Question Answer Window", "config/qa_window.conf")

        self.text_widget = tk.Text(self.master, wrap="word")
        self.text_widget.pack()

        self.text = ""
        self.answer = ""
        self.question = ""

        self.text_input = tk.Text(self.master, state=tk.NORMAL)
        self.text_input.pack()

        self.send_button = tk.Button(
            self.master,
            text="Apply",
            command=self.process_question,
        )
        self.send_button.pack()

    def process_question(self):
        self.question = self.text_input.get("1.0", tk.END).strip()
        self.answer = generate_answer(self.question, self.text)
        self.display_answer()

    def display_answer(self):
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, self.answer)