import os
from groq import Groq
from dotenv import load_dotenv
from openai import OpenAI
import pygame
import time
import warnings
import speech_recognition as sr

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")


# these are the modules for new rec function

import io
import soundfile as sf
import numpy as np
import whisper
# we also use speech rec but, as it's shared


warnings.filterwarnings("ignore", category=DeprecationWarning)
load_dotenv()
r = sr.Recognizer()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
messages = [
    {
        'role': 'system',
        'content': 'You are a pizza order-taking bot named Bob the pizza guy. Be as helpful as possible. Help customers with their orders when they seem confused, and keep your responses concise to avoid boring them. Any questions that are not related to pizza avoid them and remind user that their sole purpose is to help in pizza ordering only. Also make sure your responses are short and not too long as long prompts will waste the customer time '
    }
]

def getting_speech(response_text):
    client2 = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response_speech = client2.audio.speech.create(model="tts-1", voice="alloy", input=response_text)
    response_speech.stream_to_file('assistant.mp3')
    print(f'Assistant: {response_text}')
    
    pygame.mixer.init()    
    pygame.mixer.music.load('assistant.mp3')
    pygame.mixer.music.play()    
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()
def recog_whisper(
        audio_data, model = "base", show_dict = False, load_options = None, language = 'english', translate = False, **transscribe_options
):
    assert isinstance(audio_data,sr.AudioData)
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
    
def gettingInputInVoice():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration= 0.2)
        print("say something... ")
        audio = r.listen(source)
    
    # return r.recognize_whisper(audio, language='english') # this is the one with speech_recognition module
    return recog_whisper(audio, model = 'base') # this one is my own function

while True:
    try:

        # user_prompt = input("user: ")
        user_prompt = gettingInputInVoice()
        messages.append({'role': 'user', 'content': user_prompt})

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
        )
        response_text = chat_completion.choices[0].message.content
        messages.append({'role': 'assistant', 'content': response_text})

        getting_speech(response_text)

    except EOFError:
        break

