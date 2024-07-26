import os
from groq import Groq
from dotenv import load_dotenv
from openai import OpenAI
import pygame
import time
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
load_dotenv()

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

while True:
    try:
        user_prompt = input("user: ")
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
    