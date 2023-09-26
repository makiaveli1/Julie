from files.menu import main_menu
from files.julie import Julie
from files.setup import Setting
from files.brain import LongTermMemory
import click
from logging import logger
import logging
import re
import random
from termcolor import colored

class Main:
    """
    This class is responsible for running the chatbot.
    """
    Settings = Setting
    memory = LongTermMemory()
    julie = Julie()

    def main(self):
        """
        This function runs the chatbot.
        """
        try:
            user_choice = self.get_user_choice()
            if user_choice == 'Exit':
                self.exit_chat()
                return

            username = self.get_username()
            if not username:
                return

            user_data = self.get_user_data(username)
            if not user_data:
                return

            self.greet_user(username, user_data)

            while True:
                user_input = self.get_user_input()
                if not user_input:
                    return

                if user_input in ['exit', 'bye', 'quit', 'goodbye', 'sayonara']:
                    self.exit_chat()
                    break

                self.respond_to_user(user_input, username)
        except KeyboardInterrupt as e:
            random_msg = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_msg, "red"))
            logger.info("User interrupted the conversation.")

    def get_user_choice(self):
        """
        This function displays the main menu and returns the user's choice.
        """
        try:
            return main_menu()
        except Exception as e:
            logger.error(f"Failed to display main menu: {e}")

    def exit_chat(self):
        """
        This function exits the chat.
        """
        click.echo(click.style(
            "Julie: Nya~ Goodbye, senpai! See you next time! 🐾", fg='red'))

    def get_username(self):
        """
        This function gets the user's username.
        """
        try:
            username_raw = click.prompt(click.style(
                "What's your username?", fg='blue'))
            return username_raw.lower()
        except Exception as e:
            logger.error(f"Failed to get username: {e}")

    def get_user_data(self, username):
        """
        This function gets the user's data.
        """
        try:
            return self.memory.get_user_data(username.lower())
        except Exception as e:
            logger.error(f"Failed to get user data: {e}")

    def greet_user(self, username, user_data):
        """
        This function greets the user.
        """
        if user_data:
            click.echo(click.style(
                f"Julie: Nya~ Welcome back, {username}! 🐾", fg='green'))
        else:
            click.echo(click.style(
                f"Julie: Nya~ Nice to meet you, {username}! 🐾", fg='green'))

    def get_user_input(self):
        """
        This function gets the user's input.
        """
        while True:
            try:
                # Keep the original user input and a lowercase version
                original_user_input = input(
                    colored("You: ", Setting.get_text_color()))
                return original_user_input.lower()
            except Exception as e:
                logger.error(f"Failed to get user input: {e}")

    def respond_to_user(self, user_input, username):
        """
        This function responds to the user.
        """
        try:
            chatbot_response = self.julie.generate_response(
                user_input, username)
            Setting.simulate_typing(
                colored(f"Julie: {chatbot_response}", Setting.get_text_color()))
        except Exception as e:
            logging.error(f"Failed to generate response: {e}")
            chatbot_response = "Sorry, I couldn't generate a response."
            Setting.simulate_typing(
                colored(f"Julie: {chatbot_response}", "green"))


if __name__ == "__main__":
    main_instance = Main()
    while True:
        try:
            user_choice = main_instance.get_user_choice()
            if user_choice == 'Exit':
                break
            elif user_choice == 'Chat':
                main_instance.main()
        except KeyboardInterrupt as e:
            random_msg = random.choice(Setting.interrupt_messages)
            Setting.simulate_typing(colored(random_msg, "red"))
            logger.info("User interrupted the conversation.")
        except Exception as e:
            logger.error(f"An error occurred in main: {e}")


