import json
import uuid
from datetime import datetime
from collections import Counter
from termcolor import colored
import re


from utils import Utils
import logging
logging.basicConfig(level=logging.DEBUG)


class BotMemory:
    """
    This class is responsible for managing the bot's memory.
    It includes methods for loading, saving, and manipulating user data.
    """
    def __init__(self):
        """
        Initialize the BotMemory class.
        Load user data from file during initialization.
        """
        self.user_data = self.load_user_data()

    def load_user_data(self):
        """
        Load user data from a JSON file.
        Return an empty dictionary if file not found.
        """
        try:
            with open('user_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_user_data(self):
        """
        Save user data to a JSON file.
        """
        with open('user_data.json', 'w') as f:
            json.dump(self.user_data, f)

    def generate_unique_id(self):
        """
        Generate a unique user ID.
        """
        user_id = str(uuid.uuid4())
        return user_id

    def check_or_generate_user(self, input_username):
        """
        Check if a user exists, if not, generate a new user.
        """
        min_length = 3
        max_length = 50
        is_new_user = False

        if len(input_username) < min_length or len(input_username) > max_length:
            raise ValueError(
                f"Username should be between {min_length} and {max_length} characters long.")

        existing_usernames = list(self.user_data.keys())

        if input_username in existing_usernames:
            user_id = self.user_data[input_username]['user_id']
        else:
            user_id = self.generate_unique_id()
            is_new_user = True

        return input_username, user_id, is_new_user

    def register_user(self, user_id, session_data, username, is_new_user):
        """
        Register a new user or update an existing user's session data.
        """
        if session_data is None:
            session_data = {
                'user_settings': 'N/A',
                'opt_in_status': 'N/A',
                'start_time': 'N/A',
                'session_id': 'N/A'
            }

        if is_new_user:
            user_data = {
                'user_id': user_id,
                'username': username,
                'session_data': session_data
            }
            self.user_data[username] = user_data

        else:
            self.user_data[username]['session_data'] = session_data

        self.save_user_data()

    def retrieve_user_data(self, user_id, username):
        """
        Retrieve user data.
        Return an empty dictionary if user not found.
        """
        try:
            user_data = self.user_data[username]
            return user_data if user_data else {}
        except KeyError:
            logging.error(f"No past data found for this user.")
            return {}
        
        
    def handle_user_data(self, username, user_id, is_new_user):
        """
        Handle user data.
        Retrieve past data if user exists, capture new session data.
        """
        past_data = None
        session_data = None
        try:
            if username and user_id:
                if not is_new_user:
                    past_data = self.retrieve_user_data(user_id, username)
            
            session_data = self.capture_session_data(None)
        except ValueError as ve:
            logging.error(f"ValueError in handle_user_data: {ve}")
        except Exception as e:
            logging.error(f"Unexpected error in handle_user_data: {e}")

        return past_data, session_data

    def capture_session_data(self, user_settings):
        """
        Capture session data.
        Ask user if they want to remember the chat.
        """
        Utils.simulate_typing(colored(
            "Would you like me to remember our chat? (yes/no): ", "cyan"))
        opt_status = input().strip().lower()
        session_data = {
            'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_settings': user_settings,
            'opt_in_status': opt_status == 'yes',
            'session_id': str(uuid.uuid4())
        }
        if session_data['opt_in_status']:
            Utils.simulate_typing(colored(
                "Your chat history will be logged.", "green"))
        else:
            Utils.simulate_typing(colored(
                "Your chat history will not be logged.", "green"))
        return session_data

    def analyze_frequent_topics(self, conversation_history, past_data, top_n=3):
        """
        Analyze frequent topics from conversation history and past data.
        """
        realtime_text = " ".join(
            [msg['content'] for msg in conversation_history if msg['role'] == 'user'])

        past_text = " ".join([interaction['User_Message']
                             for interaction in past_data])

        all_text = realtime_text + " " + past_text

        words = re.findall(r'\w+', all_text.lower())
        word_freq = Counter(words)
        most_common_words = [item[0] for item in word_freq.most_common(top_n)]

        return most_common_words

