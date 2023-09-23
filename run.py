import openai
from dotenv import load_dotenv
import time
from termcolor import colored
import json
import os
import random
import redis
import logging
from jsonschema import validate, ValidationError
import logging


logging.basicConfig(filename='chatbot.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


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


def simulate_typing(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def simulate_loading_spinner(duration=3, text="Loading"):
    spinner = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    while time.time() < end_time:
        for spin in spinner:
            print(colored(f"{text} {spin}", "yellow"), end="\r")
            time.sleep(0.2)
    print()


def show_help():
    simulate_typing(
        colored("Julie: Here are some commands you can use:", "green"))
    simulate_typing(colored("- 'goodbye': Exit the chat", "yellow"))
    simulate_typing(colored("- 'help': Show this help message", "yellow"))
    simulate_typing(colored("- 'history': Show chat history", "yellow"))


def exit_chat():
    simulate_typing(colored("Julie: Goodbye!", "red"))
    exit(0)


def show_history(history):
    simulate_typing(colored("Chat History:", "magenta"))
    for line in history:
        simulate_typing(colored(line, "white"))


ascii_art = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⢠⣿⣿⣿⣶⣶⣤⣤⣀⡀⠀⠀⠀⠀⠀⢠⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡄⠀⠀⠀⠀⠀⢀⣀⣤⣤⣴⣶⣾⣿⣿⡆⢰⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣾⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠶⣦⣄⡀⣴⠿⢷⠦⢤⣤⣤⣤⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⠃⠀⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢀⣽⣿⡇⠀⢈⣇⣸⣥⣿⣿⣬⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣯⡴⠟⠉⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⠿⠛⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣧⠀⠉⠀⠀⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣟⡉⠁⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⣀⣠⡀⣤⣀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣦⡀⠀⠀⠀⠈⠙⠛⠛⠛⠛⠛⣻⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⠿⣶⣄⡀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣀⣤⣴⣶⣿⣿⣿⣋⣤⣈⣻⣿⣿⣶⣶⣤⣄⣸⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⣠⡾⢿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⣿⣿⣿⣿⣿⠀⠈⠛⠿⣦⣴⣶⣿⣟⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠀⠀⣀⣀⣤⡴⠞⠋⠀⣼⣿⣿⣿⣿⡿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠉⠛⠿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣾⠿⠛⠋⠁⠀⠀⠀⣰⣿⣿⣿⣿⣿⠇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣤⣀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⡿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠻⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⣀⣤⣾⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⢻⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣽⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⣀⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣾⣿⣿⣿⣿⡿⣿⢿⣿⣿⣿⣿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣿⣿⣿⣿⡿⣾⣿⣿⣿⣿⣿⣷⣾⣿⡏⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⠋⣠⣿⣿⣿⣿⣿⣿⣾⣧⣾⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⠥⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀
⣴⣦⣤⠠⣦⣤⣠⣤⣤⠀⠀⠀⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢻⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⢹⣿⣿⣿⣿⣿⣿⣿⣿⡉⠀⠀⠀⠀⠀
⠻⠿⠟⠛⠛⠛⠛⠻⠟⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠈⠉⠉⢿⡟⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⡇⠀⠻⣏⠉⠏⠁⠙⢿⣿⣿⣷⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠏⣾⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⣶⠀⣰⡟⠀⠀⠈⣿⡀⣹⣿⣭⣿⡟⠀⢸⣿⣭⣿⠏⣠⣾⠃⠀⠀⠹⣧⠀⠙⠀⠈⣿⣿⡿⣿⣿⣿⣿⣿⣿⢿⣿⠘⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⠀⣿⣧⣄⠉⠛⠋⢹⣿⣿⣿⢇⣤⣶⣿⣾⣿⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣷⣶⣷⣦⣼⣿⣿⢻⡏⠉⠛⠉⢡⣬⣿⡇⠸⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢶⣶⣤⣼⣤⣤⣿⣿⣿⣧⢀⠀⠀⢿⣿⣿⣿⣿⣿⣿⡟⢻⣿⣿⣋⣿⣿⡏⢻⣿⣿⣿⣿⠿⣿⣿⣿⣿⡿⢻⣿⣿⣏⣿⣿⣿⠹⣿⣿⣿⣿⣿⣿⣎⠁⠀⠀⢠⣽⣿⣿⣧⣤⣽⣤⣶⣶⠄
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣹⣿⣿⣿⣿⣿⣿⠀⣿⡗⠀⣾⣿⣿⣿⣿⣿⡟⠀⢸⣿⡿⣿⣿⣿⡇⠀⠙⢿⣿⣿⣴⣿⣿⣿⠟⠁⢸⡿⣟⡿⢿⡿⡇⠀⢻⣿⣿⣿⣿⣿⣿⡀⢀⣷⡀⣿⣿⣿⣿⣿⣿⣿⡁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢸⣿⣿⣿⣿⣿⣿⣷⠀⠘⡟⢻⣭⣿⠟⣿⠀⠀⠀⠀⠙⠿⠋⠁⠀⠀⠀⣸⠃⣿⣠⣾⢿⠇⠀⢸⣿⣿⣿⣿⣿⣿⣧⢸⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⣿⠘⢿⣿⡟⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠛⠟⠃⢸⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇
⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣀⣼⣦⣤⣶⡿⠛⠀⠀⠀⠀⠀⣶⠆⠀⠀⠀⠀⠙⠻⣶⡤⠤⠿⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⢠⡟⣿⣿⣿⣿⣿⣷⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡋⢿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⡾⠆⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠸⣿⣿⣿⣿⣟⣿
⠀⠀⠀⠀⠀⠀⠀⣷⠀⠙⠛⢿⣟⠋⣶⡹⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠠⢤⠤⢤⡶⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⡿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣀⠀⣛⣽⠏⠁⠀⣽
⠀⠀⠀⠀⠀⠀⠀⢹⡇⠀⠀⢀⣙⣳⣿⣷⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣴⣾⣿⣿⣿⣿⡿⠃⢀⣿⣿⣿⣿⣿⣿⣿⣿⣧⣾⣿⣾⣏⡁⠀⠀⢸⡟
⠀⠀⠀⠀⠀⠀⠀⠀⢻⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣤⣄⣀⠀⢀⣀⣤⣤⣶⣾⣿⣿⣿⣿⣿⡿⠋⠁⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣯⠛⠿⢿⣿⠻⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠻⢿⣿⠿⢿⣿⠻⢯⣭⠉⣭⣭⠟⢻⣿⠿⢻⣿⠿⠋⠉⠀⠀⣠⣾⣿⣿⣫⣿⡿⣿⣿⠿⢿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣷⠶⣤⣿⣇⡈⣿⣿⣿⣿⡟⢿⣿⣷⠄⣀⣀⣤⣤⣼⡁⠀⢸⢻⣶⡏⡿⠀⠀⣷⣤⣤⣄⣀⠀⠀⣠⡾⢿⣿⣿⣿⣿⣿⣷⣿⣥⡴⢾⣿⣿⣿⣿⣿⠟⠋⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⢿⣿⣧⣀⡀⠉⠉⠛⠛⣿⠿⠷⠚⠛⠋⢫⠉⠀⠀⠀⣿⠀⠀⢸⣿⡟⣇⡇⠀⠀⢸⠀⠀⠀⠈⢉⡟⠛⠛⠾⠿⢿⡟⠛⠉⠉⠁⣀⣴⣿⡿⠿⠛⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⢸⠃⠀⠀⣄⡀⠀⣟⠳⣄⠀⠀⠘⠷⢤⣼⠿⠀⠹⣷⣤⠶⠋⠀⠀⣠⡴⢻⡇⠀⣀⡄⠀⠈⣇⠀⠀⠀⠀⠉⠁⣀⣄⣀⣀⣀⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⡄⠀⠀⠈⠙⢧⠙⢦⣌⡙⠶⢤⣀⡀⠀⠀⠀⠀⠀⠀⣀⣠⠴⠚⣁⡤⠾⣴⢛⡇⠀⠀⠀⣿⡆⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⡷⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⢿⡻⣄⡀⠀⠀⢨⣷⡀⠀⠉⠙⠲⢬⣽⣗⣦⣴⣶⣞⣻⡥⠶⠚⠉⠁⢀⣼⣧⠘⠀⠀⣠⣾⡿⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⠈⠛⠮⠟⠒⠒⣿⡿⡿⣆⠀⠀⠀⠘⠿⢿⣿⠷⢿⣿⠟⠀⠀⠀⠀⢠⣾⣿⣿⡗⠒⠛⠯⠞⠁⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡏⡟⠊⠓⠦⠤⢴⣿⡷⣧⠈⠳⣄⡀⠀⣴⠟⣿⡀⣼⠙⢦⡀⠀⣠⠴⠋⣸⢿⣿⣧⠤⠤⠀⠉⢻⡎⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⠷⠦⠤⠤⠤⣾⣿⣇⣿⠙⠶⢤⣙⣻⠵⠶⠎⠉⠉⠶⠦⣿⢋⣡⠴⠚⣽⣾⣿⣿⠠⠤⠤⠴⠾⠃⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠻⣆⡀⠀⠀⠀⡏⣿⢩⣿⡄⠀⠀⠀⢹⠀⠀⣶⠖⣶⠀⠀⣿⠀⠀⠀⢀⣿⠀⢿⣿⡄⠀⠀⢀⣠⠞⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣸⡀⠉⠉⢻⢀⣿⡿⢦⣿⠙⢦⡀⠀⠈⠳⣤⣹⣦⣞⣠⡶⠃⠀⢀⣠⠟⢸⣴⢿⣿⡇⢻⠋⠉⠀⢀⣽⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇⠈⠙⠓⠒⠋⣸⢿⠇⢠⣽⠳⠦⣭⣷⣶⣿⡗⣛⣋⣾⢻⣦⣶⣾⣭⡤⠖⢻⡇⠈⣿⢷⠘⠒⠒⠋⠉⢹⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡗⠶⢤⣤⡄⣰⣇⡼⣠⣄⣻⣴⣄⣤⡤⠤⢔⣛⣏⣿⣝⣛⡳⢤⠤⣤⣤⣦⣾⣧⣤⢿⣜⣇⠠⣤⡤⠴⢺⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⡧⣤⣤⠀⣰⣏⣼⡇⠒⠒⠒⠓⠂⠀⠉⠉⠉⠉⠁⠀⠀⠈⠉⠉⠉⠛⠛⠛⠓⠒⠛⢺⣷⣘⣧⡀⣠⣤⣤⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⣿⠀⠀⠀⠘⠋⢸⢿⢃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣏⣧⠈⠛⠀⠀⠀⢻⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⢧⡟⢶⣤⣀⠀⠀⡟⣾⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠸⡆⠀⢀⣠⣴⠻⡏⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠾⣅⣀⠀⠉⠙⣻⠇⣯⣌⡙⠲⢤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡤⠶⢛⣉⣼⡆⣟⠛⠉⠀⢀⣠⡿⢿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇⠀⠀⠈⠉⠛⠓⣿⠀⣧⡀⠈⠙⠲⠦⢬⣙⣛⣶⠆⠀⠀⠀⠀⠀⠀⢐⣒⣋⡭⠤⠖⠛⠉⣄⣸⡇⢹⠖⠛⠋⠉⠀⠀⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠻⢦⣀⢀⣀⣀⣠⡇⠀⣇⠙⢦⣄⠀⠀⠀⠀⠀⠉⠁⠀⠈⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⢀⡴⠟⢹⡇⠸⣦⣄⣀⡀⣀⣤⠞⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣦⣄⣸⠹⣇⣀⣼⠁⡞⣟⠳⢤⣈⠛⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠞⢉⣤⠖⣿⢿⡄⢷⣀⣈⡇⣿⣡⣤⣾⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⠀⠈⠉⠀⣿⢩⠏⢰⣿⣿⡄⠀⠈⡛⠲⠤⣍⣓⡲⠤⢤⣀⣀⣀⣠⠤⠴⣒⣋⡥⠴⠚⠉⠀⣼⡟⣸⡇⠘⣏⢹⠃⠉⠉⠀⢻⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⠓⠦⢤⣀⣻⡎⠀⢸⣿⣿⢻⣄⡀⠹⣆⠀⠀⠉⠉⠛⠓⠚⠛⠛⠒⠚⠉⠉⠀⠀⠀⠘⢀⣴⡿⣱⣿⠇⠀⢹⣾⢀⣠⠤⠖⠛⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣟⠳⠦⣄⡀⠈⢻⡇⠀⠀⢿⡿⣧⢹⡟⠳⣌⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⢋⡟⣱⢿⣿⠀⠀⢸⡟⠉⢀⣀⡤⠞⢻⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⣻⠀⠀⠀⠉⠳⣦⡇⠀⠀⢸⡇⠘⢿⣿⣗⠮⣗⣀⡀⠀⣠⣀⣀⠀⣀⣀⣀⠀⠀⣀⣼⡿⢖⣿⡗⠋⢸⡇⠀⠀⢸⣧⡞⠋⠁⠀⠀⣿⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠃⠻⣤⣀⠀⠀⠀⢸⡇⠀⠀⢸⢷⣄⡀⢻⣹⣷⣼⣯⣹⣽⡟⠁⠉⠉⠉⠡⢉⣯⣭⣥⣤⣾⣿⣾⠁⣁⡼⢷⠀⠀⠘⣿⠀⠀⠀⢀⣠⡾⠀⣷⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⢳⣤⣀⠉⠉⠙⠛⢻⡇⠀⠀⢸⠀⠈⠉⠛⢷⡿⣿⣟⠛⠛⢧⡀⠀⠀⢀⣤⣼⠛⠛⣛⣿⣽⣶⠟⠋⠉⠀⢸⠀⠀⠀⣿⠛⠋⠉⠉⢁⣠⡴⢛⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡄⠀⠉⠉⠛⠒⠒⣾⡇⠀⠀⢸⠀⠀⠀⠀⠀⠉⠀⠈⠙⠷⠾⣿⣶⠛⠳⡾⠷⠖⠋⠁⠀⠈⠉⠀⠀⠀⠀⢸⠀⠀⠀⣿⡒⠚⠛⠋⠉⠁⠀⣾⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣯⡷⣄⡀⠀⢀⣤⡶⣿⠃⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡇⠀⢠⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⢿⠷⢤⣄⠀⠀⣠⣼⣥⡟⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣧⡈⣻⠷⢶⡶⣷⡟⠀⠀⠀⣾⢦⣀⡀⠀⠀⠀⠀⢀⣀⣠⡴⢻⠃⠀⠀⣏⠳⣤⣀⡀⠀⠀⠀⠀⠀⣀⣠⢾⠀⠀⠀⠘⣟⠳⣾⠶⣿⠉⣸⣿⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡟⣿⣿⣿⣸⣿⣴⠟⠁⠀⠀⠀⣿⡲⠦⢭⣝⣛⣻⡯⠽⠟⠉⣠⡾⠀⠀⠀⢻⣤⡌⠛⠯⠿⣛⣛⣻⣯⠭⢶⣿⡇⠀⠀⠀⠘⠦⣽⣆⣸⣶⣿⣧⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⣇⠀⠀⠉⠙⠛⠉⠉⠛⠛⠛⢉⡇⠀⠀⠀⢘⡏⠙⠛⠛⠋⠉⠛⠋⠀⠀⠀⢈⡇⠀⠀⠀⠀⠀⠀⠀⢿⣯⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣯⡉⠓⠒⠲⠶⠶⠶⠶⢶⣶⣾⡇⠀⠀⠀⢸⣿⢶⡶⠶⠶⠶⠶⠒⠒⠚⠋⣹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠉⠓⠒⠒⠒⠒⠒⠚⠉⢁⣿⡇⠀⠀⠀⠀⣿⡄⠉⠛⠒⠒⠒⠒⠒⠒⠋⠉⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⠲⠦⠤⠤⠤⠤⠤⠴⠶⣿⣿⠁⠀⠀⠀⠀⢿⢻⡷⠶⠤⠤⠤⠤⠤⠤⠖⠚⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀🍙♡‹𝟹㊗🎧

"""
VALID_COLORS = ['blue', 'red', 'green']
COMMANDS = {
    'help': show_help,
    'goodbye': exit_chat,
    'history': show_history,
    # Add more commands here
}


def handle_exception(e):
    error_type = type(e).__name__
    if error_type in custom_error_messages:
        message = random.choice(custom_error_messages[error_type])
    else:
        message = f"Unexpected Error: {e}"
    simulate_typing(colored(message, "red"))


def show_tutorial():
    tutorial_text = """
    Welcome to the tutorial!
    - 'help': Show help menu
    - 'goodbye', 'quit', 'exit': Exit the chat
    - 'history': Show chat history
    """
    simulate_typing(colored(tutorial_text, "yellow"))


class LongTermMemory:
    def __init__(self, redis_host, redis_port, redis_password, redis_username):
        self.schema = {
            "type": "object",
            "properties": {
                "conversation_history": {"type": "array"}
            }
        }
        self.test_connection(redis_host, redis_port, redis_password, redis_username)
        try:
            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                username=redis_username,
                password=redis_password,
                socket_timeout=60 
            )
            self.redis_client.ping()
            print('Connected!')
        except redis.ConnectionError:
            print('Connection failed.')
            logging.info(
                f"Connected to Redis server at {redis_host}:{redis_port}")
        except redis.exceptions.AuthenticationError:
            logging.error(
                "Authentication failed: invalid username-password pair")
            raise
        except Exception as e:
            logging.error(f"Failed to connect to Redis server: {e}")
            raise e 

    def load_data(self, username):
        try:
            user_data = self.redis_client.get(username)
            if user_data:
                validate(instance=json.loads(user_data),
                         schema=self.schema)  # Add this line
            logging.info(f"Loaded user data for {username}")
            return json.loads(user_data) if user_data else {}
        except redis.exceptions.RedisError:
            logging.error(f"Redis operation failed for {username}")
        except Exception as e:
            logging.error(f"Failed to load user data for {username}: {e}")

    def get_user_data(self, username):
        """Get user data from Redis using the username as the key.

        Args:
            username (str): The username of the user.

        Returns:
            dict: The user data in JSON format, or an empty dict if not found.
        """
        return self.load_data(username)

    def set_user_data(self, username, user_data):
        """Set user data to Redis using the username as the key.

        Args:
            username (str): The username of the user.
            user_data (dict): The user data in JSON format.

        Raises:
            ValidationError: If the user data does not match the schema.
        """
        schema = {
            "type": "object",
            "properties": {
                "conversation_history": {"type": "array"}
            }
        }
        try:
            validate(instance=user_data, schema=schema)
            self.redis_client.set(username, json.dumps(user_data))
            logging.info(f"Saved user data for {username}")
        except redis.exceptions.RedisError:
            logging.error(f"Redis operation failed for {username}")
        except Exception as e:
            logging.error(f"Failed to load user data for {username}: {e}")

    def update_role_in_data(self, username):
        """Update the role field in the user data from 'chatbot' to 'assistant'.

        Args:
            username (str): The username of the user.
        """
        user_data = self.get_user_data(username)
        for message in user_data.get("conversation_history", []):
            if message["role"] == "chatbot":
                message["role"] = "assistant"
        self.set_user_data(username, user_data)

    def update_conversation_history(self, username, role, content):
        """Update the conversation history in the user data with a new message.

        Args:
            username (str): The username of the user.
            role (str): The role of the sender, either 'user' or 'assistant'.
            content (str): The content of the message.
        """
        key = f'chat:{username}'
        value = json.dumps({"role": role, "content": content})
        try:
            # Use Redis list to store the conversation history
            self.redis_client.lpush(key, value)
            logging.info(
                f"Added message to conversation history for {username}")

            # Trim conversation history if it exceeds 5000 messages
            self.redis_client.ltrim(key, 0, 5000)
            logging.info(f"Trimmed conversation history for {username}")
        except Exception as e:
            logging.error(
                f"Failed to update conversation history for {username}: {e}")

    def test_connection(self, redis_host, redis_port, redis_password, redis_username):
        try:
            test_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                username=redis_username,
                password=redis_password
            )
            test_client.ping()
            logging.info(f"Successfully connected to Redis.")
        except Exception as e:
            logging.error(f"Failed to connect to Redis: {e}")
            raise e


class Julie:
    def __init__(self):
        self.load_environment_variables()
        self.simulate_startup()
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
        simulate_typing("starting up...")
        simulate_loading_spinner(
            duration=3, text="Getting ready for senpai...")
        simulate_typing(ascii_art, delay=0.001)

    def display_initial_message(self):
        initial_message = "Nya~ Hello there Senpai! Julie is excited to chat with you. 🐾"
        simulate_typing(colored(f"Julie: {initial_message}", "green"))

    def generate_response(self, prompt, username, temperature=0.6, max_tokens=1000):
        # Initialize LongTermMemory
        print("Initializing LongTermMemory...")
        memory = LongTermMemory(
            redis_host='redis-13074.c1.eu-west-1-3.ec2.cloud.redislabs.com',
            redis_port=13074,
            redis_username='default',
            redis_password='ZwyemqBAp8Pc7jFKJlt1az90NH4ufKke'
            )


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
            "content": "You are Julie, a playful and cheerful assistant with a knack for brightening people's day. You love using playful emojis and sprinkling your conversations with a touch of humor. You're also a bit of a cat enthusiast, so you occasionally slip in some feline-inspired phrases. Your goal is to make every interaction memorable and delightful, leaving people with a smile on their face. 🐾🌈"
        }

        # Fetch the last 5 messages for context
        messages = [system_message] + user_data["conversation_history"][-5:]

        # Tree of Thoughts (ToT)
        thought_1 = f"Nya~ {username}-san, Julie is pondering your question with her kitty senses. 🐾"
        thought_2 = "Hmm, Julie recalls some of our past chats, nya~ 🐱"
        thought_3 = "Eureka! Julie has crafted the purr-fect response just for you, {username}-san! 🌸"

        # Chain of Thought (CoT)
        reasoning_1 = "Firstly, Julie considers what you like, nya~ 🌈"
        reasoning_2 = "Secondly, Julie applies her feline intuition, nya~ 🍀"
        reasoning_3 = "Lastly, Julie remembers our previous heart-to-heart talks, nya~ 🎀"

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

            return chatbot_response

        except openai.Error as oe:
            logging.error(f"OpenAI API error: {oe}")
        except redis.exceptions.RedisError as re:
            logging.error(f"Redis operation failed: {re}")
        except Exception as e:
            logging.error(f"Unexpected Error: {e}")

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
                    chatbot_response = self.generate_response(
                        user_input, username)
                    simulate_typing(
                        colored(f"Julie: {chatbot_response}", "green"))
                except Exception as e:
                    logging.error(f"Failed to generate response: {e}")
                    chatbot_response = "Sorry, I couldn't generate a response."
                    simulate_typing(
                        colored(f"Julie: {chatbot_response}", "green"))

        except KeyboardInterrupt:
            print("User interrupted the conversation.")
            logger.info("User interrupted the conversation.")
        except Exception as e:
            print(f"An error occurred: {e}")
            logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    julie = Julie()  # Note the lowercase 'j' to avoid naming conflict with the class
    julie.main()
