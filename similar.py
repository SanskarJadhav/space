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

# Title of the Streamlit App
st.title("Face Verification with DeepFace")

# Upload two images for comparison
img1 = st.file_uploader("Upload First Image", type=["jpg", "jpeg", "png"])
img2 = st.file_uploader("Upload Second Image", type=["jpg", "jpeg", "png"])

# Function to save uploaded images
def save_image(uploaded_file, filename):
    with open(filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return filename

# When both images are uploaded, process them
if img1 and img2:
    # Save the images locally
    img1_path = save_image(img1, "uploaded_img1.jpg")
    img2_path = save_image(img2, "uploaded_img2.jpg")

    # Button to trigger face verification
    if st.button("Verify Faces"):
        try:
            # Perform face verification using DeepFace
            result = DeepFace.verify(
                img1_path=img1_path,
                img2_path=img2_path,
                enforce_detection=False,  # Skip face detection if necessary
                anti_spoofing=True        # Enable anti-spoofing
            )

            # Show the result
            if result['verified']:
                st.success("Faces match!")
            else:
                st.error("Faces do not match.")
            st.write(result)  # Output the complete result dictionary

        except ValueError as e:
            st.error("Spoofing detected!")