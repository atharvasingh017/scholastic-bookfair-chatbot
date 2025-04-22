
import streamlit as st
import os
import requests

# Configure Streamlit page settings
st.set_page_config(
    page_title="📚 SCHOLASTIC FAIR Agent",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for chat interface
st.markdown("""
<style>
.user-message {
    padding: 10px;
    border-radius: 15px;
    background-color: #2b313e;
    margin: 5px 0;
    text-align: right;
    margin-left: 20%;
    display: inline-block;
    float: right;
    clear: both;
}
.bot-message {
    padding: 10px;
    border-radius: 15px;
    background-color: #1f2937;
    margin: 5px 0;
    text-align: left;
    margin-right: 20%;
    display: inline-block;
    float: left;
    clear: both;
}
.chat-input {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 20px;
    background-color: #0e1117;
    z-index: 999;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
}
.creator-info {
    position: fixed;
    bottom: 80px;
    right: 20px;
    color: #666;
    font-size: 12px;
    z-index: 998;
}
div.stButton > button {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 10px 20px;
}
.stTextInput > div > div > input {
    border-radius: 20px;
    width: auto;
    min-width: 200px;
}
</style>
""", unsafe_allow_html=True)

# Load event info
with open("bookfair.txt", "r", encoding="utf-8") as f:
    book_data = f.read()

# OpenRouter API setup
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

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
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{
            "role": "user",
            "content": prompt
        }]
    }
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "Sorry, something went wrong. 😢"
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
st.title("📚 SCHOLASTIC FAIR Agent")
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        role, content = message
        if role == "user":
            st.markdown(f'<div class="user-message">{content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{content}</div>', unsafe_allow_html=True)

# Creator info
st.markdown('<div class="creator-info">Created by Atharva Singh</div>', unsafe_allow_html=True)

# Chat input at bottom
with st.container():
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4,1])
        with col1:
            user_input = st.text_input("Ask me anything about the Book Fair!", key="user_input")
        with col2:
            submit_button = st.form_submit_button("Send")
        
        if submit_button and user_input:
            st.session_state.messages.append(("user", user_input))
            with st.spinner("Thinking..."):
                bot_response = ask_bot(user_input)
                st.session_state.messages.append(("bot", bot_response))
            st.rerun()
