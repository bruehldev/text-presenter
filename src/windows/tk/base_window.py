import tkinter as tk
from src.services.config_manager import load_window_config, save_window_config


class BaseWindow:
    def __init__(self, master, title, config_filename):
        self.master = master
        self.frame = tk.Frame(self.master)

        self.title = title
        self.config_filename = config_filename

        self.master.title(self.title)
        self.load_config()
        self.bind_configure_and_save_size()
        self.bind_save_toggle_state()

    def configure_and_save_size(self, event):
        if self.master:
            self.master.update()
            self.save_config()

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
                lambda event: self.save_config(),
            )
            self.master.bind(
                "<Map>",
                lambda event: self.save_config(),
            )
            self.master.bind(
                "<Destroy>",
                lambda event: self.save_config(),
            )

    def load_config(self):
        load_window_config(self.master, self.config_filename)

    def save_config(self):
        save_window_config(self.master, self.config_filename)
