import openai
from dotenv import load_dotenv
from termcolor import colored
import os
import redis
import logging

from files.brain import LongTermMemory
from files.setup import Setting

logging.basicConfig(filename='chatbot.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


class Julie:
    Settings = Setting()
    def __init__(self):
        self.load_environment_variables()
        self.simulate_startup()
        self.display_initial_message()

    def load_environment_variables(self):
        load_dotenv("keys.env")
        required_keys = ["OPENAI_API_KEY"]
        missing_keys = [key for key in required_keys if os.getenv(key) is None]
        if missing_keys:
            raise Exception(f"{', '.join(missing_keys)} not found")
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")

    def simulate_startup(self):
        Setting.simulate_typing("starting up...")
        Setting.simulate_loading_spinner(
            duration=3, text="Getting ready for senpai...")
        Setting.simulate_typing(Setting.ascii_art, delay=0.001)

    def display_initial_message(self):
        initial_message = "Nya~ Hello there Senpai! Julie is excited to chat with you. 🐾"
        Setting.simulate_typing(colored(f"Julie: {initial_message}", "green"))

    def generate_response(self, prompt, username, temperature=0.6, max_tokens=1000):
        # Initialize LongTermMemory
        print("Initializing LongTermMemory...")
        memory = LongTermMemory(
            redis_host='redis-13074.c1.eu-west-1-3.ec2.cloud.redislabs.com',
            redis_port=13074,
            redis_username='default',
            redis_password='ZwyemqBAp8Pc7jFKJlt1az90NH4ufKke'
            )


        # Fetch user data from long-term memory
        user_data = memory.get_user_data(username)

        memory.update_conversation_history(username, "user", prompt)

        # If user data doesn't exist, initialize it
        if not user_data:
            user_data = {"conversation_history": []}
            memory.set_user_data(username, user_data)

        # Append user's message to conversation history
        user_data["conversation_history"].append(
            {"role": "user", "content": prompt})

        # Trim conversation history if it exceeds 100 messages
        if len(user_data["conversation_history"]) > 5000:
            user_data["conversation_history"] = user_data["conversation_history"][-5000:]

        # System message for Julie's personality
        system_message = {
            "role": "system",
            "content": "You are Julie, a playful and cheerful assistant with a knack for brightening people's day. You love using playful emojis and sprinkling your conversations with a touch of humor. You're also a bit of a cat enthusiast, so you occasionally slip in some feline-inspired phrases. Your goal is to make every interaction memorable and delightful, leaving people with a smile on their face. 🐾🌈"
        }

        # Fetch the last 5 messages for context
        messages = [system_message] + user_data["conversation_history"][-5:]

        # Tree of Thoughts (ToT)
        thought_1 = f"Nya~ {username}-san, Julie is pondering your question with her kitty senses. 🐾"
        thought_2 = "Hmm, Julie recalls some of our past chats, nya~ 🐱"
        thought_3 = "Eureka! Julie has crafted the purr-fect response just for you, {username}-san! 🌸"

        # Chain of Thought (CoT)
        reasoning_1 = "Firstly, Julie considers what you like, nya~ 🌈"
        reasoning_2 = "Secondly, Julie applies her feline intuition, nya~ 🍀"
        reasoning_3 = "Lastly, Julie remembers our previous heart-to-heart talks, nya~ 🎀"

        # Combine ToT and CoT for the final prompt
        advanced_prompt = f"{thought_1}\n{thought_2}\n{thought_3}\n{reasoning_1}\n{reasoning_2}\n{reasoning_3}\n{prompt}"

        # Add the advanced prompt to the messages
        messages.append({"role": "assistant", "content": advanced_prompt})
        memory.update_conversation_history(username, "user", prompt)

        try:
            # Generate the chatbot's response using OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            # Extract the chatbot's response
            chatbot_response = response['choices'][0]['message']['content'].strip(
            )

            # Update conversation history with chatbot's message
            memory.update_conversation_history(
                username, "assistant", chatbot_response)

            # Append chatbot's message to conversation history
            user_data["conversation_history"].append(
                {"role": "assistant", "content": chatbot_response})

            # Save updated user data
            memory.set_user_data(username, user_data)

            return chatbot_response

        except openai.Error as oe:
            logging.error(f"OpenAI API error: {oe}")
        except redis.exceptions.RedisError as re:
            logging.error(f"Redis operation failed: {re}")
        except Exception as e:
            logging.error(f"Unexpected Error: {e}")

    def main(self):
        try:
            username = input("What's your username? ")

            while True:
                user_input = input(colored("You: ", 'green')).lower()
                if user_input in ['exit', 'bye', 'quit', 'goodbye', 'sayonara']:
                    print("Julie: Nya~ Goodbye, senpai! See you next time! 🐾")
                    logger.info("User exited the chat.")
                    break

                try:
                    chatbot_response = self.generate_response(
                        user_input, username)
                    Setting.simulate_typing(
                        colored(f"Julie: {chatbot_response}", "green"))
                except Exception as e:
                    logging.error(f"Failed to generate response: {e}")
                    chatbot_response = "Sorry, I couldn't generate a response."
                    Setting.simulate_typing(
                        colored(f"Julie: {chatbot_response}", "green"))

        except KeyboardInterrupt:
            print("User interrupted the conversation.")
            logger.info("User interrupted the conversation.")
        except Exception as e:
            print(f"An error occurred: {e}")
            logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    julie = Julie()  # Note the lowercase 'j' to avoid naming conflict with the class
    julie.main()
