from utils import Utils
from Memory import BotMemory
import os
from dotenv import load_dotenv
from termcolor import colored
import openai
from utils import Utils
from asciiart import ascii_art


class Initialize:
    def __init__(self):
        self.load_environment()
        self.memory = self.initialize_memory()
        self.check_api_keys()
        self.history = []
        self.username = None
        self.user_id = None
        self.is_new_user = None 
        self.user_color = None
        self.past_data = None
        self.session_data = None
        

        try:
            Utils.simulate_loading_spinner()
            Utils.simulate_typing(ascii_art, delay=0.001)
            
            Utils.simulate_typing(colored("What do I call you, Senpai?: ", "cyan"))
            input_username = input().strip()

            self.username, self.user_id, self.is_new_user = self.memory.check_or_generate_user(input_username)

            if self.username is None or self.user_id is None:
                raise ValueError("Username or User ID is None.")

            self.user_color = self.get_user_color()
            self.past_data, self.session_data = self.memory.handle_user_data(self.username, self.user_id, self.is_new_user)


            print(f"Debug: Is new user? {self.is_new_user}")

        except Exception as e:
            print(f"Unexpected Error: {e}")
        
        

    @staticmethod
    def load_environment():
        load_dotenv("keys.env")

    @staticmethod
    def initialize_memory():
        return BotMemory()

    @staticmethod
    def check_api_keys():
        required_keys = ["OPENAI_API_KEY"]
        missing_keys = [key for key in required_keys if os.getenv(key) is None]
        if missing_keys:
            raise Exception(f"{', '.join(missing_keys)} not found")
        else:
            print("All required keys found")
            openai.api_key = os.getenv("OPENAI_API_KEY")



    @staticmethod
    def get_user_color():
        while True:
            user_color = input(
                "Choose a text color for your messages (blue, red, green): ").lower()
            if user_color in ['blue', 'red', 'green']:
                return user_color
            print("Invalid color choice. Please try again.")

