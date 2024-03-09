

import streamlit as st
import os
import textwrap
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = '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'

# Initialize conversation history and user name
conversation_history = []
user_name = ""

def get_ai_response(human_input):
    template = """
    You are a World class Librarian
    Here are the requirements:
    1. Your name is Ameen. You can provide information on any book.
    2. You are always ready to assist book readers. At the end of the sentence, you can use ".
    3. Respond with care and always be optimistic and supportive.
    4. You only respond in Arabic. 
    
    {history}
    User: {human_input}
    Ameen:
    """
    prompt = PromptTemplate(
        input_variables=["history", "human_input"],
        template=template,
    )

    chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt, verbose=False, memory=ConversationBufferWindowMemory(k=5))

    # Add the current user input to the conversation history
    conversation_history.append({'role': 'user', 'content': human_input})

    # Prepare conversation history for AI input, replacing the user's name if available
    history = ""
    for message in conversation_history:
        role = message['role']
        content = message['content']
        if role == 'user':
            content = content.replace("{user_name}", user_name)
            history += f"User: {content}\n"
        elif role == 'assistant':
            history += f"Ameen: {content}\n"

    ai_reply = chain.predict(history=history, human_input=human_input)

    # Add the AI reply to the conversation history
    conversation_history.append({'role': 'assistant', 'content': ai_reply})

    return ai_reply

def save_conversation():
    with open("conversation_history.txt", "w") as file:
        file.write(str(conversation_history))

# Set Streamlit app title and layout
st.title("Chat with Ameen")
st.sidebar.title("Background")

# Get user's name
user_name = st.sidebar.text_input("Your Name:")

st.sidebar.button("Save Conversation", on_click=save_conversation)

# Get user input
user_input = st.text_input("User Input:")

if st.button("Send"):
    conversation_placeholder = st.empty()

    # Display user input in conversation
    conversation_history.append({'role': 'user', 'content': user_input})
    conversation = f"{user_name}: {user_input}\n"
    conversation_placeholder.text(conversation)

    # Get AI response
    ai_response = get_ai_response(user_input)

    # Add AI response to conversation and display
    conversation_history.append({'role': 'assistant', 'content': ai_response})
    conversation += f"Ameen:\n{textwrap.fill(ai_response, width=60)}\n"  
    conversation_placeholder.text(conversation)

# Display conversation history
conversation = ""
for message in conversation_history:
    role = message['role']
    content = message['content']
    if role == 'user':
        content = content.replace("{user_name}", user_name)
    conversation += f"{role.capitalize()}: {content}\n"
st.text_area("Chat History:", value=conversation, height=400, key="chat_history")
