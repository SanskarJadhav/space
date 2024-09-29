import streamlit as st
import numpy as np
import torch
from speechbrain.pretrained import SpeakerRecognition
import audio_recorder_streamlit as ar

# Load pre-trained speaker recognition model from SpeechBrain
speaker_model = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="tmp")

# Title of the web app
st.title("Speaker Recognition App")

# Record the first audio clip
st.header("Record First Audio Clip")
audio1 = ar.audio_recorder(key="audio1")

# Record the second audio clip
st.header("Record Second Audio Clip")
audio2 = ar.audio_recorder(key="audio2")

if audio1 is not None and audio2 is not None:
    # Save audio files temporarily for processing
    with open("audio1.wav", "wb") as f:
        f.write(audio1)
    
    with open("audio2.wav", "wb") as f:
        f.write(audio2)

    # Perform speaker verification
    score, prediction = speaker_model.verify_files("audio1.wav", "audio2.wav")
    
    # Display the result
    st.subheader("Speaker Verification Result")
    if prediction:
        st.success(f"The audios are from the same speaker. (Score: {score:.4f})")
    else:
        st.error(f"The audios are from different speakers. (Score: {score:.4f})")

else:
    st.write("Please record both audio clips.")
