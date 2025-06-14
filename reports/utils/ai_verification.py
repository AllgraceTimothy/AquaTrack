import tensorflow as tf
import numpy as np
from PIL import Image
import os

model = tf.keras.models.load_model(os.path.join('reports' ,'ai_models', 'leak_classifier.keras'))

def verify_leak(image_path):
    img = Image.open(image_path).convert('RGB').resize((128, 128))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    prediction = model.predict(img_array)[0][0]
    print(prediction)
    return prediction < 0.5
