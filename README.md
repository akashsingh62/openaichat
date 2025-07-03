# 🤖 Local AI Chat App using Ollama + Streamlit

A sleek, privacy-first conversational chat app powered by **Ollama's LLaMA3** model and built with **Streamlit**. Ask questions and get responses — all running locally with **no API keys, no cloud dependencies**.

---

## 📸 Demo

![Chat App Screenshot](chatbot screen shot .png)

---

## ✨ Features

✅ Fully local — no internet, no cloud model  
✅ Powered by LLaMA3 via [Ollama](https://ollama.com)  
✅ Responsive UI using Streamlit  
✅ Chat history display  
✅ Modern dark theme  

---

## 🚀 How It Works

- User enters a query in the text box.
- The prompt is passed to `Ollama` via `ChatOllama`.
- The response is returned and rendered in the chat window.
- All chats are stored in `st.session_state` for history.

---

## 🛠️ Installation & Setup

### 1. Clone this repository

```bash
git clone https://github.com/your-username/ollama-streamlit-chat.git
cd ollama-streamlit-chat
