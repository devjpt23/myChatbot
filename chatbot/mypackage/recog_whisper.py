import whisper
# from mypackage.audio import AudioData
import io
import soundfile as sf
import numpy as np
import sys
import os
# from . import Microphone, Recognizer
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mypackage.audio import AudioData
from mypackage.microphone import Microphone, Recognizer
def main():
    transcription = recog_whisper(mic_recognition(), model='base') 
    print(transcription)

def recog_whisper(
        audio_data, model = "base", show_dict = False, load_options = None, language = 'english', translate = False, **transscribe_options
):

    assert isinstance(audio_data, AudioData)

    whisper_model = whisper.load_model(model, **load_options or {})

    wav_bytes = audio_data.get_wav_data(convert_rate=16000)
    wav_stream = io.BytesIO(wav_bytes)
    audio_array, samplingRate = sf.read(wav_stream)
    audio_array = audio_array.astype(np.float32)

    result = whisper_model.transcribe(
        audio_array,
        language = language,
        task = 'translate' if translate else None,
        **transscribe_options
    )

    if show_dict:
        return result
    else:
        return result['text']
    
def mic_recognition():
    r = Recognizer()
    with Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=0.2)
        print("Say something ")
        audio = r.listen(source)
        return audio

if __name__ == '__main__':
    main()

