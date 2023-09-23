import openai
from dotenv import load_dotenv
from termcolor import colored
import os
import redis
import random
import logging

from files.julie import Julie
from files.setup import Setting

logging.basicConfig(filename='chatbot.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


class Main:
    Settings = Setting()
    julie = Julie()

    def main(self):
        try:
            username = input("What's your username? ")

            while True:
                user_input = input(colored("You: ", 'green')).lower()
                if user_input in ['exit', 'bye', 'quit', 'goodbye', 'sayonara']:
                    print("Julie: Nya~ Goodbye, senpai! See you next time! 🐾")
                    logger.info("User exited the chat.")
                    break

                try:
                    chatbot_response = chatbot_response = self.julie.generate_response(
                        user_input, username)
                    Setting.simulate_typing(
                        colored(f"Julie: {chatbot_response}", "green"))
                except Exception as e:
                    logging.error(f"Failed to generate response: {e}")
                    chatbot_response = "Sorry, I couldn't generate a response."
                    Setting.simulate_typing(
                        colored(f"Julie: {chatbot_response}", "green"))

        except KeyboardInterrupt as e:
            random_msg = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_msg, "red"))
            logger.info("User interrupted the conversation.")

        except Exception as e:
            error_type = type(e).__name__
            random_msg = random.choice(
                Setting.custom_error_messages.get(error_type, ["Unknown Error"]))
            Setting.simulate_typing(colored(random_msg, "red"))
            logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    Main().main()
