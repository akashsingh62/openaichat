import streamlit as st
import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv()
token = os.environ.get("AZURE_OPENAI_KEY")

# Azure setup
endpoint = "https://models.github.ai/inference"  # Replace with your endpoint
model = "openai/gpt-4.1"

# Initialize Azure OpenAI client
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(token))

# CSS Styling (like ChatGPT + fixed input bottom)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .chat-container {
        max-height: 78vh;
        overflow-y: auto;
        padding-right: 10px;
    }
    .chat-message {
        border-radius: 10px;
        padding: 10px 15px;
        margin: 10px 0;
        width: fit-content;
        max-width: 80%;
        word-wrap: break-word;
    }
    .user-message {
        background-color: #2f2f2f;
        margin-left: auto;
        text-align: right;
    }
    .assistant-message {
        background-color: #3a3a3a;
        margin-right: auto;
        text-align: left;
    }
    .bottom-form {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 10px;
        background-color: #1e1e1e;
        border-top: 1px solid #444;
        z-index: 999;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
# Sticky header title (fixed at top)
st.markdown(
    """
    <style>
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background-color: #1e1e1e;
        padding: 15px 0;
        text-align: left;
        font-size: 24px;
        font-weight: bold;
        color: white;
        z-index: 1000;
    }

    /* Push content below the fixed header */
    .stApp {
        padding-top: 70px !important;
    }
    </style>

    <div class="fixed-header"> Intellichatbot</div>
    """,
    unsafe_allow_html=True
)


# Session State Init
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Chat container
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for chat in st.session_state["chat_history"]:  # 🚀 Old on top, new at bottom
    st.markdown(
        f"<div class='chat-message user-message'>🧑 {chat['user']}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div class='chat-message assistant-message'>🤖 {chat['ai']}</div>",
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)

# Fixed input form at the bottom
# ⬇️ Fixed bottom form container with Streamlit form inside
st.markdown("<div class='chat-input-container'>", unsafe_allow_html=True)

with st.form("chat-form", clear_on_submit=True):
    user_input = st.text_area("", placeholder="Type your message here...", height=100, label_visibility="collapsed")
    submit = st.form_submit_button("Send")

st.markdown("</div>", unsafe_allow_html=True)





# On submit
if submit and user_input.strip() != "":
    with st.spinner("Thinking..."):
        response = client.complete(
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content=user_input),
            ],
            temperature=1,
            top_p=1,
            model=model,
        )
        reply = response.choices[0].message.content
        st.session_state["chat_history"].append({"user": user_input, "ai": reply})
        st.rerun()
