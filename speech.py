import streamlit as st
import torchaudio
from speechbrain.pretrained import SpeakerRecognition
from audio_recorder_streamlit import audio_recorder
import io
from pydub import AudioSegment

# Initialize the Speaker Recognition Model from SpeechBrain
recognizer = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="tmp_model")

# Streamlit UI
st.title("Speaker Recognition with SpeechBrain")

# Record the first audio sample
st.write("Record your first audio sample:")
audio_bytes_1 = audio_recorder(pause_threshold=3.0, format="mp3")

if audio_bytes_1:
    # Load audio from MP3 bytes and convert to WAV using pydub
    audio_1 = AudioSegment.from_file(io.BytesIO(audio_bytes_1), format="mp3")
    audio_1_wav = io.BytesIO()
    audio_1.export(audio_1_wav, format="wav")
    
    # Load the converted WAV file using torchaudio
    signal_1, fs_1 = torchaudio.load(audio_1_wav)
    
    # Extract speaker embeddings from the first recording
    embeddings_1 = recognizer.encode_batch(signal_1)
    
    # Display speaker embedding
    st.write("Speaker Embedding for first audio:", embeddings_1)
    
    # Record the second audio sample for comparison
    st.write("Record a second audio sample for speaker verification:")
    audio_bytes_2 = audio_recorder(pause_threshold=3.0, format="mp3", key="second_audio")

    if audio_bytes_2:
        # Load second recording from MP3 bytes and convert to WAV
        audio_2 = AudioSegment.from_file(io.BytesIO(audio_bytes_2), format="mp3")
        audio_2_wav = io.BytesIO()
        audio_2.export(audio_2_wav, format="wav")
        
        # Load the second audio sample using torchaudio
        signal_2, fs_2 = torchaudio.load(audio_2_wav)
        
        # Extract embeddings from the second recording
        embeddings_2 = recognizer.encode_batch(signal_2)
        
        # Perform speaker verification between the two recordings
        score, decision = recognizer.verify_batch(signal_1, signal_2)
        
        # Display the similarity score and the decision
        st.write("Speaker Similarity Score:", score.item())
        st.write("Are the speakers the same?", "Yes" if decision else "No")
