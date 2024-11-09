import streamlit as st
from utils.api_requests import collect_preferences
from transformers import pipeline

# Load Hugging Face text generation pipeline (using a pre-trained model like GPT-2)
generator = pipeline("text-generation", model="gpt2")

# Setting up the app's title and description
st.title("One-Day Tour Planning Assistant")
st.markdown("Welcome to the One-Day Tour Planning Assistant! Enter your preferences below to get a personalized plan.")

# Collecting user inputs for tour preferences
city = st.text_input("City to Visit", help="Enter the city where you want to plan your tour.")
start_time = st.time_input("Start Time", help="Pick the time you'd like to start your tour.")
budget = st.number_input("Budget", min_value=0.0, format="%.2f", help="Enter your budget for the tour in your local currency.")

# Button to trigger API request
if st.button("Submit"):
    # Collecting preferences in a dictionary
    preferences = {
        "city": city,
        "start_time": start_time.strftime("%H:%M"),  # Formatting start_time as a string in "HH:MM" format
        "budget": budget
    }

    # Calling the API function to process preferences (assuming the API handles the logic of preferences collection)
    response = collect_preferences(preferences)

    # If response from the API is valid, generate a personalized tour plan using Hugging Face model
    if response:
        st.subheader("Your One-Day Tour Plan:")
        st.write(response)

        # Generate additional content with Hugging Face (e.g., a creative summary or suggestions)
        prompt = f"Create a fun and engaging one-day tour plan for {city} starting at {start_time.strftime('%H:%M')} with a budget of {budget}. Here are the preferences: {response}"
        generated_text = generator(prompt, max_length=200, num_return_sequences=1)

        st.subheader("Tour Plan Summary from AI:")
        st.write(generated_text[0]["generated_text"])
    else:
        st.error("Sorry, we couldn't generate a tour plan with the provided preferences. Please try again.")
