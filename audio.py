import streamlit as st
from streamlit_mic_recorder import mic_recorder, speech_to_text

# Initialize session state if it's not already initialized
if 'text_received' not in st.session_state:
    st.session_state['text_received'] = []

# Layout: Convert speech to text
c1, c2 = st.columns(2)
with c1:
    st.write("Convert speech to text:")
with c2:
    text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')

# Append the received text to the session state list
if text:
    st.session_state.text_received.append(text)

# Display all received texts
for t in st.session_state.text_received:
    st.text(t)
    
# Record voice and play the recorded audio
st.write("Record your voice, and play the recorded audio:")
audio = mic_recorder(start_prompt="⏺️", stop_prompt="⏹️", key='recorder')
if audio:
    st.audio(audio['bytes'])
