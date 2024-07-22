import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")

)
messages = []

while True:
    try:
        user_prompt = input("user: ")
        messages.append(
            {'role':'user','content':user_prompt}
        )

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
        )
        responseText = chat_completion.choices[0].message.content
        print(f"Assitant:{responseText}")
    except EOFError:
        break
