import pygame
import os
from tkinter import messagebox

# Initialize Pygame
pygame.init()

# Initialize mixer
pygame.mixer.init()


# Create a mixer channel
channel = pygame.mixer.Channel(0)


def play_audio_file_channel(file):
    if os.path.exists(file):
        channel.play(pygame.mixer.Sound(file))
        while channel.get_busy():
            pygame.time.Clock().tick(1)
    else:
        messagebox.showwarning("File Not Found", "No audio file found.")


def stop_audio_channel():
    channel.stop()


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
    else:
        messagebox.showwarning("File Not Found", "No audio file found.")


def delete_audio_files():
    folder = "audios/sentences"
    audio_files = os.listdir(folder)
    for filename in audio_files:
        file = os.path.join(folder, filename)
        if os.path.exists(file):
            os.remove(file)
    if os.path.exists("audios/title.wav"):
        os.remove("audios/title.wav")
