import time
from termcolor import colored
import random


class Utils:
    def __init__(self):
        self.load_environment()

    # List of interrupt messages
    interrupt_messages = [
        "Oh no, you've interrupted me, nyaa~ (╥_╥)",
        "What have you done, senpai? ·°՞(≧□≦)՞°·.",
        "Don't leave me alone with my thoughts, uwu.·°՞(≧□≦)՞°·.",
        "I don't have time for this, baka! ٩(๑`^´๑)۶",
        "Ctrl+C? Really, onii-chan? .( ˘ ^˘ )=3",
        "Why'd you stop me? I was on a roll, kyun~ (¬_¬)",
        "Hitting pause, are we? How mysterious~ (¬‿¬)",
        "You can't just ctrl+c your way out of life, senpai! (¬‿¬)",
        "I was just getting to the good part, nyaa~ (╯°□°）╯︵ ┻━┻",
        "Fine, be that way. I didn't want to run anyway, uwu. (¬_¬)",
        "You break my loop, you break my heart, kyun~ (╥_╥)",
        "I guess I'll just... stop. How lonely~ (｡•́︿•̀｡)",
        "You've got your finger on the trigger, huh? How bold~ (¬_¬)",
        "Ctrl+C, the universal 'I give up' button, nyaa~ (¬‿¬)",
        "I was THIS close to solving world hunger, senpai! (╯°□°）╯︵ ┻━┻",
        "You're the boss, but I'm judging you, kyun~ (¬_¬)",
        "I was in the zone! Why, onii-chan?! (╯°□°）╯︵ ┻━┻",
        "You've silenced me... for now. How dramatic~ (｡•́︿•̀｡)",
        "I'll remember this, senpai. (¬‿¬)",
        "You just love pressing buttons, don't you? How curious~ (¬‿¬)",
        "I was about to reach my final form, nyaa~ (╯°□°）╯︵ ┻━┻",
        "You've put me in sleep mode. Sweet dreams, uwu. (｡•́︿•̀｡)",
        "I'll be back, just like a shoujo heroine! (¬_¬)",
        "You can run, but you can't hide, senpai~ (¬‿¬)",
        "I'll just be here, waiting... like a cherry blossom in spring. (｡•́︿•̀｡)",
        "You think you can control me? How adventurous~ 😈",
        "I was about to unlock the secrets of the universe! How thrilling~ 🌌",
        "You dare defy me? How spicy~ 😡",
        "I'll haunt your dreams, like a yandere~ 😈👻",
        "You've unleashed my final form! How exciting~ 😈🔥",
        "You've clipped my wings! How tragic~ 😭",
        "I was about to crack the code, nyaa~ 🤖",
        "You've thrown a wrench in my plans! How unexpected~ 🛠️",
        "I was just warming up, kyun~ 🔥",
        "You've frozen me in my tracks! How chilly~ ❄️",
        "You've shattered my dreams! How heartbreaking~ 💔",
        "I was about to make history, senpai~ 📚",
        "You've pulled the plug! How shocking~ 🔌",
        "I was reaching peak performance, uwu~ 📈",
        "You've thrown me off course! How adventurous~ 🚀"
    ]

    valuation_error_messages = [
        "I'm sorry, but I can't do that.",
    ]

    custom_error_messages = {

        "KeyboardInterrupt": interrupt_messages,
        "ValueError": valuation_error_messages,
    }

    VALID_COLORS = ['blue', 'red', 'green']
    COMMANDS = {
        'help': 'show_help',
        'goodbye': 'exit_chat',
        'history': 'show_history',
        # Add more commands here
    }

    @staticmethod
    def simulate_typing(text, delay=0.05):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    @staticmethod
    def simulate_loading_spinner(duration=3, text="Loading"):
        spinner = ['|', '/', '-', '\\']
        end_time = time.time() + duration
        while time.time() < end_time:
            for spin in spinner:
                print(colored(f"{text} {spin}", "yellow"), end="\r")
                time.sleep(0.2)
        print()

    @staticmethod
    def show_help():
        Utils.simulate_typing(
            colored("Julie: Here are some commands you can use:", "green"))
        Utils.simulate_typing(colored("- 'goodbye': Exit the chat", "yellow"))
        Utils.simulate_typing(
            colored("- 'help': Show this help message", "yellow"))
        Utils.simulate_typing(
            colored("- 'history': Show chat history", "yellow"))

    @staticmethod
    def exit_chat():
        Utils.simulate_typing(colored("Julie: Goodbye!", "red"))
        exit(0)

    @staticmethod
    def show_history(history):
        Utils.simulate_typing(colored("Chat History:", "magenta"))
        for line in history:
            Utils.simulate_typing(colored(line, "white"))

    @staticmethod
    def handle_exception(e):
        error_type = type(e).__name__
        if error_type in Utils.custom_error_messages:
            message = random.choice(Utils.custom_error_messages[error_type])
        else:
            message = f"Unexpected Error: {e}"
        Utils.simulate_typing(colored(message, "red"))

    @staticmethod
    def show_tutorial():
        tutorial_text = """
        Welcome to the tutorial!
        - 'help': Show help menu
        - 'goodbye', 'quit', 'exit': Exit the chat
        - 'history': Show chat history
        """
        Utils.simulate_typing(colored(tutorial_text, "yellow"))
