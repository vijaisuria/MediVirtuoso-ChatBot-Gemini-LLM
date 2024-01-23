import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import time
import random
from utils import SAFETY_SETTTINGS

# Load environment variables from .env file
load_dotenv()

# Get the GOOGLE_API_KEY from the environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")

page_icon_path = "logo.png"
if os.path.exists(page_icon_path):
    st.set_page_config(
        page_title="MediBot",
        page_icon="page_icon_path", 
        menu_items={
            'About': "# Make By hiliuxg"
        }
    )


st.title("MediVirtuoso")
st.caption("Unveiling the Symphony of Healing with Comprehensive Drug Knowledge, Side Effect Insights, and Precision Dosage Guidance.")

try:
    genai.configure(api_key=google_api_key)
except AttributeError as e:
    st.warning("Please Configure Gemini App Key First.")

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat()

with st.sidebar:
    if st.button("Clear Chat Window", use_container_width=True, type="primary"):
        st.rerun()

for message in chat.history:
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input(""):
    prompt = prompt.replace('\n', '  \n')
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        try:
            full_response = ""
            for chunk in chat.send_message(prompt, stream=True, safety_settings=SAFETY_SETTTINGS):
                word_count = 0
                random_int = random.randint(5, 10)
                for word in chunk.text:
                    full_response += word
                    word_count += 1
                    if word_count == random_int:
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "_")
                        word_count = 0
                        random_int = random.randint(5, 10)
            message_placeholder.markdown(full_response)
        except genai.types.generation_types.BlockedPromptException as e:
            st.exception(e)
        except Exception as e:
            st.exception(e)
