import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title("Healthcare Assistant - Chat with a Medical Expert")

# Brief description
st.write("Welcome to the Healthcare Assistant. You can ask about health-related topics, symptoms, medications, and more!")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Collect user input
user_input = st.chat_input("How can I assist you with your health today?")

# Function to get a response from OpenAI with healthcare-specific context
def get_response(prompt):
    # Custom system message for healthcare assistant behavior
    system_message = {
        "role": "system",
        "content": ("You are a healthcare assistant that helps users with health-related information. "
                    "You provide general health advice, symptom descriptions, lifestyle recommendations, "
                    "and medical information based on reliable sources. However, always remind the user "
                    "to consult a healthcare professional for a diagnosis or treatment plan. "
                    "If the user asks for something outside your knowledge, direct them to a doctor.")
    }

    # Send the conversation history along with the system message for more context
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            system_message
        ] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages] +
        [{"role": "user", "content": prompt}]
    )
    # Access the content directly as an attribute
    return response.choices[0].message.content

# Process and display response if there's input
if user_input:
    # Append user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant's response
    assistant_response = get_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)

