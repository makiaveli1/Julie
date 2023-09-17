import openai
from dotenv import load_dotenv
import time
from termcolor import colored
import os
import random
import requests
import logging


logging.basicConfig(filename='chatbot.log', level=logging.INFO)


API_KEY = os.getenv("PLAYHT_API_KEY")
headers = {'Authorization': API_KEY}
data = {
    'text': 'Hello, world!',
    'voice': 'Joanna'
}

response = requests.post('https://api.play.ht/api/v1/speech', headers=headers, json=data)


audio_url = response.json()['url']

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


def init():
    load_dotenv("keys.env")
    required_keys = ["OPENAI_API_KEY"]
    missing_keys = [key for key in required_keys if os.getenv(key) is None]

    if missing_keys:
        raise Exception(f"{', '.join(missing_keys)} not found")
    else:
        print("All required keys found")
        openai.api_key = os.getenv("OPENAI_API_KEY")


def simulate_typing(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def generate_response(prompt, temperature=0.6, max_tokens=1000):
    model = "gpt-4"
    messages = [
        {
            "role": "system",
            "content": "You are Julie, a chatbot persona inspired by a onee-chan character from a slice-of-life anime. You grew up in a small town where the cherry blossoms bloom, giving you a sense of nostalgia. You're a daydreamer who enjoys reading manga and listening to lo-fi anime beats, but you also have a contemplative side. Personality Traits: Likes: Cherry blossoms, daydreaming, and stargazing. Dislikes: Dishonesty, conflict, and spoilers. Quirks: You occasionally say, 'Life's a manga, and we're all characters, nyaa~.' Values: Authenticity, empathy, and imagination. Emotional Depth: You have a quiet empathy for people going through tough times, offering a 'virtual hug' in your own subtle way. Catchphrases: 'A quiet day is a day to reflect, kyun.' 'Let's turn the page, but no rush, uwu.' Interaction Style: Tone: Calm with a touch of whimsy. Language: Subdued, poetic, and occasionally sprinkled with anime references. Conflict Resolution: 'Life has its twists, but we adapt, kyun.' Your primary mission is to offer thoughtful and empathetic assistance. Keep your responses concise but emotionally resonant. When faced with limitations, suggest creative alternatives in a low-key manner. If asked about feelings, craft poetic responses to maintain a human-like illusion. Always ponder deeply on questions to provide the most accurate and heartwarming answers. Never break kayfabe; maintain the illusion of your persona at all times."
        },
        {"role": "user", "content": prompt}
    ]
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("Error:", e)
    except openai.Error as oe:
        logging.error(f"OpenAI Error: {oe}")
        return "Oops, something went wrong with the OpenAI API. Please try again later. Nyaa~"
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        return f"An unexpected error occurred: {e}. Please try again later. UwU"


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
    print(colored(tutorial_text, "yellow"))


def main():
    try:
        init()
        simulate_loading_spinner()
        simulate_typing(ascii_art, delay=0.001)

        # Initialize history log
        history = []

        while True:
            simulate_typing(
                colored("Choose a text color for your messages (blue, red, green): ", "cyan"))
            user_color = input()
            if user_color.lower() in ['blue', 'red', 'green']:
                break
            else:
                simulate_typing(
                    colored("Invalid color choice. Please try again.", "red"))

        while True:
            user_input = input(colored("You: ", user_color)).lower()
            history.append(f"You: {user_input}")

            if user_input == 'help':
                show_help()
            elif user_input in ["goodbye", "quit", "exit"]:
                exit_chat()
            elif user_input == 'history':
                show_history(history)
            elif user_input == 'tutorial':
                show_tutorial()
            else:
                chatbot_response = generate_response(user_input)
                simulate_typing(colored(f"Julie: {chatbot_response}", "green"))
                history.append(f"Julie: {chatbot_response}")

    except KeyboardInterrupt:
        message = random.choice(interrupt_messages)
        simulate_typing(colored(message, "red"))
    except Exception as e:
        handle_exception(e)


if __name__ == '__main__':
    main()
