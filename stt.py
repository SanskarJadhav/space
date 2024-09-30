import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import os
from audio_recorder_streamlit import audio_recorder

# Function to convert audio file to WAV (if not in WAV format)
def convert_to_wav(uploaded_file):
    audio = AudioSegment.from_file(uploaded_file)
    wav_filename = "converted.wav"
    audio.export(wav_filename, format="wav")
    return wav_filename

# Function to recognize speech from audio file
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file
        try:
            text = recognizer.recognize_sphinx(audio_data)  # Using CMU Sphinx (offline)
            return text
        except sr.UnknownValueError:
            return "Sorry, could not understand the audio."
        except sr.RequestError as e:
            return f"Error with speech recognition service; {e}"

# Streamlit app
st.title("Audio Transcription App")
audio = audio_recorder(sample_rate=41_000)

if audio:
    st.audio(audio, format="audio/wav")
    if st.button("Use this Voice Recording"):
        voice_register(audio)

def voice_register(audio):
     with open("audio2.wav", "wb") as f:
        f.write(audio)

    # Transcribe the audio
    st.write("Transcribing the audio...")
    transcription = transcribe_audio("audio2.wav")
    
    # Display the transcription
    st.subheader("Transcription:")
    st.write(transcription)
else:
    st.write("Please upload an audio file to transcribe.")

