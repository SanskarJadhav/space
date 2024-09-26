# from deepface import DeepFace

# try:
#     result = DeepFace.verify(
#         img1_path = "SanskarJadhavpic.jpeg",
#         img2_path = "SanskarJadhav_sit_id.jpeg",
#         anti_spoofing = True
#     )
#     print(result)
# except ValueError:
#     print("Spoofing detected")

import streamlit as st
import numpy as np
from deepface import DeepFace
from PIL import Image
import os
import io
import sqlite3

# Set TensorFlow log level
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Initialize the SQLite database
# conn = sqlite3.connect('image_paths.db')
# c = conn.cursor()

# # Create a table to store image paths
# c.execute('''
#     CREATE TABLE IF NOT EXISTS images (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         img_name TEXT NOT NULL,
#         img_path TEXT NOT NULL
#     )
# ''')
# conn.commit()

# Title of the Streamlit App
st.title("Face Verification with DeepFace")

# Upload two images for comparison
img1 = st.file_uploader("Upload First Image", type=["jpg", "jpeg", "png"])
img2 = st.file_uploader("Upload Second Image", type=["jpg", "jpeg", "png"])

# Function to save uploaded images and insert their paths into the database
# def save_image(uploaded_file, filename):
#     # Insert image path into the database
#     c.execute("INSERT INTO images (img_name, img_path) VALUES (?, ?)", (uploaded_file.name, filename))
#     conn.commit()
#     return filename

# # Retrieve the image path from the database by filename
# def get_image_path(img_name):
#     c.execute("SELECT img_path FROM images WHERE img_name = ?", (img_name,))
#     data = c.fetchone()
#     return data[0] if data else None

# When both images are uploaded, process them
if img1 and img2:
    # Convert the BytesIO objects back to bytes

    img1pil = Image.open(img1)
    img2pil = Image.open(img2)
    image1 = np.array(Image.open(img1))
    image2 = np.array(Image.open(img2))
    
    try:
            # Perform face verification using DeepFace
        result = DeepFace.verify(
            img1_path=img1pil,
            img2_path=img2pil,
            enforce_detection=False,  # Skip face detection if necessary
            anti_spoofing=True        # Enable anti-spoofing
        )

        # Show the result
        if result['verified']:
            st.success("Faces match!")
        else:
            st.error("Faces do not match.")
        st.write(result)  # Output the complete result dictionary
    else:
        st.error("Image paths not found in the database.")
except ValueError as e:
    st.error("Spoofing detected!")
    st.error(e)
