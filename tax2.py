import streamlit as st
import os

from dotenv import load_dotenv
load_dotenv()

from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

st.set_page_config(page_title="Tax & Bookkeeping AI Assistant")
st.header("Ask Your Tax & Bookkeeping Questions")

# 1. Create/OpenAI chat model with your desired temperature
chat_model = ChatOpenAI(
    temperature=0.5,
    openai_api_key="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"

)

# 2. Initialize session state to store conversation
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        SystemMessage(content=(
            "You are a helpful AI assistant specialized in Tax and Bookkeeping. "
            "You provide general informational guidance, not professional advice. "
            "Always remind users to consult a professional if needed."
        ))
    ]

def get_model_response(user_query: str) -> str:
    """Get AI response given the conversation so far + user query."""
    # Add user message
    st.session_state["messages"].append(HumanMessage(content=user_query))

    # Invoke the model
    response = chat_model.invoke(st.session_state["messages"])

    # Add AI message to the conversation
    st.session_state["messages"].append(AIMessage(content=response.content))
    return response.content

# 3. Minimal UI: Just input, button, and final answer
user_query = st.text_input("Enter your question about Tax/Bookkeeping here:")
submit = st.button("Get Answer")

if submit:
    if user_query.strip():
        answer = get_model_response(user_query.strip())
        st.subheader("Assistant’s Response:")
        st.write(answer)
    else:
        st.warning("Please type in a question before clicking 'Get Answer'.")

# 4. (Optional) Remove or comment out any conversation display
#    This ensures users never see the System or Human messages.
