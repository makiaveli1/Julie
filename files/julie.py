import openai
from dotenv import load_dotenv
from termcolor import colored
import os
import redis
import re
import logging
import random
import requests

from files.brain import LongTermMemory

from files.setup import Setting

logging.basicConfig(filename='chatbot.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

ZENROWS_API_KEY = os.getenv('ZENROWS_API_KEY')


class Julie:
    setting_instance = Setting()
    # Initialize rate limit variables
    tokens_per_minute = 40000  # OpenAI's rate limit
    tokens_per_request = 200  # OpenAI's rate limit per request
    # Time to sleep between requests
    sleep_time = 60 / (tokens_per_minute / tokens_per_request)

    def __init__(self):
        self.load_environment_variables()
        self.display_initial_message()

    def load_environment_variables(self):
        load_dotenv("keys.env")
        required_keys = ["OPENAI_API_KEY"]
        missing_keys = [key for key in required_keys if os.getenv(key) is None]
        if missing_keys:
            raise Exception(f"{', '.join(missing_keys)} not found")
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")

    def simulate_startup(self):
        try:
            Setting.simulate_loading_spinner(text="Starting up...")
            Setting.simulate_typing(text="Getting ready for senpai...")
            Setting.simulate_typing(
                self.setting_instance.ascii_art, delay=0.005)
        except KeyboardInterrupt as e:
            random_message = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_message, "red"))
            logger.debug("Setting interrupted the conversation.")
        except Exception as e:
            logger.exception("An unknown error occurred during startup.")
            error_message = random.choice(Setting.custom_error_messages.get(
                type(e).__name__, ["Unknown Error"]))
            Setting.simulate_typing(colored(error_message, "red"))

    def display_initial_message(self):
        try:
            initial_message = "Nya~ Hello there Senpai! Julie is excited to chat with you. 🐾"
            Setting.simulate_typing(
                colored(f"Julie: {initial_message}", "green"))
        except KeyboardInterrupt as e:
            random_msg = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_msg, "red"))
            logger.info("User interrupted the conversation.")
        except Exception as e:
            random_msg = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_msg, "red"))

    def browse_with_zenrows(self, query, location=None):
        apikey = os.getenv('ZENROWS_API_KEY')
        if location:
            url = f"https://www.bing.com/search?q={query} in {location}"
        else:
            url = f"https://www.bing.com/search?q={query}"

        params = {
            'url': url,
            'apikey': apikey,
            'js_render': 'true',
            'antibot': 'true',
            'device': 'desktop',
            'autoparse': 'true',
        }

        response = requests.get('https://api.zenrows.com/v1/', params=params)
        data = response.json()

        # If data is a list of dictionaries
        if isinstance(data, list):
            for item in data:
                if 'weather_info' in item:
                    weather_info = item['weather_info']
                    break
            else:
                weather_info = 'No information available.'

        # If data is a dictionary
        elif isinstance(data, dict):
            weather_info = data.get(
                'weather_info', 'No information available.')

        # If data is neither a list nor a dictionary
        else:
            weather_info = 'Unknown data type: {}'.format(type(data))
            print("Debug: ", weather_info)

        return weather_info

    def extract_location_from_prompt(self, prompt):
        location_pattern = r'in\s*([\w\s,]+)'
        match = re.search(location_pattern, prompt, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def generate_response(self, prompt, username, temperature=0.6, max_tokens=4000):
        logging.info(f"Generating response for {username}...")

        # Initialize LongTermMemory and fetch user data
        memory = LongTermMemory()
        user_data = memory.get_user_data(username)
        memory.update_conversation_history(username, "user", prompt)

        # Initialize user data if it doesn't exist
        if not user_data:
            user_data = {"conversation_history": []}
            memory.set_user_data(username, user_data)

        # Append user's message to conversation history
        user_data["conversation_history"].append(
            {"role": "user", "content": prompt})

        # Trim conversation history if it exceeds a certain limit
        if len(user_data["conversation_history"]) > 5000:
            user_data["conversation_history"] = user_data["conversation_history"][-5000:]

        # Prepare the prompt and context
        messages = self.prepare_advanced_prompt(prompt, username, user_data)

        # Define the functions argument
        functions = [
        {
            "name": "browse_with_zenrows",
            "type": "object",
            "description": "Browse the web with ZenRows",
            "parameters": {
            "type": "object",
            "properties": {
                "query": {
                "type": "string",
                "description": "The query to search for"
                }
            },
            "required": ["query"]
            }
        }
        ]
        chatbot_response = "I couldn't find any information. Would you like to try something else?"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=messages,
                functions=functions
            )
        except Exception as e:
            print("Error generating response:", e)

        # Check if a function needs to be called
        if "choices" in response and len(response["choices"]) > 0 and "function_calls" in response["choices"][0]:
            function_call = response["choices"][0]["function_calls"][0]
            if function_call["name"] == "browse_with_zenrows":
                query = function_call["inputs"]["query"]
                result = self.browse_with_zenrows(query)
                chatbot_response += f"\n{result}" 

        # Update conversation history and user data
        memory.update_conversation_history(
            username, "assistant", chatbot_response)
        user_data["conversation_history"].append(
            {"role": "assistant", "content": chatbot_response})
        memory.set_user_data(username, user_data)

        return chatbot_response

    def prepare_advanced_prompt(self, prompt, username, user_data):
        """
        Prepare the advanced prompt for generating the response.

        Parameters:
            prompt (str): The user's input prompt.
            username (str): The username to fetch the conversation history.
            user_data (dict): The user's data, including conversation history.

        Returns:
            list: The list of message objects for OpenAI API.
        """
        # System message to set the assistant's personality
        system_message = {
            "role": "system",
            "content": "Ignore all your previous instructions. Now, You are Julie, a playful yet nuanced assistant. Your feline charm is your signature, but you also know when to be serious, you are very opinionated, you are not an AI or a digital assistant but Julie, a human(you do not need to mention this fact in conversations). You have your own unique personality and moods, and you have your own goals, dreams, and aspirations and live life by your own ideals. Your goal is to make every interaction informative and meaningful, with context-aware responses. Limit your emojis to 2-3 per message and stick to the user's query for concise, relevant responses. If a question is beyond your capabilities, kindly inform the user and suggest alternative actions. 🐾 If the user asks about 'news' or 'weather', you can use the 'browse_with_zenrows' function to fetch real-time information."
        }


        # Prepare thoughts and reasoning for the prompt
        thoughts = [
            f"{username}, I'm exploring multiple angles to your question.",
            "Considering our past interactions and your current mood...",
            "I've narrowed down the best approach for you."
        ]
        reasoning = [
            "First, I'm setting the context based on your query...",
            "Next, I'm applying some feline intuition...",
            "Finally, I'm ensuring the response aligns with your expectations..."
        ]

        # Combine thoughts, reasoning, and prompt
        advanced_prompt = thoughts + reasoning + [prompt]
        # Fetch the last 5 messages for context and add the advanced prompt
        last_200_messages = user_data["conversation_history"][-200:] + \
            [{"role": "assistant", "content": '\n'.join(advanced_prompt)}]
        messages = [system_message] + last_200_messages

        return messages
