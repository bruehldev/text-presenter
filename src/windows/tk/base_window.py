import tkinter as tk
from services.config_manager import (
    load_size,
    save_size,
    load_toggle_state,
    save_toggle_state,
)


class BaseWindow:
    def __init__(self, master, title, config_filename):
        self.master = master
        self.frame = tk.Frame(self.master)

        self.title = title
        self.config_filename = config_filename

        self.master.title(self.title)
        self.load_size()
        self.load_toggle_state()
        self.bind_configure_and_save_size()
        self.bind_save_toggle_state()

    def configure_and_save_size(self, event):
        if self.master:
            self.master.update()
            self.save_size()

    def bind_configure_and_save_size(self):
        if self.master:
            self.master.bind(
                "<Configure>",
                lambda event: self.configure_and_save_size(event),
            )

    def bind_save_toggle_state(self):
        if self.master:
            self.master.bind(
                "<Unmap>",
                lambda event: self.save_toggle_state(),
            )
            self.master.bind(
                "<Map>",
                lambda event: self.save_toggle_state(),
            )
            self.master.bind(
                "<Destroy>",
                lambda event: self.save_toggle_state(),
            )

    def load_size(self):
        if self.master:
            load_size(self.master, self.config_filename)

    def save_size(self):
        if self.master:
            save_size(self.master, self.config_filename)

    def toggle(self):
        if self.master.state() == "normal":
            self.master.withdraw()
        else:
            self.master.deiconify()

    def load_toggle_state(self):
        if self.master:
            load_toggle_state(self.master, self.config_filename + "_toggle")

    def save_toggle_state(self):
        if self.master:
            save_toggle_state(self.master, self.config_filename + "_toggle")
