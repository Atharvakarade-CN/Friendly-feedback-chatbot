from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("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"))

print("Hello! I am AI Chatbot. Type 'bye' to exit.")

while True:
    user = input("You: ")

    if user.lower() == "bye":
        print("Bot: Goodbye! 👋")
        break

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": user}
        ]
    )

    bot_reply = response.choices[0].message.content
    print("Bot:", bot_reply)
