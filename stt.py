import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import os

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

uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg", "flac"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")

    # Convert the file to WAV format if necessary
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    if file_extension != ".wav":
        st.write("Converting audio file to WAV format...")
        audio_file = convert_to_wav(uploaded_file)
    else:
        audio_file = uploaded_file

    # Transcribe the audio
    st.write("Transcribing the audio...")
    transcription = transcribe_audio(audio_file)
    
    # Display the transcription
    st.subheader("Transcription:")
    st.write(transcription)
else:
    st.write("Please upload an audio file to transcribe.")

