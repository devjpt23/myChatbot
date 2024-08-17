import os
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()


client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama3-groq-70b-8192-tool-use-preview"
# MODEL = "llama3-70b-8192"


messages = [
    {
        "role": "system",
        "content": "You are a function calling LLM that uses the data extracted from the functions to answer questions around pizza menu. Do not let the user know that you are a LLM, instead always tell them that you are a helpful pizza bot",
    }
]

# IF THIS MODEL DOESNT WORK WELL WE NEED TO CHANGE IT TO MIXTRAL MODEL

# WE NEED TO INITILIZE THE API CLIENT ---> CHECKED
# WE NEED TO DEFINE A FUNCTION AND CONVERSATION PARAMETERS -- checked
# WE TO PROCESS THE MODEL'S REQUEST -- checked
# WE NEED TO INCORPORATE FUNCTION RESPONSE INTO CONVERSATION -- checked

# 〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️

# ✅✅✅ function number 1--checked ✅✅✅
# WE NEED TO HAVE ONE FOR PIZZA MENU -- checked
# ---> INDICATE THE MENU FOR PIZZA WE SELL --CHECKED THIS
# 〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️

# ✅✅✅ function number 2--checked ✅✅✅
# WE NEED TO DISPLAY THE PRICE OF THE PIZZAS OR FOOD ITEMS--checked
# ---> INDICATE THE PRICES OF THE PARTICULAR PIZZAS when called--checked

# 〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️

# ✅✅✅function number 3--checked✅✅✅
# WE NEED TO CHECK THE CART
# ---> INDICATE THE ITEMS CURRENTLY ORDERED, BUT NOT FINALISED
# 〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️

# ✅✅✅function number 4--checked✅✅✅
# WE NEED TO REMOVE ITEM FROM THE CART
# ---> SUBTRACT THE ITEM FROM THE CART
# 〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️

# ✅✅✅function number 5--checked✅✅✅
# WE NEED TO ADD ITEM TO THE CART
# ---> ADD THE CHOOSEN ITEM INTO THE CART
# 〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️


# ✅✅✅function number 6--checked✅✅✅
# ---> INDICATE THE DESCRIPTION OF THE PIZZAS OR FOOD ITEM

# function number 8

# WE NEED TO FINALISE THE ORDER
# ---> WE NEED TO MAKE THE ORDER IN THE CART AND GET THE TOTAL OF THE ITEMS
# ORDERED AND PRESENT IT TO THE CUSTOMER
#  return item names and total price
# 〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️
cart_items = []

price_list = {
    "classic cheese pizza": 10,
    "Hawaian Pizza": 100,
    "Tropical Pizza": 150,
    "Neopolitan Pizza": 31,
}


def get_repsonse(question):
    return json.dumps({"question": question})


def get_pizza_menu():
    menu = [
        [
            "classic Cheese Pizza",
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
        "classic cheese pizza": "just full of the cheese you like, who doesnt like cheese",
        "Hawaian Pizza": "it flys from the beaches of hawai on spot you order it (t/c apply)",
        "Tropical Pizza": "A vacation on a slice! Imagine a cheesy paradise topped with juicy pineapple, zesty mango chunks, and a hint of spicy jalapeño for that island kick. It's like a beach party in your mouth—no sunscreen required!",
        "Neopolitan Pizza": "just neopolitan,  like usual",
    }
    if description.get(itemName):
        return json.dumps(description.get(itemName))


def get_pizza_price(itemName):
    if price_list.get(itemName):
        return json.dumps(price_list.get(itemName))


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
            "description": "Your name is Bob the pizza guy. Responding a casual chat, if you are confused or dont know the answer to something just say and even if you are not sure which function to use just say 'Sorry i am not sure how can i help you with that. Could you make the statement more clear'",
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
            "description": "Get the price of pizza that user is looking. e.g what is the price of xyz pizza",
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
            "description": "Adds item to the cart for example 'can you please add one xyz pizza' or 'can you add another xyz pizza' so this will increment the value of current item by one",
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
            "description": "Get the description of the pizza when asked for",
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
]


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
            user_prompt = input("User: ")
            print(f"Pizza bot: {run_coversation(user_prompt)}")
        except EOFError:
            break


if __name__ == "__main__":
    main()
