import streamlit as st
import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

#  Load environment variables from .env
load_dotenv()
token = os.environ.get("AZURE_OPENAI_KEY")

#  Azure setup
endpoint = "https://models.github.ai/inference"  # Replace with your endpoint
model = "openai/gpt-4.1"  # Update model if needed

#  Initialize the Azure OpenAI client
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

#  Custom dark theme styling (optional)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #343541;
        color: #ececf1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#  App title
st.title("🧠 Azure OpenAI Chat Application")

#  Input form
with st.form("llm-form"):
    user_input = st.text_area("Enter your question or statement:")
    submit = st.form_submit_button("Submit")

#  Session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# On form submit
if submit and user_input:
    with st.spinner("Generating response..."):
        response = client.complete(
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content=user_input),
            ],
            temperature=1,
            top_p=1,
            model=model
        )
        reply = response.choices[0].message.content
        st.session_state["chat_history"].append({"user": user_input, "ai": reply})
        st.write(reply)

#  Display chat history
st.write("## Chat History")
for chat in reversed(st.session_state["chat_history"]):
    st.write(f"**🧑 User**: {chat['user']}")
    st.write(f"**🧠 Assistant**: {chat['ai']}")
    st.write("---")
