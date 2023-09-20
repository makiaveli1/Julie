import openai
from dotenv import load_dotenv
import time
from termcolor import colored
import os
import logging
import os.path
import random

from utils import Utils
from init import Initialize
from Memory import BotMemory


logging.basicConfig(filename='chatbot.log', level=logging.INFO)

function_schema_retrieve = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "title": "retrieve_user_data",
    "type": "object",
    "required": ["sh", "user_id", "username"],
    "properties": {
        "sh": {"type": "string"},
        "user_id": {"type": "string"},
        "username": {"type": "string"}
    }
}


def generate_response(prompt, conversation_history, memory, temperature=0.6, max_tokens=1000):
    model = "gpt-4"  # Assuming you're using GPT-4

    # Add the new user prompt to the conversation history
    conversation_history.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=conversation_history,
            max_tokens=max_tokens,
            temperature=temperature,
            # Add this line to include function call
            functions=[function_schema_retrieve],
            function_call="auto"
        )

        bot_response = response['choices'][0]['message']['content'].strip()

        # Check for function call in response
        if 'function' in response['choices'][0]:
            function_data = response['choices'][0]['function']
            if function_data['name'] == "retrieve_user_data":
                sh = memory.sh  # Use the Memory instance to get the Google Sheets object
                user_id = function_data['arguments']['user_id']
                username = function_data['arguments']['username']

                # You can then call your retrieve_user_data function here
                past_data = memory.retrieve_user_data(
                    user_id, username)  # Use the Memory instance method

        # Add the bot's response to the conversation history
        conversation_history.append(
            {"role": "assistant", "content": bot_response})

        return bot_response
    except Exception as e:
        print("Error:", e)
        



def main():
    try:
        print("Debug: Initializing...")
        init_obj = Initialize()
        memory_obj = BotMemory()
        user_worksheet = memory_obj.user_worksheet

        print("Debug: Checking or generating user...")
        username, user_id, is_new_user = memory_obj.check_or_generate_user(user_worksheet, init_obj.username)
        print(f"Debug: Is new user? {is_new_user}")


        memory_obj.register_user(memory_obj.sh, user_id, username, is_new_user)

        # Create a new worksheet for new users
        if is_new_user:
            new_worksheet = memory_obj.create_user_worksheet(memory_obj.sh, None, user_id, username)
        else:
            worksheet_name = f"{username}_{user_id}".replace("-", "_")
            new_worksheet = memory_obj.sh.worksheet(worksheet_name)

        history = []
        user_color = init_obj.user_color

        while True:
            user_input = input(colored("You: ", user_color)).lower()
            history.append(f"You: {user_input}")

            if user_input == 'help':
                Utils.show_help()
            elif user_input in ["goodbye", "quit", "exit"]:
                Utils.exit_chat()
            elif user_input == 'history':
                past_data = memory_obj.retrieve_user_data(memory_obj.sh, user_id, username)
                Utils.show_history(past_data)
            elif user_input == 'tutorial':
                Utils.show_tutorial()
            else:
                chatbot_response = generate_response(user_input, init_obj.memory)
                print(f"Julie: {chatbot_response}")
                history.append(f"Julie: {chatbot_response}")
                memory_obj.log_interaction(new_worksheet, user_input, chatbot_response)

    except KeyboardInterrupt:
        message = random.choice(Utils.interrupt_messages)
        print(f"Unexpected exit: {message}")
    except Exception as e:
        Utils.handle_exception(e)

if __name__ == '__main__':
    main()
