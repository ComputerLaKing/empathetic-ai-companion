import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Companion", layout="centered")
st.title("🧠 Empathetic AI Companion")

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def query_huggingface(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return f"Error: {response.status_code} — {response.text}"
    try:
        return response.json()[0]["generated_text"]
    except Exception as e:
        return f"Response parsing error: {str(e)}"

with st.form("chat_form"):
    user_input = st.text_input("You:", "", placeholder="Type how you feel...", label_visibility="visible")
    submit = st.form_submit_button("Send")

if submit and user_input:
    with st.spinner("AI Companion is thinking..."):
        response = query_huggingface(user_input)
        st.markdown(f"**AI:** {response}")
