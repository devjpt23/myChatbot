# this is the first stage in eliminating the need for 'speech_recognition' library
import speech_recognition as sr
import io
import numpy as np
import soundfile as sf
import whisper

import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

def recog_whisper(
        audio_data, model = "base", show_dict = False, load_options = None, language = 'english', translate = False, **transscribe_options
):

    # assert isinstance(audio_data, sr.AudioData)

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

r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration = 0.2)
    print("Say something ")
    audio = r.listen(source)

transcription = recog_whisper(audio, model='base') 
print(transcription)

