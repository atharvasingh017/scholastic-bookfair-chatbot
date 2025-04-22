
import streamlit as st
import os
import requests

st.set_page_config(page_title="📚 Book Fair Chatbot", layout="centered")
st.title("📚 Book Fair Chatbot")
st.write("Ask me anything about the event, books, schedule, or payments!")

# Load event info
with open("bookfair.txt", "r", encoding="utf-8") as f:
    book_data = f.read()

# OpenRouter API (Free access to open-source models)
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]  # stored securely

def ask_bot(question):
    prompt = f"""
You are a friendly assistant at a school Book Fair. Based on the following information, answer the user's question clearly and politely.

Book Fair Info:
{book_data}

User: {question}
Assistant:
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",  # free model on OpenRouter
        "messages": [{
            "role": "user",
            "content": prompt
        }]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                             json=payload,
                             headers=headers)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Sorry, something went wrong. 😢"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat UI
user_input = st.text_input("You:", key="user_input")

if user_input:
    # Add user message
    st.session_state.messages.append(("You", user_input))
    
    # Get bot response
    with st.spinner("Bot is thinking..."):
        bot_response = ask_bot(user_input)
        st.session_state.messages.append(("Bot", bot_response))

# Display chat history
for role, message in st.session_state.messages:
    if role == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Bot:** {message}")
