import requests
import json
import os
from dotenv import load_dotenv
from langchain import LLMChain
from langchain.vectorstores.weaviate import Weaviate
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain
from langchain.chat_models import ChatOpenAI
import weaviate
import openai
import sys
print(sys.path)


# Load environment variables
load_dotenv("keys.env")

langchain_instance = LLMChain(prompt={"your_key": "your_value"}, llm={"your_key": "your_value"}),

# Validate environment variables
if not os.environ.get("OPENAI_API_KEY") or not os.environ.get("WEAVIATE_API_KEY"):
    raise EnvironmentError("Missing environment variables.")

# Initialize Weaviate client
auth_config = weaviate.AuthApiKey(api_key=os.environ.get("WEAVIATE_API_KEY"))
client = weaviate.Client(
    url="https://julie-cluster-jwm0y3lz.weaviate.network",
    auth_client_secret=auth_config
)


llm = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
chat_model = ChatOpenAI()
vectorstore = Weaviate(client, "PodClip", "content")
qa = ChatVectorDBChain.from_llm(OpenAI, vectorstore)


# Function to create schema


def create_schema(client, schema):
    try:
        client.schema.create(schema)
    except Exception as e:
        print(f"Failed to create schema: {e}")


# Check if VectorData class exists
existing_schema = client.schema.get()
if 'VectorData' not in [x['class'] for x in existing_schema['classes']]:
    vector_schema = {
        "classes": [
            {
                "class": "VectorData",
                "properties": [
                    # Changed from "float"
                    {"name": "vector", "dataType": ["number[]"]}
                ]
            }
        ]
    }
    create_schema(client, vector_schema)
else:
    print("Class VectorData already exists!")

# Delete and create JulieChatInteraction class
client.schema.delete_class("JulieChatInteraction")

vector_schema = {
    "classes": [
        {
            "class": "VectorData",
            "properties": [
                {"name": "vector", "dataType": ["float"]}
            ]
        }
    ],
    'vectorizer': 'text2vec-openai'
}

schema = {
    "classes": [
        {
            "class": "JulieChatInteraction",
            "properties": [
                {"name": "text", "dataType": ["string"]},
                {"name": "mood", "dataType": ["string"]},
                {"name": "feedback", "dataType": ["string"]},
                {"name": "vector", "dataType": ["VectorData"]},
                {"name": "clientAge", "dataType": ["int"]},
                {"name": "clientInfo", "dataType": ["string"]},
                {"name": "importantNotes", "dataType": ["string"]},
                {"name": "sessionID", "dataType": ["string"]},
                {"name": "timestamp", "dataType": ["string"]},
                {"name": "userAgent", "dataType": ["string"]},
                {"name": "interactionType", "dataType": ["string"]},
                {"name": "language", "dataType": ["string"]},
                {"name": "location", "dataType": ["string"]},
                {"name": "responseTime", "dataType": ["int"]},
                {"name": "userSentiment", "dataType": ["string"]},
                {"name": "customTags", "dataType": ["string"]},
                {"name": "privacyConsent", "dataType": ["boolean"]}
            ]
        }
    ]
}


client.schema.delete_class("JulieChatInteraction")
client.schema.create(schema)


# Create VectorData object
vector_data = {"vector": [0.1, 0.2, 0.3]}
vector_id = client.data_object.create(vector_data, "VectorData")


chat_data = {
    "text": "How are you?",
    "mood": "Neutral",
    "feedback": "None",
    "vector": [vector_id],
    "clientAge": 30,
    "clientInfo": "Prefers text over voice",
    "importantNotes": "Allergic to peanuts",
    "sessionID": "XYZ123",
    "timestamp": "2023-09-14T12:34:56Z",
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/237.84.2.178 Safari/537.36",
    "interactionType": "Chat",
    "language": "English",
    "location": "United States",
    "responseTime": 0,
    "userSentiment": "Neutral",
    "customTags": "None",
    "privacyConsent": True
}
client.data_object.create(chat_data, "JulieChatInteraction")


query = {
    "query": {
        "type": "JulieChatInteraction",
        "properties": [
            "text", "mood", "feedback", "vector", "clientAge", "clientInfo",
            "importantNotes", "sessionID", "timestamp", "userAgent", "interactionType", "language", "location", "responseTime", "userSentiment", "customTags", "privacyConsent"
        ]
    }
}
result = client.data_object.query(query)


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
