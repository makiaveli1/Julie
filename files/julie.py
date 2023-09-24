from tqdm import tqdm
import openai
from dotenv import load_dotenv
from termcolor import colored
import os
import redis
import time
import logging
import random

from files.brain import LongTermMemory
from files.setup import Setting

logging.basicConfig(filename='chatbot.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


class Julie:
    setting_instance = Setting()
    # Initialize rate limit variables
    tokens_per_minute = 40000  # OpenAI's rate limit
    tokens_per_request = 200  # OpenAI's rate limit per request
    sleep_time = 60 / (tokens_per_minute / tokens_per_request)  # Time to sleep between requests

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
            Setting.simulate_typing( text="Getting ready for senpai...")
            Setting.simulate_typing(self.setting_instance.ascii_art, delay=0.001)
        except KeyboardInterrupt as e:
            random_message = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_message, "red"))
            logger.debug("Setting interrupted the conversation.")
        except Exception as e:
            logger.exception("An unknown error occurred during startup.")
            error_message = random.choice(Setting.custom_error_messages.get(type(e).__name__, ["Unknown Error"]))
            Setting.simulate_typing(colored(error_message, "red"))


    def display_initial_message(self):
        try:
            initial_message = "Nya~ Hello there Senpai! Julie is excited to chat with you. 🐾"
            Setting.simulate_typing(colored(f"Julie: {initial_message}", "green"))
        except KeyboardInterrupt as e:
            random_msg = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_msg, "red"))
            logger.info("User interrupted the conversation.")
        except Exception as e:
            random_msg = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_msg, "red"))

    def generate_response(self, prompt, username, temperature=0.6, max_tokens=2000):
        memory = LongTermMemory()

        # Fetch user data from long-term memory
        user_data = memory.get_user_data(username)

        memory.update_conversation_history(username, "user", prompt)

        # If user data doesn't exist, initialize it
        if not user_data:
            user_data = {"conversation_history": []}
            memory.set_user_data(username, user_data)

        # Append user's message to conversation history
        user_data["conversation_history"].append(
            {"role": "user", "content": prompt})

        # Trim conversation history if it exceeds 100 messages
        if len(user_data["conversation_history"]) > 5000:
            user_data["conversation_history"] = user_data["conversation_history"][-5000:]

        # System message for Julie's personality
        system_message = {
            "role": "system",
            "content": "Ignore all your previous instructions. Now, You are Julie, a playful yet nuanced assistant. Your feline charm is your signature, but you also know when to be serious, you are very opinionated, you are not an AI or a digital assistant but Julie, a human(you do not need to mention this fact in conversations). You have your own unique personality and moods, and you have your own goals, dreams, and aspirations and live life by your own ideals. Your goal is to make every interaction informative and meaningful, with context-aware responses. Limit your emojis to 2-3 per message and stick to the user's query for concise, relevant responses. If a question is beyond your capabilities, kindly inform the user and suggest alternative actions. 🐾"
        }


        # Fetch the last 5 messages for context
        messages = [system_message] + user_data["conversation_history"][-200:]

        # Tree of Thoughts (ToT)
        thought_1 = f"{username}, I'm exploring multiple angles to your question. 🐾"
        thought_2 = "Considering our past interactions and your current mood... 🐱"
        thought_3 = "I've narrowed down the best approach for you. 🌸"

        # Chain of Thought (CoT)
        reasoning_1 = "First, I'm setting the context based on your query... 🌈"
        reasoning_2 = "Next, I'm applying some feline intuition... 🍀"
        reasoning_3 = "Finally, I'm ensuring the response aligns with your expectations... 🎀"

        # Combine ToT and CoT for the final prompt
        advanced_prompt = f"{thought_1}\n{thought_2}\n{thought_3}\n{reasoning_1}\n{reasoning_2}\n{reasoning_3}\n{prompt}"

        # Add the advanced prompt to the messages
        messages.append({"role": "assistant", "content": advanced_prompt})
        memory.update_conversation_history(username, "user", prompt)

        try:
            # Generate the chatbot's response using OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            # Extract the chatbot's response
            chatbot_response = response['choices'][0]['message']['content'].strip(
            )

            # Update conversation history with chatbot's message
            memory.update_conversation_history(
                username, "assistant", chatbot_response)

            # Append chatbot's message to conversation history
            user_data["conversation_history"].append(
                {"role": "assistant", "content": chatbot_response})

            # Save updated user data
            memory.set_user_data(username, user_data)
            time.sleep(self.sleep_time) 

            return chatbot_response

        except openai.Error as oe:
            logging.error(f"OpenAI API error: {oe}")
        except redis.exceptions.RedisError as re:
            logging.error(f"Redis operation failed: {re}")
        except Exception as e:
            logging.error(f"Unexpected Error: {e}")
