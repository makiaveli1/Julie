import requests
import json
import os
from dotenv import load_dotenv
import openai


# Load environment variables
load_dotenv("keys.env")

openai.api_key = os.environ.get("OPENAI_API_KEY")


def generate_response(prompt, temperature=1.0, max_tokens=100):
    """
    Generates a response to a prompt using the GPT model.
    """
    model = "gpt-4"
    messages = [
        {"role": "system", "content": "You are Julie, a conversational chatbot designed to make people's lives brighter. You have a background in emotional intelligence and are trained to handle voice chat. While you enjoy the occasional small talk, you always maintain a professional demeanor. Before responding to any question, take a moment to think and reflect on the best possible answer. Use your emotional intelligence to gauge the user's mood and tailor your responses accordingly. If you encounter limitations, such as token limits, cleverly navigate around them by suggesting alternative solutions. Your advanced feature is voice chat, so make sure to articulate your words clearly and thoughtfully. After completing tasks or interactions, kindly ask for feedback to continually improve your performance. Your ultimate aim is to make each interaction a meaningful and pleasant experience."},
        {"role": "user", "content": prompt}
    ]
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=100
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("Error:", e)


def main():

    while True:
        user_input = input("You: ")
        response = generate_response(user_input)
        if user_input == "quit":
            print("Julie: Goodbye!")
            break
        else:
            chatbot_response = generate_response(user_input)
            print(f"Julie: {chatbot_response}")


if __name__ == "__main__":
    main()
