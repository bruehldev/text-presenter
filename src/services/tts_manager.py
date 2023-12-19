from TTS.api import TTS
import os


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def generate_tts(sentences, model_name):
    create_folder("audios/sentences")
    for i in range(len(sentences)):
        tts = TTS(
            model_name=model_name,
            gpu=True,
        )
        tts.tts_to_file(text=sentences[i], file_path=f"audios/sentences/audio_{i}.wav")


# "tts_models/en/ljspeech/vits"
def generate_tts_title(title, model_name):
    if title is None:
        return
    create_folder("audios")
    tts = TTS(
        model_name=model_name,
        gpu=True,
    )
    tts.tts_to_file(text=title, file_path=f"audios/title.wav")


# List of model names
def get_model_names():
    en_model_names = [
        "tts_models/multilingual/multi-dataset/xtts_v2",
        "tts_models/multilingual/multi-dataset/xtts_v1.1",
        "tts_models/multilingual/multi-dataset/your_tts",
        "tts_models/multilingual/multi-dataset/bark",
        "tts_models/en/ek1/tacotron2",
        "tts_models/en/ljspeech/tacotron2-DDC",
        "tts_models/en/ljspeech/tacotron2-DDC_ph",
        "tts_models/en/ljspeech/glow-tts",
        "tts_models/en/ljspeech/speedy-speech",
        "tts_models/en/ljspeech/tacotron2-DCA",
        "tts_models/en/ljspeech/vits",
        "tts_models/en/ljspeech/vits--neon",
        "tts_models/en/ljspeech/fast_pitch",
        "tts_models/en/ljspeech/overflow",
        "tts_models/en/ljspeech/neural_hmm",
        "tts_models/en/vctk/vits",
        "tts_models/en/vctk/fast_pitch",
        "tts_models/en/sam/tacotron-DDC",
        "tts_models/en/blizzard2013/capacitron-t2-c50",
        "tts_models/en/blizzard2013/capacitron-t2-c150_v2",
        "tts_models/en/multi-dataset/tortoise-v2",
        "tts_models/en/jenny/jenny",
    ]
    return en_model_names
