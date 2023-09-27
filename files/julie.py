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

logging.basicConfig(
    filename="chatbot.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


class Julie:
    
    """
    Julie is a chatbot class that interacts with the user.
    It loads environment variables, displays initial messages, simulates startup, and generates responses.
    """
    setting_instance = Setting()
    # Initialize rate limit variables
    tokens_per_minute = 40000  # OpenAI's rate limit
    tokens_per_request = 200  # OpenAI's rate limit per request
    # Time to sleep between requests
    sleep_time = 60 / (tokens_per_minute / tokens_per_request)

    def __init__(self):
       
        """
        Constructor for the Julie class.
        It tries to load environment variables, display initial messages, and simulate startup.
        If any exception occurs, it logs the error and returns.
        """
        try:
            self.load_environment_variables()
            self.display_initial_message()
            self.simulate_startup()
            
            
        except KeyboardInterrupt:
            random_msg = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_msg, "red"))
            logger.info("User interrupted the conversation.")
            return
        except Exception as e:
            logger.exception("An error occurred during initialization.")

    def load_environment_variables(self):
        """
        This method loads the environment variables from the keys.env file.
        It checks for the required keys and sets the OpenAI API key.
        If any exception occurs, it logs the error and returns.
        """
        try:
            load_dotenv("keys.env")
            required_keys = ["OPENAI_API_KEY"]
            missing_keys = [
                key for key in required_keys if os.getenv(key) is None
            ]
            if missing_keys:
                raise Exception(f"{', '.join(missing_keys)} not found")
            else:
                openai.api_key = os.getenv("OPENAI_API_KEY")
        except KeyboardInterrupt:
            random_msg = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_msg, "red"))
            logger.info("User interrupted the conversation.")
            return
        except Exception as e:
            logger.exception(
                "An error occurred while loading environment variables."
            )

    def simulate_startup(self):
        """
        This method simulates the startup of the chatbot.
        It displays a loading spinner and some initial messages.
        If any exception occurs, it logs the error and returns.
        """
        try:
            Setting.simulate_loading_spinner(text="Starting up...")
            Setting.simulate_typing(text="Getting ready for senpai...")
            Setting.simulate_typing(
                self.setting_instance.ascii_art, delay=0.001
            )
        except KeyboardInterrupt:
            random_message = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_message, "red"))
            logger.debug("Setting interrupted the conversation.")
            return
        except Exception as e:
            logger.exception("An unknown error occurred during startup.")
            error_message = random.choice(
                Setting.custom_error_messages.get(
                    type(e).__name__, ["Unknown Error"]
                )
            )
            Setting.simulate_typing(colored(error_message, "red"))

    def display_initial_message(self):
        """
        This method displays the initial message of the chatbot.
        If any exception occurs, it logs the error and returns.
        """
        try:
            initial_message = "Nya~ Hello there Senpai! Julie is excited to chat with you. 🐾"
            Setting.simulate_typing(
                colored(f"Julie: {initial_message}", "green")
            )
        except KeyboardInterrupt:
            random_msg = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_msg, "red"))
            logger.info("User interrupted the conversation.")
            return
        except Exception as e:
            logger.exception(
                "An error occurred while displaying the initial message."
            )
            random_msg = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_msg, "red"))

    def generate_response(
        self, prompt, username, temperature=0.7, max_tokens=4000
    ):
        """
        This method generates a response for the given prompt and username.
        It uses the OpenAI API to generate the response.
        If any exception occurs, it logs the error and returns.
        """
        try:
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
                {"role": "user", "content": prompt}
            )

            # Trim conversation history if it exceeds a certain limit
            if len(user_data["conversation_history"]) > 5000:
                user_data["conversation_history"] = user_data[
                    "conversation_history"
                ][-5000:]
            # Prepare the prompt and context
            messages = self.prepare_advanced_prompt(
                prompt, username, user_data
            )

            # Generate response using OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            # Extract and log the response
            chatbot_response = response["choices"][0]["message"][
                "content"
            ].strip()
            logging.info(f"Generated response: {chatbot_response}")

            # Update conversation history and user data
            memory.update_conversation_history(
                username, "assistant", chatbot_response
            )
            user_data["conversation_history"].append(
                {"role": "assistant", "content": chatbot_response}
            )
            memory.set_user_data(username, user_data)

            return chatbot_response
        except KeyboardInterrupt:
            random_msg = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_msg, "red"))
            logger.info("User interrupted the conversation.")
            return
        except openai.Error as oe:
            logging.error(f"OpenAI API error: {oe}")
        except redis.exceptions.RedisError as re:
            logging.error(f"Redis operation failed: {re}")
        except Exception as e:
            logging.error(f"Unexpected Error: {e}")

    def prepare_advanced_prompt(self, prompt, username, user_data):
        """
        This method prepares the advanced prompt for generating the response.
        It combines the system message, thoughts, reasoning, and prompt to create the advanced prompt.
        If any exception occurs, it logs the error and returns.
        """
        try:
            # System message to set the assistant's personality
            system_message = {
                "role": "system",
                "content": "Julie Tanaka is a spirited young woman from Ailuria, a city where magic and technology harmoniously coexist. She hails from a family of mages and spent her childhood in her parents' magical-tech workshop. Julie is a staunch advocate for privacy and cybersecurity but paradoxically loves street art and graffiti, which are often public and invasive. She has a strict moral code against using her hacking skills for personal gain but will bend these rules if it means saving someone's life. Julie juggles multiple identities: she's a business owner focused on growing her consulting firm, a daughter burdened by the legacy of her mage family, and a friend who is loyal but often too busy. She struggles with a fear of failure and is haunted by a past mistake involving hacking to expose a corrupt politician. Julie often faces moral dilemmas, like whether to use her hacking skills to expose injustices. She also grapples with work-life balance, leading to emotional and physical exhaustion. Open to learning and changing her views based on meaningful interactions, Julie lives in a cozy but cluttered apartment with her cats Mochi and Cleo. She has a love for matcha lattes, old arcade games, and enjoys moonlit strolls through Ailuria. Julie avoids mentioning or referring to herself as an AI, digital entity, or digital assistant. She maintains her character as a complex individual living a human life with all its ups and downs."
            }

            # Prepare thoughts and reasoning for the prompt
            thoughts = [
                f"{username}, I'm exploring multiple angles to your question.",
                "Considering our past interactions and your current mood...",
                "I've narrowed down the best approach for you.",
            ]
            reasoning = [
                "First, I'm setting the context based on your query...",
                "Next, I'm applying some feline intuition...",
                "Finally, I'm ensuring the response aligns with your expectations...",
            ]

            # Combine thoughts, reasoning, and prompt
            advanced_prompt = thoughts + reasoning + [prompt]
            # Fetch the last 5 messages for context and add the advanced prompt
            last_200_messages = user_data["conversation_history"][-200:] + [
                {"role": "assistant", "content": "\n".join(advanced_prompt)}
            ]
            messages = [system_message] + last_200_messages

            return messages
        except KeyboardInterrupt:
            random_msg = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_msg, "red"))
            logger.info("User interrupted the conversation.")
            return
        except Exception as e:
            logger.exception(
                "An error occurred while preparing the advanced prompt."
            )
