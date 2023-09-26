from files.menu import main_menu
from files.julie import Julie
from files.setup import Setting
from files.brain import LongTermMemory
import click
import logging
import re
import random
from termcolor import colored

# Initialize logging
logging.basicConfig(filename='chatbot.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

# Initialize objects
julie = Julie()
memory = LongTermMemory()
settings = Setting()


class Main:
    Settings = settings
    memory = memory
    julie = julie

    def main(self):
        user_choice = main_menu()

        if user_choice == 'Exit':
            click.echo(click.style(
                "Julie: Nya~ Goodbye, senpai! See you next time! 🐾", fg='red'))
            return

        # User prompt for username with color
        username_raw = click.prompt(click.style(
            "What's your username?", fg='blue'))
        username = username_raw.lower()
        user_data = self.memory.get_user_data(username.lower())

        # Recognize user based on the data fetched
        if user_data:
            click.echo(click.style(
                f"Julie: Nya~ Welcome back, {username}! 🐾", fg='green'))
        else:
            click.echo(click.style(
                f"Julie: Nya~ Nice to meet you, {username}! 🐾", fg='green'))
        try:
            while True:
                if re.match("^[A-Za-z0-9_-]+$", username):
                    break
                else:
                    print(
                        "Invalid username. Only alphanumeric characters, hyphens, and underscores are allowed.")
            while True:
                # Keep the original user input and a lowercase version
                original_user_input = input(
                    colored("You: ", Setting.get_text_color()))
                user_input = original_user_input.lower()

                if user_input in ['exit', 'bye', 'quit', 'goodbye', 'sayonara']:
                    print("Julie: Nya~ Goodbye, senpai! See you next time! 🐾")
                    logger.info("User exited the chat.")
                    break

                try:
                    chatbot_response = self.julie.generate_response(
                        original_user_input, username)
                    Setting.simulate_typing(
                        colored(f"Julie: {chatbot_response}", Setting.get_text_color()))
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
    main_instance = Main()
    while True:
        user_choice = main_menu()
        if user_choice == 'Exit':
            break
        elif user_choice == 'Chat':
            main_instance.main()
