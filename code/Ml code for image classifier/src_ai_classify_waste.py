import cv2
import numpy as np
import tensorflow as tf
from picamera2 import Picamera2  # For Raspberry Pi Camera
import time

# Placeholder for pre-trained CNN model (replace with actual model)
model = tf.keras.models.load_model('waste_classifier.h5')

def capture_image():
    picam = Picamera2()
    picam.start()
    time.sleep(2)  # Warm-up camera
    image = picam.capture_array()
    picam.stop()
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

def classify_waste(image):
    # Preprocess image for CNN
    img = cv2.resize(image, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    
    # Predict (0: Biodegradable, 1: Non-biodegradable)
    prediction = model.predict(img)
    return 'Biodegradable' if prediction[0][0] > 0.5 else 'Non-biodegradable'

def main():
    while True:
        image = capture_image()
        result = classify_waste(image)
        print(f"Classified waste as: {result}")
        time.sleep(5)  # Adjust based on needs

if __name__ == "__main__":
    main()