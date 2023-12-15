import os


def create_config_folder():
    config_folder = "config"
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)


def load_size(window, filename):
    create_config_folder()
    try:
        with open(filename, "r") as conf:
            window.geometry(conf.read())
    except FileNotFoundError:
        pass


def save_size(window, filename):
    create_config_folder()
    with open(filename, "w") as conf:
        conf.write(window.geometry())


def load_toggle_state(window, filename):
    create_config_folder()
    try:
        with open(filename, "r") as conf:
            window.state(conf.read())
    except FileNotFoundError:
        pass


def save_toggle_state(window, filename):
    create_config_folder()
    with open(filename, "w") as conf:
        conf.write(window.state())
