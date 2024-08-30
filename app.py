# pip install openai, streamlit, dotenv, os

import openai
import os  # Import os for environment variable access
import streamlit as st  # Import Streamlit for web-based GUI
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables from .env file (if using a local environment)
load_dotenv()

# Retrieve the API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Check if the API key is loaded
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

# Set the API key for the OpenAI library
openai.api_key = openai_api_key

# Instantiate the client with the API key
client = openai

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [{
        "role":
        "system",
        "content":
        "You are a helpful but terse AI assistant who gets straight to the point."
    }]


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
        completion = client.chat.completions.create(model="gpt-4o-mini",
                                                    messages=chat_history,
                                                    temperature=0.0)

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
    response = get_llm_response(prompt, st.session_state['chat_history'])
    print(response)


# Streamlit App Configuration
st.title("OpenAI Chatbot")

# Input field for the user
user_input = st.text_input("Your prompt:", "")

# If the user makes an input
if user_input:
    response = get_llm_response(user_input, st.session_state['chat_history'])
    st.write("Response from Chat-Bot:")
    st.write(response)

    # Display the entire chat history
    st.write("Chat History:")
    for message in st.session_state['chat_history']:
        role = "User" if message["role"] == "user" else "Assistant"
        st.write(f"{role}: {message['content']}")
