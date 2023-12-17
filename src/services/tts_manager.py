from TTS.api import TTS
from pydub.playback import play


""" vocoder_models
 1: vocoder_models/universal/libri-tts/wavegrad
 2: vocoder_models/universal/libri-tts/fullband-melgan
 3: vocoder_models/en/ek1/wavegrad
 4: vocoder_models/en/ljspeech/multiband-melgan
 5: vocoder_models/en/ljspeech/hifigan_v2
 6: vocoder_models/en/ljspeech/univnet
 7: vocoder_models/en/blizzard2013/hifigan_v2
 8: vocoder_models/en/vctk/hifigan_v2
 9: vocoder_models/en/sam/hifigan_v2
 10: vocoder_models/nl/mai/parallel-wavegan
 11: vocoder_models/de/thorsten/wavegrad
 12: vocoder_models/de/thorsten/fullband-melgan
 13: vocoder_models/de/thorsten/hifigan_v1
 14: vocoder_models/ja/kokoro/hifigan_v1
 15: vocoder_models/uk/mai/multiband-melgan
 16: vocoder_models/tr/common-voice/hifigan
 17: vocoder_models/be/common-voice/hifigan
"""

# TODO make vocoder selectable


def generate_tts(sentences):
    for i in range(len(sentences)):
        tts = TTS(
            model_name="tts_models/en/ljspeech/vits",
            gpu=True,
        )
        tts.tts_to_file(text=sentences[i], file_path=f"audios/audio_{i}.wav")


def generate_tts_title(title):
    tts = TTS(
        model_name="tts_models/en/ljspeech/vits",
        gpu=True,
    )
    tts.tts_to_file(text=title, file_path=f"audios/title.wav")
