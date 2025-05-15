import face_recognition
import face_recognition_models
import numpy as np
import cv2
from PIL import Image
import io
import base64

def process_base64_image(base64_image):
    """Process a base64 image and return face encoding"""
    try:
        # Decode base64 image
        image_data = base64.b64decode(base64_image.split(',')[1])
        image = Image.open(io.BytesIO(image_data))
        image_array = np.array(image)
        
        # Convert RGB to BGR if needed
        if len(image_array.shape) == 3 and image_array.shape[2] == 3:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        # Detect face and get encoding
        face_locations = face_recognition.face_locations(image_array)
        if not face_locations:
            return None, "No face detected in image"

        face_encoding = face_recognition.face_encodings(image_array, face_locations)[0]
        return face_encoding, None
    except Exception as e:
        return None, str(e)

def compare_face_encodings(known_encoding, unknown_encoding):
    """Compare two face encodings and return if they match"""
    try:
        # Reshape if needed
        if isinstance(known_encoding, bytes):
            known_encoding = np.frombuffer(known_encoding, dtype=np.float64)
        
        # Compare faces
        matches = face_recognition.compare_faces([known_encoding], unknown_encoding)
        return matches[0], None
    except Exception as e:
        return False, str(e)
