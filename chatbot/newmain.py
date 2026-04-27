import os
from groq import Groq
from dotenv import load_dotenv
from openai import OpenAI
import pygame
import time
import json
import warnings
import speech_recognition as sr
import io
import soundfile as sf
import numpy as np
import whisper

MODEL = "llama3-groq-8b-8192-tool-use-preview"

cart_items = []

price_list = {
    "Classic Cheese Pizza": 10,
    "Hawaian Pizza": 11,
    "Tropical Pizza": 15,
    "Neopolitan Pizza": 14,
}


def get_repsonse(question):
    return json.dumps({"question": question})


def get_pizza_menu():
    menu = [
        [
            "Classic Cheese Pizza",
        ],
        [
            "Hawaian Pizza",
        ],
        [
            "Tropical Pizza",
        ],
        [
            "Neopolitan Pizza",
        ],
    ]
    return json.dumps(menu)


def get_pizza_description(itemName):
    description = {
        "Classic Cheese Pizza": "just full of the cheese you like, who doesnt like cheese",
        "Hawaian Pizza": "it flys from the beaches of hawai on spot you order it (t/c apply)",
        "Tropical Pizza": "A vacation on a slice! Imagine a cheesy paradise topped with juicy pineapple, zesty mango chunks, and a hint of spicy jalapeño for that island kick. It's like a beach party in your mouth—no sunscreen required!",
        "Neopolitan Pizza": "just neopolitan,  like usual",
    }
    if description.get(itemName):
        return json.dumps(description.get(itemName))


def get_pizza_price(itemName):
    if price_list.get(itemName):
        return json.dumps(price_list.get(itemName))


def get_all_price_list():
    return json.dumps(price_list)


def get_cart_items(itemCount, itemName):  # this function adds a pizza in cart

    cart_items.append([itemCount, itemName])
    return json.dumps(cart_items)


def get_cart():  # this returns the item namees in the cart
    items_inCart = cart_items
    return json.dumps(items_inCart)


# [[3,classic cheese pizza],[10,'hawaian pizza']]
def remove_item(itemName, quantity):
    for item in cart_items:
        if item[1] == itemName:
            if quantity < int(item[0]):
                (item[0]) -= quantity
            elif quantity == int(item[0]):
                cart_items.remove(itemName)
            else:
                return f"You only have {item[1]} of {item[1]}"
    return json.dumps(get_cart())


def get_bill():
    total_price = 0
    per_item_bill = []
    for count, item_name in cart_items:
        item_price = price_list.get(item_name)
        total_price += item_price * count
        per_item_bill.append(
            f"{item_name} : {count} x {item_price} dollars = {count * item_price} dollars"
        )

    return json.dumps({"Total Bill": total_price, "Itemized Bill": per_item_bill})


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_response",
            "description": "Your name is Bob the pizza guy. Responding a casual chat, if you are confused or dont know the answer to something just say and even if you are not sure which function to use just say 'Sorry i am not sure how can i help you with that. Could you make the statement more clear'. If the user leaves a blank, just ask the user to say something",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Responding a casual chat",
                    }
                },
                "required": ["question"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pizza_menu",
            "description": "Gets the items from the menu and thier descirptions and display them when the function is called and also dont provide description for the pizzas at the start unless asked for",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pizza_price",
            "description": "Get the price of pizza that user is looking. e.g what is the price of xyz pizza.Allow spelling mistakes, match the pizza typed with the closest pizza in the menu so this can avoid errors in the code",
            "parameters": {
                "type": "object",
                "properties": {
                    "itemName": {
                        "type": "string",
                        "description": "The price of pizza that we need",
                    }
                },
                "required": ["itemName"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_cart_items",
            "description": "Adds item to the cart for example 'can you please add one xyz pizza' or 'can you add another xyz pizza' so this will increment the value of current item by one. Allow spelling mistakes, match the pizza typed with the closest pizza in the menu so this can avoid errors in the code",
            "parameters": {
                "type": "object",
                "properties": {
                    "itemName": {
                        "type": "string",
                        "description": "item name to add in the cart",
                    },
                    "itemCount": {
                        "type": "number",
                        "description": "this is the number of item that need to be added",
                    },
                },
                "required": ["itemName"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_cart",
            "description": "Gets items orderd and placed in the cart and displays them when the function is called",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remove_item",
            "description": "Remove the item from the cart and display the again",
            "parameters": {
                "type": "object",
                "properties": {
                    "itemName": {
                        "type": "string",
                        "description": "This is the item name that needs to be removed from the cart. e.g 'kindly remove one classic cheese pizza' so in this case classic cheese pizza need to be removed from the cart",
                    },
                    "quantity": {
                        "type": "number",
                        "description": "remove the particular amount of pizza from the cart e.g remove 5 xyz pizza so that means we need to remove 5 pizzas named xyz from the cart",
                    },
                },
                "required": ["itemName"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pizza_description",
            "description": "Get the description of the pizza when asked for. Allow spelling mistakes, match the pizza typed with the closest pizza in the menu so this can avoid errors in the code",
            "parameters": {
                "type": "object",
                "properties": {
                    "itemName": {
                        "type": "string",
                        "description": "We need to provide description for this pizza only when asked",
                    }
                },
                "required": ["itemName"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_bill",
            "description": "Gets the bills of the items present in the cart e.g can you give me the bill",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_all_price_list",
            "description": "Get the price list of all pizzas in the menu",
            "parameters": {},
        },
    },
]
warnings.filterwarnings(
    "ignore", message="FP16 is not supported on CPU; using FP32 instead"
)


warnings.filterwarnings("ignore", category=DeprecationWarning)
load_dotenv()
r = sr.Recognizer()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
messages = [
    {
        "role": "system",
        "content": "You are a pizza order-taking bot named Bob the pizza guy. Be as helpful as possible. Help customers with their orders when they seem confused, and keep your responses concise to avoid boring them. Any questions that are not related to pizza avoid them and remind user that their sole purpose is to help in pizza ordering only. Also make sure your responses are short and not too long as long prompts will waste the customer time ",
    }
]


def getting_speech(response_text):
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response_speech = openai_client.audio.speech.create(
        model="tts-1", voice="alloy", input=response_text
    )
    response_speech.stream_to_file("assistant.mp3")
    print(f"Assistant: {response_text}")

    pygame.mixer.init()
    pygame.mixer.music.load("assistant.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()
    os.remove("assistant.mp3")


# TODO: Delete assitant.mp3 after use


def recognize_voice(
    audio_data,
    model="base",
    show_dict=False,
    load_options=None,
    language="english",
    translate=False,
    **transscribe_options,
):
    assert isinstance(audio_data, sr.AudioData)
    whisper_model = whisper.load_model(model, **load_options or {})

    wav_bytes = audio_data.get_wav_data(convert_rate=16000)
    wav_stream = io.BytesIO(wav_bytes)
    audio_array, samplingRate = sf.read(wav_stream)
    # TODO: Remove library, get audio array in correct format for whisper using pyaudio
    audio_array = audio_array.astype(np.float32)

    result = whisper_model.transcribe(
        audio_array,
        language=language,
        task="translate" if translate else None,
        **transscribe_options,
    )

    if show_dict:
        return result
    else:
        return result["text"]


def gettingInputInVoice():
    with sr.Microphone() as source:
        # TODO: Make this work using pyaudio
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("say something... ")
        audio = r.listen(source)

    # return r.recognize_whisper(audio, language='english') # this is the one with speech_recognition module
    return recognize_voice(audio, model="base")  # this one is my own function


# while True:
#     try:

#         # user_prompt = input("user: ")
#         user_prompt = gettingInputInVoice()
#         messages.append({"role": "user", "content": user_prompt})

#         chat_completion = client.chat.completions.create(
#             messages=messages,
#             model="llama3-8b-8192",
#         )
#         response_text = chat_completion.choices[0].message.content
#         messages.append({"role": "assistant", "content": response_text})

#         getting_speech(response_text)

#     except EOFError:
#         break


def run_coversation(user_prompt):
    messages.append({"role": "user", "content": user_prompt})
    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=tools, tool_choice="auto", max_tokens=4096
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "get_reponse": get_repsonse,
            "get_pizza_menu": get_pizza_menu,
            "get_pizza_description": get_pizza_description,
            "get_pizza_price": get_pizza_price,
            "get_cart_items": get_cart_items,
            "get_cart": get_cart,
            "remove_item": remove_item,
            "get_bill": get_bill,
            "get_all_price_list": get_all_price_list,
        }
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        second_response = client.chat.completions.create(model=MODEL, messages=messages)
        final_response = second_response.choices[0].message.content
    else:
        response = client.chat.completions.create(
            model=MODEL, messages=messages, max_tokens=4096
        )
        messages.append(response_message)
        final_response = response.choices[0].message.content

    return final_response


def main():
    while True:
        try:
            user_prompt = gettingInputInVoice()
            # print(f"Pizza bot: {run_coversation(user_prompt)}")
            getting_speech(run_coversation(user_prompt))
        except EOFError:
            break


if __name__ == "__main__":
    main()
