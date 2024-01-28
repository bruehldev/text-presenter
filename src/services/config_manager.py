import json
import os


def create_config_folder():
    config_folder = "config"
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)


def load_window_config(window, filename):
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


def save_window_config(window, filename):
    create_config_folder()
    config_data = {}
    try:
        with open(filename, "r") as conf:
            config_data = json.load(conf)
    except FileNotFoundError:
        pass

    config_data["size"] = window.geometry()
    config_data["toggle_state"] = window.state()

    with open(filename, "w") as conf:
        json.dump(config_data, conf)


def get_config(config_name):
    create_config_folder()
    if not os.path.exists("config/" + config_name + ".conf"):
        return None
    with open("config/" + config_name + ".conf", "r") as conf:
        config_data = json.load(conf)
        return config_data


def save_config(config_name, config_data):
    with open("config/" + config_name + ".conf", "w") as conf:
        json.dump(config_data, conf)


def get_config_parameter(config_name, key):
    config = get_config(config_name)
    # check if config is None or key does not exist
    if config is None or key not in config:
        return None
    return config[key]


def set_config_parameter(config_name, key, value):
    config = get_config(config_name)
    config[key] = value
    save_config(config_name, config)
