import streamlit as st
from medicine_chatbot import MedicineChatbot
import os
import json
import random

# Set page config
st.set_page_config(page_title="Medicine Data Chatbot", layout="wide")

# Initialize the chatbot
@st.cache_resource
def get_chatbot():
    return MedicineChatbot()

chatbot = get_chatbot()

# Custom CSS for better styling
st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

def save_chat_history(chat_history):
    desktop_path = os.path.expanduser("~/Desktop")
    filename = os.path.join(desktop_path, "medicine_chatbot_history.json")
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            existing_history = json.load(f)
    else:
        existing_history = []

    existing_history.extend(chat_history)

    with open(filename, 'w') as f:
        json.dump(existing_history, f, indent=4)

def main():
    st.title("Medicine Data Chatbot")
    st.markdown('<p class="big-font">I\'m a Medicine Chatbot. I can provide information about specific tablets, their descriptions, and side effects.</p>', unsafe_allow_html=True)
    st.warning("This chatbot provides general information only. Always consult a healthcare professional for medical advice.")

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # User options as buttons
    st.write("What would you like to do?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Ask about a specific tablet"):
            st.session_state.mode = "specific"
    with col2:
        if st.button("Get random tablet facts"):
            st.session_state.mode = "random"
    with col3:
        if st.button("Hear a medicine joke"):
            st.session_state.mode = "joke"

    # Handle user input based on selected mode
    if 'mode' in st.session_state:
        if st.session_state.mode == "specific":
            user_input = st.text_input("Enter the tablet name or your query:")
            if user_input:
                process_query(user_input)
        elif st.session_state.mode == "random":
            if st.button("Get Random Tablet Info"):
                display_random_info()
        elif st.session_state.mode == "joke":
            display_medicine_joke()

def process_query(user_input):
    with st.spinner("Processing your query..."):
        try:
            response, confidence_score, response_time = chatbot.generate_response(user_input)

            st.info(f"Confidence Score: {confidence_score:.2f} | Response Time: {response_time:.2f} seconds")

            for key, value in response.items():
                st.markdown(f"**{key}**: {value}")

            # Save chat history
            st.session_state.chat_history.append({"query": user_input, "response": response})
            save_chat_history(st.session_state.chat_history)

        except Exception as e:
            st.error(f"An error occurred: {e}")

def display_random_info():
    random_info = chatbot.get_random_tablet_info()
    st.subheader("Random Tablet Fact")
    st.write(f"**Name**: {random_info['Product Name']}")
    st.write(f"**Description**: {random_info['Description']}")
    st.write(f"**Side Effects**: {random_info['Side Effects']}")
    st.write(f"**Drug Interactions**: {random_info['Drug Interactions']}")
    st.write(f"**Salt Composition**: {random_info['Salt Composition']}")

def display_medicine_joke():
    jokes = [
        "Why did the pharmacy cross the road? To get to the other side effects!",
        "What do you call a doctor who fixes websites? A URL-ologist!",
        "Why don't scientists trust atoms? Because they make up everything!",
        "What kind of medicine do you give to a seasick crocodile? Anti-gator!",
        "Why did the pill bottle need glasses? It couldn't see the expiration date!"
        
    ]
    st.write(random.choice(jokes))

if __name__ == "__main__":
    main()
