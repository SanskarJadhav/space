import streamlit as st
from whisper_stt import whisper_stt

api = st.secrets["OPENAI_API_KEY"]

text = whisper_stt(openai_api_key=api, language = 'en')  
# If you don't pass an API key, the function will attempt to retrieve it as an environment variable : 'OPENAI_API_KEY'.
if text:
    st.write(text)
