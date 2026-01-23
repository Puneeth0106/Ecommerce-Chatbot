"""E-commerce Chatbot Application.

A Streamlit-based chatbot that routes user queries to appropriate handlers:
- FAQ: Frequently asked questions
- SQL: Database queries
- Small talk: General conversation
"""

import streamlit as st
from pathlib import Path

from faq import faq_chain, ingest_faq_data
from router import router
from small_talk import talk
from sql import sql_chain


# Initialize FAQ data
FAQ_DATA_PATH = Path(__file__).parent / "resources/faq_data.csv"
ingest_faq_data(FAQ_DATA_PATH)


def ask_query(query: str) -> str:
    """Route the user query to the appropriate handler.

    Args:
        query: The user's input query string.

    Returns:
        The response from the appropriate handler or an error message.
    """
    route = router(query).name

    if route == "faq":
        return faq_chain(query)
    elif route == "sql":
        return sql_chain(query)
    elif route == "small_talk":
        return talk(query)
    else:
        return f"Route '{route}' is not implemented."


# Page configuration
st.set_page_config(
    page_title="E-commerce Chatbot",
    page_icon="EC",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling
st.markdown(
    """
    <style>
    .main {
        padding-top: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("E-commerce Chatbot")
st.markdown("---")
st.markdown(
    """
    Welcome! I can help you with:
    - FAQ: Frequently asked questions about our products
    - Database Queries: Product information and inventory
    - Small Talk: General conversation
    """
)

# Initialize session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
st.markdown("---")
st.markdown("### Chat History")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
user_query = st.chat_input("Enter your query")

if user_query:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Generate and display assistant response
    with st.chat_message("assistant"):
        response_generator = ask_query(user_query)
        full_response = st.write_stream(response_generator)
    st.session_state.messages.append({"role": "assistant", "content": full_response})