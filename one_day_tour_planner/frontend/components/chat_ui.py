import streamlit as st

def chat_ui():
    """
    This function creates a simple chat UI for the user to interact with.
    It allows users to enter their messages and send them to the chat bot or backend.
    """

    # Title and instructions
    st.title("Chat with Assistant")
    st.markdown("""
    ### Welcome to the Chat Interface!
    Type your message below and click "Send" to interact with the assistant.
    """)

    # Display chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Displaying chat history
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.write(f"**You:** {message['text']}")
        else:
            st.write(f"**Assistant:** {message['text']}")

    # User input
    user_message = st.text_area("User:", "", height=100)

    # Send button to submit message
    if st.button("Send"):
        if user_message.strip():  # If the user has entered a non-empty message
            # Save user message to session state
            st.session_state.messages.append({'role': 'user', 'text': user_message})

            # Here you would typically send the message to the backend (e.g., to OpenAI or other APIs)
            # In this case, we are simulating a response from the assistant.
            assistant_response = get_assistant_response(user_message)

            # Save assistant's response to session state
            st.session_state.messages.append({'role': 'assistant', 'text': assistant_response})

            # Clear the user message input field
            st.text_area("User:", "", height=100, key="new_message")  # Clear the field

            # Refresh the page to display the new message
            st.experimental_rerun()

def get_assistant_response(user_message: str) -> str:
    """
    A simple placeholder function that simulates the assistant's response.
    In a real application, you would replace this with an API call to the backend.
    
    Args:
        user_message (str): The message input by the user.

    Returns:
        str: The simulated response from the assistant.
    """
    # This is where you would integrate with a backend or AI service to get real responses
    return f"Assistant's response to: {user_message}"
