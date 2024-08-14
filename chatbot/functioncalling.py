from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama3-8b-8192"

# first lets get us a def function
# then lets get us a function description (tools)

def show_menu():
    """Get menu items from the menu"""
    menu = [
        "Cheese Pizza",
        "Neopolitan pizza",
        "Veggie loaded pizza",
        "Dev special pizza",
        "chase speical pizza"
    ]
    return json.dumps(menu)

def run_conversation(user_prompt):
    messages=[
        {
            "role":"system",
            "content":"You are a helpful pizza bot, you knowledge is not beyond the world of pizza. Please be kind."
        },
        {
            "role":"user",
            "content":user_prompt
        }
    ]
    tools = [
        {
                "type": "function",
                "function": {
                    "name": "show_menu",
                    "description": "Gets the items from the menu and display them when function is called",
                    "parameters": {},
                },
            }
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {
            "show_menu":show_menu
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
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return second_response.choices[0].message.content


while True:
    try:
        user_prompt = input('User: ')
        response = run_conversation(user_prompt)
        print(f"Assistant: {response}")
    except EOFError:
        break


