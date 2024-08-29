# Installiere die benötigten Bibliotheken
# pip install openai
# pip install python-dotenv

from dotenv import load_dotenv
import os

load_dotenv()  # Lädt die Variablen aus der .env Datei

# Zugriff auf die API-Schlüsselvariable
openai_api_key = os.getenv('OPENAI_API_KEY')

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Instantiate the client with the API key
client = OpenAI(api_key=openai_api_key)

# Define global chat history list
chat_history = [
    {"role": "system", "content": "You are a helpful but terse AI assistant who gets straight to the point."}
]

def get_llm_response(prompt, chat_history):
    """
    This function takes a prompt as input, adds it to the chat history, and passes the updated history
    to OpenAI's GPT-3.5 model. The function returns the response from the model and updates the chat history.
    """
    try:
        if not isinstance(prompt, str):
            raise ValueError("Input must be a string enclosed in quotes.")

        # Append the user prompt to the chat history
        chat_history.append({"role": "user", "content": prompt})

        # Correct API call using the OpenAI Python library
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            temperature=0.0
        )
        
        # Get the response from the model
        response = completion.choices[0].message.content
        
        # Append the assistant's response to the chat history
        chat_history.append({"role": "assistant", "content": response})
        
        return response

    except Exception as e:
        return f"Error: {str(e)}"

def print_llm_response(prompt):
    """
    This function takes a prompt as input, calls the get_llm_response function, and prints the response.
    It also updates the chat history with each new interaction.
    """
    response = get_llm_response(prompt, chat_history)
    print(response)

# Example usage
print_llm_response("What is the capital of France?")
