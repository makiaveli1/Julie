import requests
import json 
import argparse
from dotenv import load_dotenv
load_dotenv("keys.env")
import pinecone
import langchain
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEYS")

def generate_response(prompt):
    """
    Generates a response to a prompt using the GPT-4 model.   
    """
    model_engine = "GPT-4"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=4000
    )
    return response.choices[0].text.script()

