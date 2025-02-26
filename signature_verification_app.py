# app.py
import streamlit as st
import cv2
import numpy as np
from utils_signature_verification import preprocess_signature, extract_features, compute_similarity
def main():
    st.title("Handwritten Signature Verification")
    st.write("Upload two signatures to check if they match.")

# Upload signatures
uploaded_file1 = st.file_uploader("Upload Signature 1", type=["jpg", "png", "jpeg"])
uploaded_file2 = st.file_uploader("Upload Signature 2", type=["jpg", "png", "jpeg"])

if uploaded_file1 and uploaded_file2:
    # Read and preprocess images
    file_bytes1 = np.asarray(bytearray(uploaded_file1.read()), dtype=np.uint8)
    image1 = cv2.imdecode(file_bytes1, cv2.IMREAD_COLOR)
    preprocessed1 = preprocess_signature(image1)
    
    file_bytes2 = np.asarray(bytearray(uploaded_file2.read()), dtype=np.uint8)
    image2 = cv2.imdecode(file_bytes2, cv2.IMREAD_COLOR)
    preprocessed2 = preprocess_signature(image2)
    
    # Display preprocessed images
    st.image([preprocessed1, preprocessed2], caption=["Signature 1", "Signature 2"], width=300)
    
    # Extract features
    features1 = extract_features(preprocessed1)
    features2 = extract_features(preprocessed2)
    
    # Compute similarity
    similarity = compute_similarity(features1, features2)
    st.write(f"Similarity Score: {similarity:.2f}")
    
    # Threshold for match/non-match
    threshold = 0.7  # Adjust based on your use case
    if similarity > threshold:
        st.success("Signatures MATCH!")
    else:
        st.error("Signatures DO NOT MATCH!")

if __name__ == "__main__":
    main()