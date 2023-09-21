from dotenv import load_dotenv
import gspread
import uuid
from datetime import datetime
from collections import Counter
from termcolor import colored
import re


from utils import Utils


class BotMemory:
    def __init__(self):
        load_dotenv()
        self.sh, self.user_worksheet = self.init_gspread()

    def init_gspread(self):
        gc = gspread.service_account(filename='creds.json')
        sh = gc.open('Julie-history')
        try:
            user_worksheet = sh.worksheet('User')
        except:
            user_worksheet = sh.add_worksheet(
                title='User', rows='100', cols='20')
        return sh, user_worksheet


    def generate_unique_id(self):
        user_id = str(uuid.uuid4())
        return user_id

    def check_or_generate_user(self,user_worksheet, input_username):
        min_length = 3
        max_length = 50
        is_new_user = False

        if len(input_username) < min_length or len(input_username) > max_length:
            raise ValueError(
                f"Username should be between {min_length} and {max_length} characters long.")

        existing_usernames = user_worksheet.col_values(2)
        existing_user_ids = user_worksheet.col_values(1)

        if input_username in existing_usernames:
            index = existing_usernames.index(input_username)
            user_id = existing_user_ids[index]
        else:
            user_id = self.generate_unique_id()
            is_new_user = True

        return input_username, user_id, is_new_user

    # Register user and create new worksheet for them

    def register_user(self, sh, user_id, session_data, username, is_new_user):
        # Add user to 'User' worksheet
        user_worksheet = sh.worksheet('User')

        # Provide default values if session_data is None
        if session_data is None:
            session_data = {
                'user_settings': 'N/A',
                'opt_in_status': 'N/A',
                'start_time': 'N/A',
                'session_id': 'N/A'
            }

        if is_new_user:
            # Find the next available row
            next_row = len(user_worksheet.get_all_values()) + \
                1  # Assuming the first row contains headers

            # Prepare the row data
            row_data = [
                user_id,
                username,
                session_data['user_settings'],
                session_data['opt_in_status'],
                session_data['start_time'],
                session_data['session_id']
            ]

            # Insert the row data into the next available row
            user_worksheet.insert_row(row_data, next_row)

        else:
            # Search for the existing row with the user's ID
            user_ids = user_worksheet.col_values(1)
            row_number = user_ids.index(user_id) + 1

            # Update the existing row
            user_worksheet.update_cell(
                row_number, 3, session_data['user_settings'])
            user_worksheet.update_cell(
                row_number, 4, session_data['opt_in_status'])
            user_worksheet.update_cell(
                row_number, 5, session_data['start_time'])
            user_worksheet.update_cell(
                row_number, 6, session_data['session_id'])

    # Create a new worksheet for a user
    def create_user_worksheet(self, sh, user_id, username):
        # Validate and format the worksheet name
        worksheet_name = f"{username}_{user_id}".replace("-", "_")

        # Create a new worksheet
        new_worksheet = sh.add_worksheet(
            title=worksheet_name, rows="100", cols="20")

        # Define columns
        columns = ['User_Message', 'Bot_Response', 'Timestamp',
                   'User_Feedback', 'Session_Duration', 'Frequently_Used_Commands',
                   'User_Preference', 'Sentiment_Score']

        # Add columns to the new worksheet
        new_worksheet.append_row(columns)

        return new_worksheet

    def retrieve_user_data(self, sh, user_id, memory, username):
        # Validate and format the worksheet name
        worksheet_name = f"{username}_{user_id}".replace("-", "_")
        print(f"Debug: Worksheet name: {worksheet_name}")
        print("Debug: Type of sh:", type(memory.sh))  # Debugging sh
        print("Debug: sh attributes:", dir(memory.sh))  # Debugging sh

        print("Debug: Type of memory:", type(memory))  # Debugging memory
        print("Debug: memory attributes:", dir(memory))  # Debugging memory

        try:
            # Open the user-specific worksheet
            user_worksheet = sh.worksheet(worksheet_name)

            # Get all records (each record is a dictionary representing a row)
            past_data = user_worksheet.get_all_records()

            # Debug line
            print(
                f"Debug in retrieve_user_data: {type(past_data)}, {past_data}")

            # Return the data if found
            return past_data if past_data else {}
        except Exception as e:
            print(f"No past data found for this user. Error: {e}")
            return {}

    # Reading a cell (A1 notation)

    def read_cell(self, worksheet, cell_name):
        return worksheet.acell(cell_name).value

    # Writing to a cell (A1 notation)

    def write_cell(self, worksheet, cell_name, value):
        worksheet.update(cell_name, value)

    # Appending a row

    def append_row(self, worksheet, row_values):
        worksheet.append_row(row_values)

        # Log interactions between user and chatbot

    def log_interaction(self, new_worksheet, user_message, bot_response):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        interaction_data = [user_message, bot_response,
                            current_time, '', '', '', '', '']
        self.append_row(new_worksheet, interaction_data)

    def capture_session_data(self, user_settings):
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
        realtime_text = " ".join(
            [msg['content'] for msg in conversation_history if msg['role'] == 'user'])

        past_text = " ".join([interaction['User_Message']
                             for interaction in past_data])

        all_text = realtime_text + " " + past_text

        words = re.findall(r'\w+', all_text.lower())
        word_freq = Counter(words)
        most_common_words = [item[0] for item in word_freq.most_common(top_n)]

        return most_common_words
