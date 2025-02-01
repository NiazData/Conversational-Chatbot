#pip install streamlit
#pip install langchain-openai
import os
import streamlit as st
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

# Set your OpenAI key
os.environ["OPENAI_API_KEY"] = "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"


def main():
    st.title("English to Bengali Translator")

    # Search bar (text input)
    user_input = st.text_input("Enter your English text to translate:")

    if st.button("Translate"):
        # Only run if user actually typed something
        if user_input.strip():
            # Initialize the ChatOpenAI model
            chat = ChatOpenAI(temperature=0.2)

            # Create the prompt (in this case, instruct the model to translate to Bengali)
            prompt = f"Translate this sentence to Bengali: {user_input}"
            message = HumanMessage(content=prompt)

            # Send the message to the model
            response = chat.invoke([message])

            # Display the model’s output in the app
            st.write("**Translation:**")
            st.success(response.content)  # success box for better visibility

if __name__ == "__main__":
    main()
