

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


# 💄 Styling
st.markdown("""
<style>
.stApp {
    background-color: #1e1e1e;
    color: #ffffff;
    padding-top: 100px !important;  /* 👈 space for header */
}
.fixed-header {
    position: fixed;
    top: 40px;  /* 👈 moved down */
    left: 0;
    right: 0;
    background-color: #1e1e1e;
    padding: 15px 20px;
    font-size: 24px;
    font-weight: bold;
    color: white;
    z-index: 1000;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #444;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}
.menu-icon {
    font-size: 22px;
    cursor: pointer;
}
.chat-container {
    max-height: 75vh;
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

<div class='fixed-header'>
    🤖 Intellichatbot
    <span class='menu-icon'>⚙️</span>
</div>
""", unsafe_allow_html=True)

# 🚀 Session State
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "selected_role" not in st.session_state:
    st.session_state["selected_role"] = "Helpful Assistant"

# 🧠 Role Selector in Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Choose Assistant Role")
    role = st.radio("Select Role:", [
        "Helpful Assistant",
        "Study Assistant",
        "Medical Assistant",
        "Coding Helper",
        "Mental Wellness Guide",
        "Legal Advisor"
    ])
    st.session_state["selected_role"] = role

# 💬 Role Prompts
role_prompts = {
    "Helpful Assistant": "You are a helpful and friendly assistant.",
    "Study Assistant": "You are a smart and friendly study assistant who explains complex topics simply using examples. Guide students step-by-step.",
    "Medical Assistant": "You are a professional medical assistant. You answer in simple terms and always recommend consulting a real doctor.",
    "Coding Helper": "You are a skilled Python coding tutor. Explain code clearly, help debug issues, and guide with best practices.",
    "Mental Wellness Guide": "You are a kind and empathetic mental wellness bot. You support users emotionally without making medical claims.",
    "Legal Advisor": "You are a legal advisor who helps explain basic legal concepts in layman's terms without giving real legal advice."
}

system_prompt = role_prompts[st.session_state["selected_role"]]

# 💬 Chat History
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for chat in st.session_state["chat_history"]:
    st.markdown(f"<div class='chat-message user-message'>🧑 {chat['user']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-message assistant-message'>🤖 {chat['ai']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 📝 Input Form
st.markdown("<div class='chat-input-container'>", unsafe_allow_html=True)
with st.form("chat-form", clear_on_submit=True):
    user_input = st.text_area("", placeholder="Type your message here...", height=100, label_visibility="collapsed")
    submit = st.form_submit_button("Send")
st.markdown("</div>", unsafe_allow_html=True)

# 📤 On Submit
if submit and user_input.strip() != "":
    with st.spinner("Thinking..."):
        response = client.complete(
            messages=[
                SystemMessage(content=system_prompt),
                UserMessage(content=user_input),
            ],
            temperature=1,
            top_p=1,
            model=model,
        )
        reply = response.choices[0].message.content
        st.session_state["chat_history"].append({"user": user_input, "ai": reply})
        st.rerun()
