import pygame
import os
from tkinter import messagebox


def play_audio():
    if os.path.exists("output.wav"):
        pygame.init()
        pygame.mixer.music.load("output.wav")
        pygame.mixer.music.play()
    else:
        messagebox.showwarning(
            "File Not Found", "No TTS audio file found. Please process the text first."
        )


def stop_audio():
    pygame.mixer.music.stop()
