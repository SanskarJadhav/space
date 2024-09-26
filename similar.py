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
from deepface import DeepFace
from PIL import Image
import os
import sqlite3

# Set TensorFlow log level
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Initialize the SQLite database
conn = sqlite3.connect('image_paths.db')
c = conn.cursor()

# Create a table to store image paths
c.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        img_name TEXT NOT NULL,
        img_path TEXT NOT NULL
    )
''')
conn.commit()

# Title of the Streamlit App
st.title("Face Verification with DeepFace")

# Upload two images for comparison
img1 = st.file_uploader("Upload First Image", type=["jpg", "jpeg", "png"])
img2 = st.file_uploader("Upload Second Image", type=["jpg", "jpeg", "png"])

# Function to save uploaded images and insert their paths into the database
def save_image(uploaded_file, filename):
    with open(filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
    # Insert image path into the database
    c.execute("INSERT INTO images (img_name, img_path) VALUES (?, ?)", (uploaded_file.name, filename))
    conn.commit()
    return filename

# Retrieve the image path from the database by filename
def get_image_path(img_name):
    c.execute("SELECT img_path FROM images WHERE img_name = ?", (img_name,))
    data = c.fetchone()
    return data[0] if data else None

# When both images are uploaded, process them
if img1 and img2:
    # Save the images and insert paths into the SQLite database
    img1_path = save_image(img1, "uploaded_img1.jpg")
    img2_path = save_image(img2, "uploaded_img2.jpg")

    # Button to trigger face verification
    if st.button("Verify Faces"):
        try:
            # Retrieve image paths from the database
            img1_db_path = get_image_path(img1.name)
            img2_db_path = get_image_path(img2.name)

            if img1_db_path and img2_db_path:
                # Perform face verification using DeepFace
                result = DeepFace.verify(
                    img1_path=img1_db_path,
                    img2_path=img2_db_path,
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
