import requests
import json
import argparse
from dotenv import load_dotenv
import pinecone
import langchain
import os
import openai

# Load environment variables
load_dotenv("keys.env")

# Explicitly set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_response(prompt):
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


def test_api():
    prompt = "Is this julie?"
    response = generate_response(prompt)
    print(f"Generated response: {response}")


if __name__ == "__main__":
    test_api()
