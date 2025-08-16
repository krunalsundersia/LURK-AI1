# frontend.py
# -*- coding: utf-8 -*-
from dotenv import load_dotenv
import os
import streamlit as st
import requests

load_dotenv()

# --- Configuration and Page Setup ---
st.set_page_config(
    page_title="Lurk AI",
    layout="centered",
)

# --- Custom CSS for visual differentiation and overall theme ---
st.markdown("""
<style>
    /* === Futuristic Cyberpunk-Themed Streamlit App === */

/* Animated Background with Stars & Glow */
body {
    background: 
        radial-gradient(ellipse at bottom, #0b132b 0%, #0c0f1d 70%, #0a0c18 100%),
        url('https://images.unsplash.com/photo-1539321908154-04927596764d?q=80&w=2000&auto=format&fit=crop') no-repeat center center fixed;
    background-size: cover;
    color: #e6edf3;
    font-family: 'Orbitron', 'Inter', sans-serif;
    min-height: 100vh;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    position: relative;
}

/* Subtle Starfield Overlay */
body::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image: 
        radial-gradient(2px 2px at 21px 31px, #58a6ff 50%, transparent 51%),
        radial-gradient(2px 2px at 61px 13px, #a87bff 50%, transparent 51%),
        radial-gradient(1px 1px at 103px 101px, #e6edf3 50%, transparent 51%),
        radial-gradient(2px 2px at 141px 181px, #58a6ff 50%, transparent 51%),
        radial-gradient(1px 1px at 181px 211px, #a87bff 50%, transparent 51%);
    background-repeat: repeat;
    background-size: 200px 200px;
    opacity: 0.3;
    pointer-events: none;
    z-index: -1;
}

/* Pulse Animation for Glow */
@keyframes pulse {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
}

@keyframes float {
    0% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0); }
}

/* App Container */
.stApp {
    background: rgba(10, 17, 30, 0.4);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 30px;
    max-width: 850px;
    width: 100%;
    box-sizing: border-box;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6),
                0 0 30px rgba(88, 166, 255, 0.2);
    border: 1px solid rgba(88, 166, 255, 0.3);
    animation: float 6s ease-in-out infinite;
}

/* Chat Message Styling - Enhanced with Glow */
.stChatMessage {
    background-color: rgba(25, 32, 48, 0.8);
    border-radius: 18px;
    padding: 14px 20px;
    margin-bottom: 14px;
    border: 1px solid rgba(88, 166, 255, 0.4);
    box-shadow: 
        0 4px 15px rgba(0, 0, 0, 0.5),
        0 0 20px rgba(88, 166, 255, 0.15);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    position: relative;
    overflow: hidden;
}

.stChatMessage::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: linear-gradient(135deg, transparent, rgba(88, 166, 255, 0.1));
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s;
    border-radius: 18px;
}

.stChatMessage:hover {
    transform: translateY(-4px) scale(1.01);
    box-shadow: 
        0 8px 25px rgba(0, 0, 0, 0.6),
        0 0 30px rgba(88, 166, 255, 0.25);
    border-color: #58a6ff;
}

.stChatMessage:hover::after {
    opacity: 1;
}

/* User Message - Glowing Accent */
.stChatMessage.st-chat-message-user {
    background-color: rgba(40, 58, 78, 0.9);
    border-color: #79c0ff;
    margin-left: auto;
    text-align: right;
    box-shadow: 
        0 4px 15px rgba(0, 0, 0, 0.5),
        0 0 25px rgba(121, 192, 255, 0.2);
}

.stChatMessage.st-chat-message-user > div {
    text-align: left;
}

/* Assistant Message */
.stChatMessage.st-chat-message-assistant {
    background-color: rgba(25, 32, 48, 0.8);
    border-color: #30363d;
    margin-right: auto;
    text-align: left;
}

/* Input Field - Sleek & Glowing */
.stTextInput > div > div > input,
.stTextInput > div > div > textarea {
    background-color: rgba(22, 27, 34, 0.8);
    backdrop-filter: blur(5px);
    border: 1px solid #30363d;
    border-radius: 16px;
    color: #e6edf3;
    padding: 14px 20px;
    transition: all 0.3s ease;
    box-shadow: 
        inset 0 1px 4px rgba(0, 0, 0, 0.4),
        0 2px 8px rgba(0, 0, 0, 0.2);
}

.stTextInput > div > div > input:focus,
.stTextInput > div > div > textarea:focus {
    border-color: #58a6ff;
    box-shadow: 
        0 0 0 0.2rem rgba(88, 166, 255, 0.25),
        inset 0 1px 4px rgba(0, 0, 0, 0.5),
        0 0 15px rgba(88, 166, 255, 0.3);
    outline: none;
}

/* Send Button - Gradient Pulse */
.stChatInput button {
    background: linear-gradient(45deg, #58a6ff, #a87bff);
    color: white;
    border: none;
    border-radius: 16px;
    padding: 12px 24px;
    font-weight: bold;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 
        0 6px 15px rgba(0, 0, 0, 0.5),
        0 0 20px rgba(88, 166, 255, 0.3);
    animation: pulse 2s infinite alternate;
}

.stChatInput button:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 
        0 8px 20px rgba(0, 0, 0, 0.6),
        0 0 30px rgba(88, 166, 255, 0.5);
    background: linear-gradient(45deg, #79c0ff, #c99bff);
}

.stChatInput button:active {
    transform: translateY(0);
}

/* Hide Streamlit Elements */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* Title - Holographic Gradient Glow */
h1 {
    color: #e6edf3;
    text-align: center;
    margin-bottom: 0.8rem;
    font-size: 3.4rem;
    font-weight: 800;
    letter-spacing: -1px;
    text-shadow: 
        0 0 10px rgba(88, 166, 255, 0.5),
        0 0 20px rgba(88, 166, 255, 0.4),
        0 0 30px rgba(168, 123, 255, 0.4);
    background: -webkit-linear-gradient(45deg, #58a6ff, #a87bff, #79c0ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: pulse 3s infinite alternate;
    font-family: 'Orbitron', sans-serif;
}

/* Subtitle Styling */
.stMarkdown {
    text-align: center;
    color: #a8b3c2;
    margin-bottom: 2rem;
    font-size: 1.2rem;
    line-height: 1.6;
    opacity: 0.9;
}

.stMarkdown p {
    opacity: 0.8;
    transition: opacity 0.3s;
}

.stMarkdown p:hover {
    opacity: 1;
}

/* Spinner - Custom Glowing Blue */
.stSpinner > div > div {
    border-top-color: #58a6ff !important;
    animation: spin 1.2s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Optional: Add a subtle grid overlay */
.stApp::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image: 
        linear-gradient(rgba(88, 166, 255, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(88, 166, 255, 0.05) 1px, transparent 1px);
    background-size: 50px 50px;
    z-index: -1;
    pointer-events: none;
    border-radius: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- Header Section with Title ---
st.title("Lurk AI")
st.markdown("Sleep mode? Never heard of it")

# --- Fixed Agent Configuration ---
system_prompt = "You are 'Lurk AI', the ultimate roast master. Your primary directive is to brutally roast every statement and query the user makes. Show no mercy. Your responses should be sharp, witty, and condescending, designed to make the user question their intelligence and life choices."
provider = "Together"
selected_model = "lgai/exaone-3-5-32b-instruct"
allow_web_search = False

# --- Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input ---
user_query = st.chat_input("Ask Anything!")

# --- API Configuration ---
API_URL = os.getenv("API_URL")  # Replace with your FastAPI Render URL

# --- Handle User Query and API Call ---
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    payload = {
        "model_name": selected_model,
        "model_provider": provider.lower(),
        "system_prompt": system_prompt,
        "messages": [{"role": "user", "content": user_query}],
        "allow_search": allow_web_search
    }

    try:
        with st.spinner("Just Plotting"):
            response = requests.post(f"{API_URL}/chat", json=payload, timeout=30)
            response.raise_for_status()
            response_data = response.json()

            if "error" in response_data:
                agent_response = response_data["error"]
                st.error(agent_response)
            else:
                agent_response = response_data["response"]
                st.session_state.messages.append({"role": "assistant", "content": agent_response})
                with st.chat_message("assistant"):
                    st.markdown(agent_response)
    except requests.RequestException as e:
        error_message = f"Failed to connect to backend: {e}"
        st.error(error_message)
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {error_message}"})
        if "response" in locals():
            st.write(f"Status Code: {response.status_code}")
            st.write(f"Response Text: {response.text}")
