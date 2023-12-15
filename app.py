import tkinter as tk
from src.windows.main_window import MainWindow


def main():
    root = tk.Tk()
    main = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
