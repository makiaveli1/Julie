import click
import os
from InquirerPy import prompt
from files.setup import Setting


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def onboarding_experience():
    clear_screen()
    click.echo(click.style("Welcome to Julie's World!",
               fg=Setting.get_text_color(), bold=True))
    click.echo(click.style("Here's a quick tutorial:",
               fg=Setting.get_text_color()))
    click.echo(click.style(
        "1. Type 'Chat' to start a conversation with Julie.", fg=Setting.get_text_color()))
    click.echo(click.style(
        "2. Type 'Settings' to adjust your preferences.", fg=Setting.get_text_color()))
    click.echo(click.style("3. Type 'Exit' to leave the chat.",
               fg=Setting.get_text_color()))
    click.echo(click.style("Enjoy your time with Julie!",
               fg=Setting.get_text_color(), bold=True))


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
            "choices": ["Chat", "Settings", "Exit"],
            "name": "option",
        }
    ])["option"]
    click.echo(click.style(
        f'You chose: {option.capitalize()}', fg=Setting.get_text_color()))
    if option == 'Settings':
        settings_menu()
    return option.capitalize()
