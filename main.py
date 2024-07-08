from typing import Set
from backend.core import run_llm
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from backend.ingestion import ingest_docs
load_dotenv()

st.header("InfoBrief: A Smart QA Bot")
st.sidebar.title("Article URLs")

url = st.sidebar.text_input("URL")
process_url_clicked = st.sidebar.button("Process URLs")
if process_url_clicked:
    with st.sidebar:
        with st.spinner("Processing URLs.."):
            ingest_docs([url])


if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


def onSend():
    with st.spinner("Generating response.."):
        prompt = st.session_state.user_input
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(generated_response["answer"])
        st.session_state["chat_history"].append((prompt, generated_response["answer"]))
        
chat_placeholder = st.empty()

with chat_placeholder.container():     
    if st.session_state["chat_answers_history"]:
        i=0
        for generated_response, user_query in zip(
            st.session_state["chat_answers_history"],
            st.session_state["user_prompt_history"],
        ):
            message(user_query, is_user=True, key=f"user_{i}")
            message(generated_response, key=f"bot_{i}")
            i+=1
        
with st.container():
    st.chat_input(on_submit=onSend, placeholder="Enter your prompt here..", key="user_input")
    