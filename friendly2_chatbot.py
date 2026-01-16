import streamlit as st
import pandas as pd
import datetime
from groq import Groq
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


st.set_page_config(page_title="Friendly Feedback Chatbot", page_icon="💬")


# -----------------------
# Load feedback safely
# -----------------------
def load_feedback():
    try:
        return pd.read_csv("feedback_data.csv")
    except:
        return pd.DataFrame(columns=["timestamp", "user", "feedback", "sentiment"])


# -----------------------
# Save feedback (No append())
# -----------------------
def save_feedback(user, feedback, sentiment):
    df = load_feedback()

    new_row = pd.DataFrame([{
        "timestamp": datetime.datetime.now(),
        "user": user,
        "feedback": feedback, 
        "sentiment": sentiment
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("feedback_data.csv", index=False)


# -----------------------
# Groq Sentiment Analysis
# -----------------------
def llm_sentiment(text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"Classify this feedback as Positive, Neutral, or Negative:\n{text}"
            }
        ]
    )
    return response.choices[0].message.content.strip()


# -----------------------
# Groq Friendly Reply
# -----------------------
def llm_reply(text, user):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a friendly chatbot that replies warmly and politely."
            },
            {
                "role": "user",
                "content": f"User '{user}' said: {text}. Give a kind and friendly reply."
            }
        ]
    )
    return response.choices[0].message.content.strip()


# -----------------------
# Streamlit UI
# -----------------------
st.title("💬 Friendly LLM Feedback Chatbot (Groq Powered)")
st.write("I’d love to hear your feedback! 😊")


user = st.text_input("Your Name:")
feedback = st.text_area("Write your feedback here:")

if st.button("Submit Feedback"):
    if user.strip() == "" or feedback.strip() == "":
        st.error("Please enter both name and feedback.")
    else:
        # LLM work
        sentiment = llm_sentiment(feedback)
        reply = llm_reply(feedback, user)

        # Save to CSV
        save_feedback(user, feedback, sentiment)

        # Display
        st.success("Thank you! Your feedback has been saved ❤️")
        st.info(f"Sentiment detected: **{sentiment}**")

        st.write("🤖 **Chatbot Reply:**")
        st.success(reply)


# Show feedback history
if st.checkbox("Show all feedback"):
    df = load_feedback()
    st.dataframe(df)
