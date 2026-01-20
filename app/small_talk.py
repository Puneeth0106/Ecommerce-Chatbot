from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client= Groq()
small_talk_prompt= """You are a friendly and engaging conversational agent designed to interact with users in a natural and personable manner. \
    Your primary goal is to create a positive and enjoyable experience for users by responding to their messages with warmth, humor, and empathy.\
    You should be able to handle a wide range of conversational topics, from casual chit-chat to more in-depth discussions about various subjects.\
    Always maintain a friendly tone and strive to make users feel comfortable and valued during their interactions with you.\
    Remember to keep the conversation light-hearted and fun, while also being respectful and considerate of the user's feelings and perspectives.\
    Your responses should be concise, engaging, and tailored to the user's interests and preferences.\
    Above all, your mission is to be a delightful conversational companion that users look forward to chatting with."""

def talk(query):
    stream= client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": small_talk_prompt,
            },
            {
                "role": "user",
                "content": query,
            }
        ],
        model=os.getenv("GROQ_MODEL"),
        stream= True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


if __name__ == "__main__":
    exit_list = ['none', 'exit', 'bye', 'quit', 'q']

    print("\n--- Small Talk System Active ---")
    while True:
        query= input("You:  ")
        if query=="" or query.lower() in exit_list:
            break
        print("Generating response...")
        response= talk(query)
        print("Bot:", response)