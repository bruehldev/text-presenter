from ttkthemes import ThemedTk
from src.windows.main_window import MainWindow

""" Themes:
plastik
scidmint
scidblue
scidpink
blue
alt
aquativo
scidgreen
breeze
adapta
clearlooks
scidpurple
winxpblue
radiance
scidsand
ubuntu
equilux
default
keramik
elegance
clam
smog
kroc
itft1
classic
yaru
scidgrey
black
arc

"""


def main():
    root = ThemedTk(theme="equilux")
    main = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
