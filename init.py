from utils import Utils
from Memory import BotMemory
from termcolor import colored
from dotenv import load_dotenv
import os
import time
import openai
from asciiart import ascii_art


class Initialize:
    def __init__(self):
        self.load_environment()
        self.memory = self.initialize_memory()
        self.check_api_keys()
        self.username, self.user_id, self.is_new_user = self.init()
        self.past_data, self.session_data = self.handle_user_data()
        self.user_color = self.get_user_color()

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


    def init(self):
        try:
            Utils.simulate_loading_spinner()
            Utils.simulate_typing(ascii_art, delay=0.001)

            # Get the username and user_id from generate_unique_id
            username, user_id = self.memory.generate_unique_id(
                self.memory.user_worksheet)

            if username is None or user_id is None:
                raise ValueError("Username or User ID is None.")

            # Pass the username to check_or_generate_user
            username, user_id, is_new_user = self.memory.check_or_generate_user(
                self.memory.user_worksheet, username)

            print(f"Debug: Is new user? {is_new_user}")
            return username, user_id, is_new_user

        except Exception as e:
            print(f"Unexpected Error: {e}")

    def handle_user_data(self):
        past_data = None
        if not self.is_new_user:
            past_data = self.memory.retrieve_user_data(
                self.memory.sh, self.user_id, self.username)
        session_data = self.memory.capture_session_data(None)
        return past_data, session_data

    @staticmethod
    def get_user_color():
        while True:
            user_color = input(
                "Choose a text color for your messages (blue, red, green): ").lower()
            if user_color in ['blue', 'red', 'green']:
                return user_color
            print("Invalid color choice. Please try again.")
