import streamlit as st
from openai import OpenAI
import os
from datetime import datetime
from textblob import TextBlob
import requests

# Load API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Empathic AI Companion", layout="centered")
st.title("🧠 Empathic AI Companion")
st.markdown("""
This is your safe space. No judgment. No advice. Just a caring listener.
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sentiment analysis to detect mood
def detect_mood(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.5:
        return "😊 Uplifting mood"
    elif polarity > 0:
        return "🙂 Slightly positive mood"
    elif polarity < -0.5:
        return "😢 Very sad mood"
    elif polarity < 0:
        return "🙁 Slightly down mood"
    else:
        return "😐 Neutral mood"

# Function to generate GPT response
def generate_reply(prompt):
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "HTTP-Referer": "https://your-app-name.streamlit.app",  # Optional but recommended
        "Content-Type": "application/json",
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are an empathetic, non-judgmental companion..."},
            {"role": "user", "content": prompt}
        ],
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        reply = res.json()['choices'][0]['message']['content']
        return reply.strip()
    except Exception as e:
        st.error(f"OpenRouter error: {e}")
        return "⚠️ Sorry, something went wrong."
    
# User input
user_input = st.chat_input("Talk to me...")
if user_input:
    mood = detect_mood(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    reply = generate_reply(user_input)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Display chat history
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
        if i == len(st.session_state.messages) - 2:
            mood_label = detect_mood(msg["content"])
            st.caption(f"Detected mood: {mood_label}")
    else:
        st.chat_message("assistant").write(msg["content"])

st.markdown("---")
st.caption("Made with 💙 using Streamlit and OpenAI")
