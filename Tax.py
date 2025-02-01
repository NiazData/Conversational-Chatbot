import streamlit as st
import os

# If you're using a .env file, load environment variables
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

# 3. Function to pass user input + conversation history to the model
def get_model_response(user_query):
    # Add user's latest question to the conversation
    st.session_state["messages"].append(HumanMessage(content=user_query))
    
    # Get the response from the model
    response = chat_model.invoke(st.session_state["messages"])
    
    # Append the AI response to the conversation
    st.session_state["messages"].append(AIMessage(content=response.content))
    
    return response.content

# 4. Streamlit UI
user_query = st.text_input("Enter your question about Tax/Bookkeeping here:")
submit = st.button("Get Answer")

if submit:
    if user_query.strip():
        answer = get_model_response(user_query.strip())
        st.subheader("Assistant’s Response:")
        st.write(answer)
    else:
        st.warning("Please type in a question before clicking 'Get Answer'.")

# 5. (Optional) Display full conversation history
#    This can be useful for debugging or to show chat flow in the UI.
with st.expander("Show Conversation History"):
    for i, msg in enumerate(st.session_state["messages"]):
        speaker = "System" if isinstance(msg, SystemMessage) else \
                  "User" if isinstance(msg, HumanMessage) else "Assistant"
        st.markdown(f"**{speaker}:** {msg.content}")
