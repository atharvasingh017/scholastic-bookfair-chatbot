import streamlit as st
from chat_bot import ChatBot

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

# Load CSS
with open("styles.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Hide streamlit default elements
st.markdown("""
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    footer {display: none;}
    div[data-testid="stForm"] {
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
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
""", unsafe_allow_html=True)

# Initialize chat bot and session state
bot = ChatBot()
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display header
st.markdown("""
<div class="main-header">
    <h1>
        <img src="https://img.icons8.com/color/48/000000/book.png" class="book-icon">
        SCHOLASTIC FAIR Agent
    </h1>
    <a href="?" class="new-chat-button">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        New chat
    </a>
</div>
""", unsafe_allow_html=True)

# Add spacing for header
st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        role, content = message
        if role == "user":
            st.markdown(f'<div class="user-message">{content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'''
                <div class="bot-message">
                    {content}
                    <div class="message-actions">
                        <button class="action-button" title="Copy">📋</button>
                        <button class="action-button" title="Regenerate">🔄</button>
                        <button class="action-button" title="Like">👍</button>
                        <button class="action-button" title="Dislike">👎</button>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

# Creator info
st.markdown('<div class="creator-info">Created by Atharva Singh</div>', unsafe_allow_html=True)

# Add spacing for chat messages
st.markdown("<div style='margin-bottom: 100px;'></div>", unsafe_allow_html=True)

# Chat input
with st.container():
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            user_input = st.text_input(
                "Message",
                key="user_input",
                placeholder="Ask anything about the Book Fair...",
                label_visibility="collapsed")
        with col2:
            submit_button = st.form_submit_button("Send")

        if submit_button and user_input:
            st.session_state.messages.append(("user", user_input))
            with st.spinner("Thinking..."):
                bot_response = bot.ask(user_input)
                st.session_state.messages.append(("bot", bot_response))
            st.rerun()