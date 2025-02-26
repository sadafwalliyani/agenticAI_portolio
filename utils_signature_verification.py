# utils.py
import cv2
import numpy as np
from skimage.feature import hog
from skimage import exposure

def preprocess_signature(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Thresholding to binarize the image
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Remove noise using morphological operations
    kernel = np.ones((3, 3), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    return cleaned

def extract_features(image):
    # Resize image to a fixed size (e.g., 128x128)
    resized = cv2.resize(image, (128, 128))
    
    # Extract HOG (Histogram of Oriented Gradients) features
    features, hog_image = hog(
        resized,
        orientations=8,
        pixels_per_cell=(16, 16),
        cells_per_block=(1, 1),
        visualize=True
    )
    
    # Optional: Extract additional features (Hu Moments)
    moments = cv2.moments(resized)
    hu_moments = cv2.HuMoments(moments).flatten()
    
    # Combine HOG and Hu Moments
    combined_features = np.concatenate([features, hu_moments])
    
    return combined_features

def compute_similarity(features1, features2):
    # Compute cosine similarity
    similarity = np.dot(features1, features2) / (np.linalg.norm(features1) * np.linalg.norm(features2))
    return similarity