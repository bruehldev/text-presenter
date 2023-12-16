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


def play_audio_file(file):
    if os.path.exists(file):
        pygame.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()
    else:
        messagebox.showwarning("File Not Found", "No audio file found.")


def delete_audio_files():
    folder = "audios"
    audio_files = os.listdir(folder)
    for filename in audio_files:
        os.remove(os.path.join(folder, filename))
