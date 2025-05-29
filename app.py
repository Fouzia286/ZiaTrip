import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Function to interact with Groq's LLaMA 3 API
def chat_with_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",  # Or use "llama3-70b-8192" if needed
        "messages": [
            {"role": "system", "content": "You are a helpful travel planning assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit UI
st.set_page_config(page_title="Personal Travel Assistant")
st.title("✈️ ZiaTrip")

# Inputs
budget = st.number_input("Enter your budget ($)", min_value=100)
duration = st.slider("Trip Duration (days)", 1, 30)
interests = st.multiselect("Select Interests", ["Beaches", "Hiking", "Museums", "Nightlife", "Food", "Shopping", "History"])

# Generate plan
if st.button("Generate Trip Plan"):
    if not interests:
        st.warning("Please select at least one interest.")
    else:
        prompt = (
            f"Plan a {duration}-day trip within a ${budget} budget, focusing on the following interests: "
            f"{', '.join(interests)}. Include destination recommendations, activities, and travel tips."
        )
        with st.spinner("Generating your personalized travel plan..."):
            result = chat_with_groq(prompt)
            st.success("Here's your trip plan:")
            st.write(result)



