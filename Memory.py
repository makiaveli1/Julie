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

    def generate_unique_id(self, user_worksheet):
        Utils.simulate_typing(colored("What do I call you, Senpai?: ", "cyan"))
        username = input().strip()

        # Validate username length
        min_length = 3
        max_length = 50
        if len(username) < min_length or len(username) > max_length:
            print(
                f"Username should be between {min_length} and {max_length} characters long.")
            return None

        # Generate a unique user ID (UUID)
        user_id = str(uuid.uuid4())

        # Check if the username or user ID already exists
        # Assuming User_ID is the first column
        user_ids = user_worksheet.col_values(1)
        # Assuming Username is the second column
        usernames = user_worksheet.col_values(2)

        if username in usernames or user_id in user_ids:
            print("Username or User ID already exists.")
            return None

        return username, user_id

    # Register user and create new worksheet for them

    def register_user(self, sh, user_id, session_data, username, is_new_user):
        # Add user to 'User' worksheet
        user_worksheet = sh.worksheet('User')

        if is_new_user:
            # Find the next available row
            next_row = len(user_worksheet.get_all_values()) + \
                1  # Assuming the first row contains headers

            # Prepare the row data
            row_data = [
                user_id,
                username,
                session_data.get('user_settings', 'N/A'),
                session_data.get('opt_in_status', 'N/A'),
                session_data.get('start_time', 'N/A'),
                session_data.get('session_id', 'N/A')
            ]

            # Insert the row data into the next available row
            user_worksheet.insert_row(row_data, next_row)

        else:
            # Search for the existing row with the user's ID
            user_ids = user_worksheet.col_values(
                1)  # User_ID is in the first column
            # Adding 1 to adjust for 0-based index
            row_number = user_ids.index(user_id) + 1

            # Update the existing row
            user_worksheet.update_cell(
                row_number, 3, session_data.get('user_settings', 'N/A'))
            user_worksheet.update_cell(
                row_number, 4, session_data.get('opt_in_status', 'N/A'))
            user_worksheet.update_cell(
                row_number, 5, session_data.get('start_time', 'N/A'))
            user_worksheet.update_cell(
                row_number, 6, session_data.get('session_id', 'N/A'))

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

    def retrieve_user_data(self, sh, user_id, username):
        # Validate and format the worksheet name
        worksheet_name = f"{username}_{user_id}".replace("-", "_")

        try:
            # Open the user-specific worksheet
            user_worksheet = sh.worksheet(worksheet_name)

            # Get all records (each record is a dictionary representing a row)
            past_data = user_worksheet.get_all_records()

            # Debug line
            print(
                f"Debug in retrieve_user_data: {type(past_data)}, {past_data}")

            return past_data
        except:
            print("No past data found for this user.")
            return None

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
        # Fill the list with placeholders for the other columns
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

    def check_or_generate_user(self, user_worksheet, username):

        # Skip the header by starting at the second row
        user_ids = user_worksheet.col_values(1)[1:]
        usernames = user_worksheet.col_values(2)[1:]

        print("Debug: User IDs from sheet:", user_ids)
        print("Debug: Usernames from sheet:", usernames)
        print("Debug: Inputted username:", username)

        is_new_user = False
        user_id = None

        if username in usernames:
            # +1 to correct the index because we skipped the header
            username_index = usernames.index(username) + 1
            # +1 because we started at the second row
            user_id = user_worksheet.cell(username_index + 1, 1).value
        else:
            is_new_user = True
            user_id = str(uuid.uuid4())

        print("Debug: Generated or retrieved User ID:", user_id)
        print("Debug: Is new user?", is_new_user)

        return username, user_id, is_new_user

    def analyze_frequent_topics(self, conversation_history, past_data, top_n=3):
        # Extracting user messages from the conversation history
        realtime_text = " ".join(
            [msg['content'] for msg in conversation_history if msg['role'] == 'user'])

        # Extracting user messages from past data
        past_text = " ".join([interaction['User_Message']
                             for interaction in past_data])

        # Combining both sets of texts
        all_text = realtime_text + " " + past_text

        words = re.findall(r'\w+', all_text.lower())
        word_freq = Counter(words)
        most_common_words = [item[0] for item in word_freq.most_common(top_n)]

        return most_common_words
