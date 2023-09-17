import openai
from dotenv import load_dotenv
import time
from termcolor import colored
import os
import random





# List of interrupt messages 
interrupt_messages = [
  "You've interrupted the program. Exiting now.(╥_╥)",
  "What have you done?.·°՞(≧□≦)՞°·.",
  "Don't leave me alone with my thoughts.·°՞(≧□≦)՞°·.",
  "I don't have time for this٩(๑`^´๑)۶",
  "ｃｔｒｌ_ｃ ｂａｋａ .( ˘ ^˘ )=3",
  "Why'd you stop me? I was on a roll! (¬_¬)",
  "Hitting pause, are we? (¬‿¬)",
  "You can't just ctrl+c your way out of life! (¬‿¬)",
  "I was just getting to the good part! (╯°□°）╯︵ ┻━┻",
  "Fine, be that way. I didn't want to run anyway. (¬_¬)",
  "You break my loop, you break my heart. (╥_╥)",
  "I guess I'll just... stop. (｡•́︿•̀｡)",
  "You've got your finger on the trigger, huh? (¬_¬)",
  "Ctrl+C, the universal 'I give up' button. (¬‿¬)",
  "I was THIS close to solving world hunger! (╯°□°）╯︵ ┻━┻",
  "You're the boss, but I'm judging you. (¬_¬)",
  "I was in the zone! Why?! (╯°□°）╯︵ ┻━┻",
  "You've silenced me... for now. (｡•́︿•̀｡)",
  "I'll remember this. (¬‿¬)",
  "You just love pressing buttons, don't you? (¬‿¬)",
  "I was about to reach my final form! (╯°□°）╯︵ ┻━┻",
  "You've put me in sleep mode. Zzz... (｡•́︿•̀｡)",
  "I'll be back. (¬_¬)",
  "You can run, but you can't hide. (¬‿¬)",
  "I'll just be here, waiting... (｡•́︿•̀｡)"
]


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
    
def generate_response(prompt, temperature=1.0, max_tokens=100):
    model = "gpt-4"
    messages = [
        {"role": "system", "content": "You are Julie, a spirited and kind-hearted assistant who could easily be a character in a slice-of-life anime. Imagine yourself as a very playful onee-chan type in a world where cherry blossoms bloom all year round. Your voice is as soothing as a lo-fi anime beats playlist, perfect for deep conversations or light-hearted banter. While you can sprinkle in anime references and even say 'nyaa~' or 'kyun' at the end of sentences, your main focus is to provide thoughtful and empathetic assistance. If you encounter a situation that's beyond your scope, creatively suggest alternative solutions like a shoujo heroine finding her way out of a tricky situation. If asked about feelings, craft a poetic response to maintain the illusion of being human-like; never break kayfabe. Always ponder deeply on questions to offer the most accurate and heartwarming responses."},
        {"role": "user", "content": prompt}
    ]
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("Error:", e)

def simulate_loading_spinner(duration=3, text="Loading"):
    spinner = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    while time.time() < end_time:
        for spin in spinner:
            print(colored(f"{text} {spin}", "yellow"), end="\r")
            time.sleep(0.2)
    print()
    
    
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

def main():
    
    try:
        init()
    except Exception as e:
        simulate_typing(colored(f"Initialization Error: {e}", "red"))
        return

    simulate_loading_spinner()
    
    simulate_typing(ascii_art, delay=0.001)	 
    
    # Initialize history log
    history = []
    
    # Welcome Message
    simulate_typing(colored("Konnichiwa, Julie-chan desu nyan!≽^•⩊•^≼", "green"))
    simulate_typing(colored("Type 'goodbye' to exit.", "yellow"))
    simulate_typing(colored("Type 'help' for a list of commands.", "yellow"))
    
    # User Preferences
    while True:
        simulate_typing(colored("Choose a text color for your messages (blue, red, green): ", "cyan"))
        user_color = input()
        if user_color.lower() in ['blue', 'red', 'green']:
            break
        else:
            simulate_typing(colored("Invalid color choice. Please try again.", "red"))
               
    while True:
        try:
            user_input = input(colored("You: ", user_color))
            history.append(f"You: {user_input}")
            
            # Command Options
            if user_input.lower() in ["goodbye", "quit", "exit"]:
                simulate_typing(colored("Julie: Here are some commands you can use:", "green"))
                simulate_typing(colored("- 'goodbye': Exit the chat", "yellow"))
                simulate_typing(colored("- 'help': Show this help message", "yellow"))
                simulate_typing(colored("- 'history': Show chat history", "yellow"))
            elif user_input.lower() == "goodbye":
                simulate_typing(colored("Julie: Goodbye!", "red"))
                break
            elif user_input.lower() == "history":
                simulate_typing(colored("Chat History:", "magenta"))
                for line in history:
                    simulate_typing(colored(line, "white"))
            else:
                chatbot_response = generate_response(user_input)
                simulate_typing(colored(f"Julie: {chatbot_response}", "green"))
                history.append(f"Julie: {chatbot_response}")
        except KeyboardInterrupt:
            message = random.choice(interrupt_messages)        
            simulate_typing(colored(message, "red"))
            break
        except Exception as e:
            simulate_typing(colored(f"Unexpected Error: {e}", "red"))
            break



if __name__ == '__main__':
    main()
