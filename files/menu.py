import click
import os
import shutil
from InquirerPy import prompt
from pyfiglet import Figlet
from termcolor import colored
from files.setup import Setting
import random


def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system("cls" if os.name == "nt" else "clear")


def center_text(text):
    """
    Centers the given text according to the terminal width.

    Args:
        text (str): The text to be centered.

    Returns:
        str: The centered text.
    """
    terminal_width = shutil.get_terminal_size().columns
    centered_text = text.center(terminal_width)
    return centered_text


def display_menu_content(content):
    """
    Displays the menu content in a formatted manner.

    Args:
        content (dict): The content to be displayed. The keys are the titles and the values are the descriptions.
    """
    for title, description in content.items():
        print(center_text(f"\n🌟 {title} 🌟"))
        print(
            center_text("--------------------------------------------------")
        )
        for line in description:
            print(center_text(line))


def display_help_menu():
    """
    Displays the help menu with a brief introduction about Julie and the guidelines for interacting with the main menu.
    """
    f = Figlet(font="slant")
    title_ascii = f.renderText("Julie's world")
    print(center_text(title_ascii))
    print(center_text("🐾🌟🐾🌟🐾🌟🐾🌟🐾🌟🐾"))

    content = {
        "WHO IS JULIE?": [
            "🌈 Greetings, I am Julie, your spirited and playful catgirl from the bustling city of Ailuria!",
            "🎮 I was once a renowned hacker, but a twist of fate led me to you.",
            "🌙 Now, I use my tech-savvy skills and magical abilities to assist and enchant!",
            "I love matcha lattes, retro video games, and moonlit walks. 🌙",
        ],
        "WHAT CAN I DO?": [
            "From playful banter to deep discussions, I aim to make every interaction enchanting!",
            "Don't be shy; whether it's advice you seek or just a chat, I've got your back! 🎮",
        ],
        "HOW TO INTERACT WITH ME?": [
            "1️⃣ Introduce Yourself: Let's get to know each other better!",
            "2️⃣ Ask Questions: Curiosity never killed the catgirl! 🐱",
            "3️⃣ Chat: Share your thoughts; I'm all ears!",
        ],
        "MY MEMORY": [
            "I have a Long-Term Memory system, making our conversations even more personalized and engaging."
        ],
        "GUIDELINES FOR INTERACTING WITH THE MAIN MENU": [
            "🔹 Navigation: Use arrow keys or type the option number.",
            "🔹 Selection: Press 'Enter' to select and proceed.",
            "🔹 Back & Exit: 'Back' or 'Exit' options are your friends.",
            "🔹 Help: Type 'Help' for this guide.",
        ],
    }

    display_menu_content(content)

    print(
        center_text(
            "\nLet's make your day not just better, but enchanting! 😸"
        )
    )
    print(center_text("🐾🐾🐾🐾🐾🐾🐾🐾🐾🐾🐾🐾🐾🐾🐾🐾"))
    input(center_text("Press Enter to continue..."))


def settings_menu():
    """
    Displays the settings menu where the user can change the text color.
    """
    questions = [
        {
            "type": "list",
            "message": "Choose an option:",
            "choices": ["Change Text Color", "Back"],
            "name": "option",
        },
        {
            "type": "list",
            "message": "Enter new text color:",
            "choices": Setting.available_colors,
            "name": "new_color",
            "when": lambda x: x["option"] == "Change Text Color",
        },
    ]
    result = prompt(questions)
    if result.get("option") == "Change Text Color":
        Setting.user_text_color = result["new_color"]
    clear_screen()


def main_menu():
    """
    Displays the main menu where the user can choose to chat, change settings, view help, or exit.

    Returns:
        str: The option chosen by the user.
    """
    clear_screen()
    try:
        option = prompt(
            [
                {
                    "type": "list",
                    "message": "What would you like to do?",
                    "choices": ["Chat", "Settings", "Help", "Exit"],
                    "name": "option",
                }
            ]
        ).get("option")
        click.echo(
            click.style(
                f"You chose: {option.capitalize()}",
                fg=Setting.get_text_color(),
            )
        )
        if option == "Settings":
            settings_menu()
            return main_menu()
        elif option == "Help":
            display_help_menu()
            return main_menu()
        return option.capitalize()
    except KeyboardInterrupt:
        random_msg = random.choice(Setting.interrupt_messages)
        Setting.simulate_typing(colored(random_msg, "red"))
        return "Exit"

