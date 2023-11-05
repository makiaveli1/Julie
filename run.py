from files.menu import main_menu, clear_screen
from files.julie import Julie
from files.setup import Setting
from files.brain import LongTermMemory
import click
import logging
import re
import random
from termcolor import colored

# Improved logging format with added filename
# and line number for better debugging
logging.basicConfig(
    format="""%(asctime)s - %(name)s - %(levelname)s -
    %(message)s [%(filename)s:%(lineno)d]""",
    level=logging.INFO
)

Settings = Setting
memory = LongTermMemory()


class Main:

    def __init__(self):
        try:
            self.memory = LongTermMemory()
            self.julie = Julie()
            self.settings = Settings()
        except Exception as e:
            logging.exception("""Failed to initialize Main
            class components.""")

    def run(self):
        try:
            main_menu(Main_instance=self)
        except KeyboardInterrupt as e:
            random_msg = random.choice(Settings.interrupt_messages)
            Settings.simulate_typing(colored(random_msg, "red"))
        except Exception as e:
            logging.exception("An error occurred in run")
            print("""Sorry, something went wrong.
                  Please try restarting the program.""")

    def chat(self, username):
        clear_screen()
        try:
            user_data = self.get_user_data(username)
            if not user_data:
                user_data = {"conversation_history": []}
                self.memory.set_user_data(username, user_data)

            self.greet_user(username, user_data)

            while True:
                user_input = self.get_user_input()
                if not user_input:
                    return
                if user_input in ["exit", "bye", "quit", "goodbye",
                                  "sayonara"]:
                    return main_menu(Main_instance=self)
                self.respond_to_user(user_input, username)
        except KeyboardInterrupt as e:
            random_msg = random.choice(Settings.interrupt_messages)
            Settings.simulate_typing(colored(random_msg, "red"))
        except Exception as e:
            logging.exception("""An error occurred
                              during the chat session.""")
            print("""Sorry, an error occurred while chatting.
                  Please try again.""")

    def get_user_choice(self):
        try:
            return main_menu(Main_instance=self)
        except KeyboardInterrupt as e:
            random_msg = random.choice(Settings.interrupt_messages)
            Settings.simulate_typing(colored(random_msg, "red"))
        except Exception as e:
            logging.exception("Failed to display main menu")
            print("""Sorry, we're having trouble
                  displaying the menu right now.""")

    def register_new_user(self):
        clear_screen()
        print("Welcome! Let's set up your new account.")
        username = self.get_username(new_user=True)
        user_data = {"conversation_history": []}
        self.memory.set_user_data(username, user_data)
        self.greet_user(username, user_data)
        self.chat(username)

    def exit_chat(self):
        click.echo(click.style("""Julie: Nya~ Goodbye,
                               senpai! See you next time! 🐾""",
                               fg="red"))
        return self.julie.exit_chat()

    def get_username(self, new_user=False):
        while True:
            try:
                username_raw = click.prompt(click.style("""What's your
                                                        username?""",
                                            fg="blue")).strip()
                # Normalize the username
                normalized_username = username_raw.lower()

                # Validate the username
                if not self.is_valid_username(normalized_username):
                    print("""Invalid username. Please use only letters,
                          numbers, and underscores,
                          between 3 to 25 characters.""")
                    continue

                # For returning users, check if the username exists
                if not new_user and not self.memory.does_username_exist(
                             normalized_username):
                    print("""Username does not exist.
                          Please check your username or
                          register as a new user.""")
                    continue

                # For new users, ensure the username is not taken
                if new_user and self.memory.does_username_exist(
                                 normalized_username):
                    print("""Username already taken.
                          Please choose a different one.""")
                    continue

                return normalized_username
            except KeyboardInterrupt as e:
                random_msg = random.choice(Settings.interrupt_messages)
                Settings.simulate_typing(colored(random_msg, "red"))
            except Exception as e:
                logging.exception("Failed to get username")
                print("""Sorry, we encountered an issue
                      getting your username.
                      Please try again.""")

    def is_valid_username(self, username):
        # Define the allowed pattern for the usernames,
        # e.g., alphanumeric and underscore
        pattern = re.compile("^[a-zA-Z0-9_]+$")
        return pattern.match(username) and 3 <= len(username) <= 25

    def get_user_data(self, username):
        try:
            user_data = self.memory.get_user_data(username.lower())
            logging.info(f"Retrieved user data for {username}: {user_data}")
            return user_data
        except KeyboardInterrupt as e:
            random_msg = random.choice(Settings.interrupt_messages)
            Settings.simulate_typing(colored(random_msg, "red"))
        except Exception as e:
            logging.exception(f"Failed to get user data for {username}")
            print(f"""Sorry, we couldn't retrieve your data, {username}.
                  Please try again.""")

    def greet_user(self, username, user_data):
        if user_data.get("conversation_history"):
            click.echo(click.style(f"Julie: Nya~ Welcome back, {username}! 🐾",
                                   fg="green"))
        else:
            click.echo(click.style(f"""Julie: Nya~ Nice to meet you,
                                   {username}! 🐾""",
                                   fg="green"))

    def get_user_input(self):
        attempts = 0
        while attempts < 3:
            try:
                original_user_input = input(colored("You: ",
                                            Settings.get_text_color()))
                return original_user_input.lower()
            except KeyboardInterrupt as e:
                random_msg = random.choice(Settings.interrupt_messages)
                Settings.simulate_typing(colored(random_msg, "red"))
            except Exception as e:
                logging.exception("Failed to get user input")
                attempts += 1
                print(f"""Sorry, something went wrong.
                      Please try again. ({3 - attempts}
                      attempts left)""")
        print("""Failed to get input after several attempts.
              Please restart the chat.""")

    def respond_to_user(self, user_input, username):
        try:
            chatbot_response = self.julie.generate_response(user_input,
                                                            username)
            Settings.simulate_typing(colored(f"Julie: {chatbot_response}",
                                             Settings.get_text_color()))
        except KeyboardInterrupt as e:
            random_msg = random.choice(Settings.interrupt_messages)
            Settings.simulate_typing(colored(random_msg, "red"))
        except Exception as e:
            logging.exception("Failed to generate response")
            print("""Sorry, I couldn't understand that.
                  Could you try rephrasing?""")


if __name__ == "__main__":
    main_instance = Main()
    try:
        while True:
            user_choice = main_instance.get_user_choice()
            if user_choice == "Exit":
                break
            elif user_choice == "Chat":
                main_instance.chat(main_instance.get_username())
    except KeyboardInterrupt as e:
        random_msg = random.choice(Settings.interrupt_messages)
        Settings.simulate_typing(colored(random_msg, "red"))
    except Exception as e:
        logging.exception("""An error occurred in the
                          main execution block.""")
