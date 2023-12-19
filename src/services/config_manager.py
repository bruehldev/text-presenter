import os
import json


def create_config_folder():
    config_folder = "config"
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)


def load_config(window, filename):
    create_config_folder()
    try:
        with open(filename, "r") as conf:
            if not conf:
                return
            config_data = json.load(conf)
            window.geometry(config_data.get("size", ""))
            window.state(config_data.get("toggle_state", ""))
    except FileNotFoundError:
        pass


def save_config(window, filename):
    create_config_folder()
    config_data = {"size": window.geometry(), "toggle_state": window.state()}
    with open(filename, "w") as conf:
        json.dump(config_data, conf)
