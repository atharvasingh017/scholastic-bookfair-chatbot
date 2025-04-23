import streamlit as st
import os
import requests

# Configure Streamlit page settings
st.set_page_config(page_title="📚 SCHOLASTIC FAIR Agent",
                   layout="wide",
                   initial_sidebar_state="collapsed",
                   menu_items={
                       'Get Help': None,
                       'Report a bug': None,
                       'About': None
                   })

# Hide streamlit default elements
st.markdown("""
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    footer {display: none;}
</style>
""",
            unsafe_allow_html=True)

# Custom CSS for chat interface
st.markdown("""
<style>
.main-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background-color: #1a1a1a;
    padding: 1rem;
    z-index: 1000;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #2f2f2f;
}
.main-header h1 {
    margin: 0;
    font-size: 1.2rem;
    color: white;
}
.book-icon {
    margin-right: 10px;
    font-size: 1.5rem;
}
.user-message {
    padding: 15px;
    border-radius: 15px;
    background-color: #1e1e1e;
    margin: 10px 0;
    text-align: left;
    margin-left: 20%;
    display: block;
    float: right;
    clear: both;
    border: 1px solid #2f2f2f;
    max-width: 80%;
    word-wrap: break-word;
}
.bot-message {
    padding: 15px;
    border-radius: 15px;
    background-color: #1a1a1a;
    margin: 10px 0;
    text-align: left;
    margin-right: 20%;
    display: block;
    float: left;
    clear: both;
    border: 1px solid #2f2f2f;
    max-width: 80%;
    word-wrap: break-word;
}
.chat-input {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 20px;
    background-color: #0e1117;
    z-index: 999;
    border-top: 1px solid #2f2f2f;
}
.creator-info {
    position: fixed;
    bottom: 100px;
    right: 20px;
    color: #666;
    font-size: 12px;
    z-index: 998;
}
div[data-testid="stForm"] {
    margin: 0 !important;
    padding: 0 !important;
    background: transparent !important;
}
.user-message {
    animation: fadeIn 0.3s ease;
}
.bot-message {
    animation: fadeIn 0.3s ease;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
div.stButton > button {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    height: 41px;
    margin-top: 0;
    width: 100%;
}
.stTextInput > div > div > input {
    border-radius: 8px;
    width: 100%;
    min-width: 200px;
    background-color: #1e1e1e;
    border: 1px solid #2f2f2f;
    padding: 12px;
    color: white;
}
div[data-testid="stForm"] {
    background-color: transparent;
    border: none;
    padding: 0;
    margin-bottom: 80px;
}
div[data-testid="stVerticalBlock"] {
    gap: 0 !important;
    padding: 0 20px;
}
</style>
""",
            unsafe_allow_html=True)

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
            timeout=30)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "Sorry, something went wrong. 😢"
    except Exception as e:
        return f"Error: {str(e)}"


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display header
st.markdown("""
<div class="main-header">
    <span class="book-icon">📚</span>
    <h1>SCHOLASTIC FAIR Agent</h1>
</div>
""",
            unsafe_allow_html=True)

# Add spacing for header
st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        role, content = message
        if role == "user":
            st.markdown(f'<div class="user-message">{content}</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{content}</div>',
                        unsafe_allow_html=True)

# Creator info
st.markdown('<div class="creator-info">Created by Atharva Singh</div>',
            unsafe_allow_html=True)

# Add spacing for chat messages
st.markdown("<div style='margin-bottom: 100px;'></div>", unsafe_allow_html=True)

# Chat input at bottom
with st.container():
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            user_input = st.text_input(
                "",
                key="user_input",
                placeholder="Ask anything about the Book Fair...",
                label_visibility="collapsed")
        with col2:
            submit_button = st.form_submit_button("Send")

        if submit_button and user_input:
            st.session_state.messages.append(("user", user_input))
            with st.spinner("Thinking..."):
                bot_response = ask_bot(user_input)
                st.session_state.messages.append(("bot", bot_response))
            st.rerun()
