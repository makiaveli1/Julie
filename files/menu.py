import click
import os
import shutil
from InquirerPy import prompt
from pyfiglet import Figlet
from termcolor import colored
from files.setup import Setting


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    

def center_text(text):
    terminal_width = shutil.get_terminal_size().columns
    centered_text = []

    # Split the text by newline characters and center each line
    for line in text.split("\n"):
        left_padding = (terminal_width - len(line)) // 2
        centered_line = " " * left_padding + line
        centered_text.append(centered_line)

    # Join the centered lines back into a single string
    return "\n".join(centered_text)
    
    

def display_help_menu():
    f = Figlet(font='slant') 
    title_ascii = f.renderText('🌸 WELCOME TO JULIE! 🌸 ')
    
    # Center-align each line of the ASCII art
    centered_title_ascii = center_text(title_ascii)
    
    # Displaying the centered ASCII title with a colored background
    print(colored(centered_title_ascii, 'white', 'on_blue'))
    
    # Displaying the ASCII title
    print(center_text("=== 🌸 WELCOME TO JULIE! 🌸 ==="))
    
    # Adding extra flair with cat paw
    print(center_text("🐾🌟🐾🌟🐾🌟🐾🌟🐾🌟🐾"))
    
    # Who is Julie?
    print(center_text("\n🌟 WHO IS JULIE? 🌟"))
    print(center_text("--------------------------------------------------"))
    print(center_text("🌈 Greetings, I am Julie, your spirited and playful catgirl from the bustling city of Ailuria!"))
    print(center_text("🎮 I was once a renowned hacker, but a twist of fate led me to you."))
    print(center_text("🌙 Now, I use my tech-savvy skills and magical abilities to assist and enchant!"))
    print(center_text("I love matcha lattes, retro video games, and moonlit walks. 🌙"))
    
    # What Can I Do?
    print(center_text("\n🌈 WHAT CAN I DO? 🌈"))
    print(center_text("--------------------------------------------------"))
    print(center_text("From playful banter to deep discussions, I aim to make every interaction enchanting!"))
    print(center_text("Don't be shy; whether it's advice you seek or just a chat, I've got your back! 🎮"))
    
    # How to Interact with Me?
    print(center_text("\n💬 HOW TO INTERACT WITH ME? 💬"))
    print(center_text("--------------------------------------------------"))
    print(center_text("1️⃣ Introduce Yourself: Let's get to know each other better!"))
    print(center_text("2️⃣ Ask Questions: Curiosity never killed the catgirl! 🐱"))
    print(center_text("3️⃣ Chat: Share your thoughts; I'm all ears!"))
    
    # My Memory
    print(center_text("\n🧠 MY MEMORY 🧠"))
    print(center_text("--------------------------------------------------"))
    print(center_text("I have a Long-Term Memory system, making our conversations even more personalized and engaging."))
    
    # Guidelines
    print(center_text("\n🎮 GUIDELINES FOR INTERACTING WITH THE MAIN MENU 🎮"))
    print(center_text("--------------------------------------------------"))
    print(center_text("🔹 Navigation: Use arrow keys or type the option number."))
    print(center_text("🔹 Selection: Press 'Enter' to select and proceed."))
    print(center_text("🔹 Back & Exit: 'Back' or 'Exit' options are your friends."))
    print(center_text("🔹 Help: Type 'Help' for this guide."))
    print(center_text("🔹 Feedback: Use the 'Feedback' option to share your thoughts."))
    
    # Signing off with a flair
    print(center_text("\nLet's make your day not just better, but enchanting! 😸"))
    print(center_text("🐾🐾🐾🐾🐾🐾🐾🐾🐾🐾🐾🐾🐾🐾🐾🐾"))

    # Pause the program and wait for the user to press any key to continue
    input(center_text("Press Enter to continue..."))


def settings_menu():
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
    if result["option"] == "Change Text Color":
        Setting.user_text_color = result["new_color"]
    clear_screen()


def main_menu():
    clear_screen()
    option = prompt([
        {
            "type": "list",
            "message": "What would you like to do?",
            "choices": ["Chat", "Settings", "Help", "Exit"],
            "name": "option",
        }
    ])["option"]
    click.echo(click.style(
        f'You chose: {option.capitalize()}', fg=Setting.get_text_color()))
    if option == 'Settings':
        settings_menu()
    elif option == 'Help':
        display_help_menu()  # This line should display the help menu
    return option.capitalize()


