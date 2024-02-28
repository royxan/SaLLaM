import streamlit as st
from utils import write_message
from agent import generate_response

st.set_page_config("SaLLaM", page_icon="⛓️")

st.title('SALLAM')
st.subheader('Chatbot Taharah Perbedaan Mazhab Fikih')
st.info("Jawaban mengacu pada Kitab Rahmatul Ummah Fi Ikhtilaf Al-A'immah Karya Muhammad bin Abdurrahman As-Syafii Ad-Dimaski")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Salam, saya chatbot untuk perbedaan mazhab fikih. Apa yang ingin Anda tanyakan?"},
    ]

def handle_submit(message):
    with st.spinner('Mohon menunggu sebentar...'):
        
        response = generate_response(message)
        write_message('assistant', response)

with st.container():
    for message in st.session_state.messages:
        write_message(message['role'], message['content'], save=False)

    if prompt := st.chat_input("Tulis pertanyaan di sini ..."):
        write_message('user', prompt)

        handle_submit(prompt)