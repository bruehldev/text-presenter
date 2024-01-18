from ttkthemes import ThemedTk
from src.windows.main_window import MainWindow

""" Themes:
arc
black
blue
clearlooks
equilux
keramik
plastik
radiance
scidblue
scidgreen
scidgrey
scidmint
scidpink
scidsand
smog
winxpblue
yaru
"""


def main():
    root = ThemedTk(theme="black")
    main = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
