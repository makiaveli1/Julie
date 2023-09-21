import openai
from dotenv import load_dotenv
import time
from termcolor import colored
import os
import logging
import os.path
import random
import json

from utils import Utils
from init import Initialize
from Memory import BotMemory


logging.basicConfig(filename='chatbot.log', level=logging.INFO)

function_schema_retrieve = {
    "name": "retrieve_user_data",
    "title": "retrieve_user_data",
    "type": "object",
    "required": ["sh", "user_id", "username"],
    "parameters": {
        "sh": {"type": "string"},
        "user_id": {"type": "string"},
        "username": {"type": "string"}
    }
}


def generate_response(prompt, conversation_history, memory, temperature=0.6, max_tokens=1000):
    model = "gpt-4-0613"
    conversation_history.append({"role": "user", "content": prompt})

    # Explicitly convert to JSON and back
    function_schema_retrieve_json = json.dumps(function_schema_retrieve)
    function_schema_retrieve_dict = json.loads(function_schema_retrieve_json)

    try:
        print("Debug: Schema Type:", type(function_schema_retrieve_dict))

        response = openai.ChatCompletion.create(
            model=model,
            messages=conversation_history,
            max_tokens=max_tokens,
            temperature=temperature,
            # Use the converted dictionary
            functions=[function_schema_retrieve_dict],
            function_call="auto"
        )
        bot_response = response['choices'][0]['message']['content'].strip()
        # Check for function call in response        
        if 'function' in response['choices'][0]:
            function_data = response['choices'][0]['function']
            if function_data['name'] == "retrieve_user_data":
                # Use the already passed sh object
                user_id = function_data['arguments']['user_id']
                username = function_data['arguments']['username']

                past_data = memory.retrieve_user_data(sh, user_id, username)

        # Use past_data to influence the bot's responses
        if past_data:
            # Custom logic here based on past_data
            pass

        # Add the bot's response to the conversation history
        conversation_history.append(
            {"role": "assistant", "content": bot_response})

        return bot_response
    except Exception as e:
        print("Error:", e)
        print("Debug: Function Schema at time of error:",
              function_schema_retrieve)


def main():
    try:
        print("Debug: Initializing...")
        init_obj = Initialize()
        print("Debug: Initialized.")
        memory_obj = BotMemory() # Initialize your sh object however you do it
        past_data = {}

        is_new_user = init_obj.is_new_user
        username = init_obj.username
        user_id = init_obj.user_id

        print(f"Debug: Is new user? {is_new_user}")

        memory_obj.register_user(
            memory_obj.sh, user_id, None, username, is_new_user)

        if is_new_user:
            new_worksheet = memory_obj.create_user_worksheet(
                memory_obj.sh, user_id, username)
        else:
            worksheet_name = f"{username}_{user_id}".replace("-", "_")
            new_worksheet = memory_obj.sh.worksheet(worksheet_name)

        history = []
        user_color = init_obj.user_color

        while True:
            user_input = input(colored("You: ", user_color)).lower()
            history.append({"role": "user", "content": user_input})

            if user_input == 'help':
                Utils.show_help()
            elif user_input in ["goodbye", "quit", "exit"]:
                Utils.exit_chat()
            elif user_input == 'history':
                past_data = memory_obj.retrieve_user_data(
                    memory_obj.sh, user_id, memory_obj, username)
                Utils.show_history(past_data)
            elif user_input == 'tutorial':
                Utils.show_tutorial()
            else:
                print("Debug: Function Schema:", function_schema_retrieve)
                chatbot_response = generate_response(
                    user_input, history, memory_obj)
                print(f"Julie: {chatbot_response}")
                history.append(
                    {"role": "assistant", "content": chatbot_response})
                memory_obj.log_interaction(
                    new_worksheet, user_input, chatbot_response)

    except KeyboardInterrupt:
        message = random.choice(Utils.interrupt_messages)
        print(f"Unexpected exit: {message}")
    except Exception as e:
        Utils.handle_exception(e)


if __name__ == '__main__':
    main()
