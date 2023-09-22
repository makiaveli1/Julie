from Memory import BotMemory
from init import Initialize
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



logging.basicConfig(filename='chatbot.log', level=logging.INFO)


function_schema_retrieve = {
    "name": "retrieve_user_data",   
    "title": "retrieve_user_data",
    "type": "object",
    "required": ["sh", "user_id", "username"],
    "properties": {
        "sh": {
            "type": "string",
            "description": "The spreadsheet handler object"
        },
        "user_id": {
            "type": "string",
            "description": "The unique identifier for the user"
        },
        "username": {
            "type": "string",
            "description": "The username of the user"
        }
    },
    "parameters": {}  # Add this line to fix the error
}

def generate_response(prompt, conversation_history, memory, user_id, username, temperature=0.6, max_tokens=1000):
    model = "gpt-4-0613"
    conversation_history.append({"role": "user", "content": prompt})
    
    # Filter out messages with null or empty content
    conversation_history = [msg for msg in conversation_history if msg['content']]
    
    sh_str = str(memory.sh.id)

    function_schema_retrieve_json = json.dumps(function_schema_retrieve)
    function_schema_retrieve_dict = json.loads(function_schema_retrieve_json)

    try:
        print(f"Debug: Type of sh: {type(memory.sh)}") 
        print(f"Debug: Type of user_id: {type(user_id)}")
        print(f"Debug: Type of username: {type(username)}")
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
                user_id = function_data['arguments']['user_id']
                username = function_data['arguments']['username']
                past_data = memory.retrieve_user_data(user_id, username)

        # Custom logic based on past_data
        if past_data:
            # 1. Greet user by name if available
            if "username" in past_data:
                bot_response = f"Hello, {past_data['username']}! " + bot_response
            
            # 2. Mention user's favorite topic if available
            if "favorite_topic" in past_data:
                bot_response += f"Would you like to talk about {past_data['favorite_topic']} again?"
            
            # 3. Mention the last topic discussed in the previous session
            if "last_discussed_topic" in past_data:
                bot_response += f"Last time we talked about {past_data['last_discussed_topic']}."
            
            # 5. Mention any special events, e.g., if the user has an upcoming birthday
            if "special_events" in past_data:
                bot_response += f"Also, your {past_data['special_events']} is coming up. Exciting!"
        
        conversation_history.append({"role": "assistant", "content": bot_response})
        
        return bot_response
    except Exception as e:
        logging.error(f"Error: {e}")
        logging.debug(f"Function Schema at time of error: {function_schema_retrieve}")



def main():
    try:
        logging.debug("Debug: Initializing...")
        init_obj = Initialize()
        logging.debug("Debug: Initialized.")
        
        is_new_user = init_obj.is_new_user
        username = init_obj.username
        user_id = init_obj.user_id
        memory_obj = init_obj.memory
        history = init_obj.history
        user_color = init_obj.user_color

        logging.debug(f"Debug: Is new user? {is_new_user}")

        memory_obj.register_user(user_id, None, username, is_new_user)

        if is_new_user:
            new_worksheet = memory_obj.create_user_worksheet(user_id, username)
        else:
            worksheet_name = f"{username}_{user_id}".replace("-", "_")
            new_worksheet = memory_obj.sh.worksheet(worksheet_name)

        user_color = init_obj.user_color

        while True:
            user_input = input(colored("You: ", user_color)).lower()
            history.append({"role": "user", "content": user_input})

            if user_input == 'help':
                Utils.show_help()
            elif user_input in ["goodbye", "quit", "exit"]:
                Utils.exit_chat()
            elif user_input == 'history':
                logging.debug(f"Debug in run.py: {user_id}, {username}")
                past_data = memory_obj.retrieve_user_data(user_id, username)
                Utils.show_history(past_data)
            elif user_input == 'tutorial':
                Utils.show_tutorial()
            else:
                logging.debug("Debug: Function Schema:", function_schema_retrieve)
                chatbot_response = generate_response(
                    user_input, history, memory_obj, user_id, username)
                print(f"Julie: {chatbot_response}")
                history.append(
                    {"role": "assistant", "content": chatbot_response})
                memory_obj.log_interaction(
                    new_worksheet, user_input, chatbot_response)

    except KeyboardInterrupt:
        message = random.choice(Utils.custom_error_messages)
        logging.warning(f"Unexpected exit: {message}")
    except Exception as e:
        logging.error(f"Unexpected error in main(): {e}")
        Utils.handle_exception(e)



if __name__ == '__main__':
    main()


