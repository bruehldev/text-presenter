from TTS.api import TTS
import torch


def generate_tts(text):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    tts.tts_to_file(
        text=text, speaker_wav="example_1.wav", language="en", file_path="output.wav"
    )
