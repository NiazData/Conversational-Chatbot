import streamlit as st
import os

from dotenv import load_dotenv
#load_dotenv()

from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

# --- PAGE CONFIG ---
st.set_page_config(page_title="Tax & Bookkeeping AI Assistant", layout="centered")

# --- INLINE CSS FOR CUSTOM STYLING ---
st.markdown("""
    <style>
    /* Hide Streamlit default menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Set a background image & color overlay for the entire app */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(
            rgba(255,255,255, 0.6),
            rgba(255,255,255, 0.6)
          ),
          url("https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?ixid=M3w5MTMyMXwwfDF8c2VhcmNofDF8fHRheCUyMGZvcm1zfGVufDB8fHx8MTY4ODU2ODcwOQ&ixlib=rb-4.0.3&w=1600")
          no-repeat center fixed;
        background-size: cover;
    }

    /* Optionally adjust padding so content is more readable over the background */
    .block-container {
        padding: 2rem 2rem 3rem 2rem;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.70);
    }

    /* Style the header */
    h1, h2, h3, h4 {
        color:  #1E40AF; /* Deep Blue */   /*#333333;*/
        font-weight: 700;
    }
    h1 {
        margin-top: 0.5rem;
        font-size: 2.2rem;
    }

    /* Style the text input label */
    .stTextInput > label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333333;
    }

    /* Style the "Get Answer" button */
    .stButton>button {
        background-color: #1D4ED8; /* A deep blue color */
        color: white;
        font-weight: 600;
        font-size: 1rem;
        border-radius: 8px;
        padding: 0.6rem 1.25rem;
        border: none;
        transition: background-color 0.3s ease;
        margin-top: 0.5rem;
    }
    /*.stButton>button:hover {
        background-color: #163B8C;
        cursor: pointer;
    }*/

    /* Subheader styling */
    .stMarkdown h2 {
        color: #1D4ED8;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- APP HEADER ---
st.header("Ask Your Tax & Bookkeeping Questions")

# --- SETUP CHAT MODEL ---
chat_model = ChatOpenAI(
    temperature=0.5,
    openai_api_key=os.getenv("OPEN_API_KEY")
)

# --- SESSION STATE FOR CONVERSATION ---
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
    st.session_state["messages"].append(HumanMessage(content=user_query))
    response = chat_model.invoke(st.session_state["messages"])
    st.session_state["messages"].append(AIMessage(content=response.content))
    return response.content

# --- APP UI ---
user_query = st.text_input("Enter your question about Tax/Bookkeeping here:")
submit = st.button("Get Answer")

if submit:
    if user_query.strip():
        answer = get_model_response(user_query.strip())
        st.subheader("Assistant’s Response:")
        st.write(answer)

        # Optional: Throw confetti or balloons for flair
        st.balloons()
    else:
        st.warning("Please type a question before clicking 'Get Answer'.")

# --- HIDE CONVERSATION HISTORY (commented out) ---
# with st.expander("Show Conversation History"):
#     for msg in st.session_state["messages"]:
#         if isinstance(msg, SystemMessage):
#             speaker = "System"
#         elif isinstance(msg, HumanMessage):
#             speaker = "You"
#         else:
#             speaker = "Assistant"
#         st.markdown(f"**{speaker}:** {msg.content}")
