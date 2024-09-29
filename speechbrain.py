import streamlit as st
import torchaudio
from speechbrain.pretrained import SpeakerRecognition
from st_custom_components import st_audiorecorder
import numpy as np
import os
import io
from scipy.io.wavfile import write

# Initialize the Speaker Recognition Model from SpeechBrain
recognizer = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="tmp_model")

# Streamlit UI
st.title("Speaker Recognition with SpeechBrain")

# Record the first audio
st.write("Record your first audio sample:")
audio_1 = st_audiorecorder()

if audio_1 is not None:
    # Convert recorded audio to a NumPy array and save as WAV
    sample_rate = 16000  # Streamlit Audio Recorder uses 16kHz by default
    audio_1_np = np.frombuffer(audio_1, np.int16)  # Decode raw audio to NumPy
    audio_1_path = "audio_1.wav"
    
    # Save audio to WAV format
    write(audio_1_path, sample_rate, audio_1_np)
    
    # Load audio using torchaudio
    signal_1, fs_1 = torchaudio.load(audio_1_path)
    
    # Extract speaker embeddings from the first recording
    embeddings_1 = recognizer.encode_batch(signal_1)
    
    # Display speaker embedding
    st.write("Speaker Embedding for first audio:", embeddings_1)
    
    # Allow user to record a second audio sample for comparison
    st.write("Record a second audio sample for speaker verification:")
    audio_2 = st_audiorecorder(key="second_audio")
    
    if audio_2 is not None:
        # Convert second recording to NumPy array and save as WAV
        audio_2_np = np.frombuffer(audio_2, np.int16)
        audio_2_path = "audio_2.wav"
        
        write(audio_2_path, sample_rate, audio_2_np)
        
        # Load second audio using torchaudio
        signal_2, fs_2 = torchaudio.load(audio_2_path)
        
        # Extract embeddings from second recording
        embeddings_2 = recognizer.encode_batch(signal_2)
        
        # Perform speaker verification between the two recordings
        score, decision = recognizer.verify_batch(signal_1, signal_2)
        
        # Display the similarity score and the decision
        st.write("Speaker Similarity Score:", score.item())
        st.write("Are the speakers the same?", "Yes" if decision else "No")

# Clean up temp files if needed
if os.path.exists("audio_1.wav"):
    os.remove("audio_1.wav")
if os.path.exists("audio_2.wav"):
    os.remove("audio_2.wav")
