import tensorflow as tf
from tensorflow.keras.applications import mobilenet_v2
import cv2
import numpy as np

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class FeatureExtractor():
    def __init__(self, input_shape=(300, 300, 3)):
        self.input_shape = input_shape
        backbone = mobilenet_v2.MobileNetV2(
            include_top=False,
            input_shape=input_shape)
        pooler = tf.keras.layers.GlobalAveragePooling2D(
            name='avg_pool')(backbone.output)
        self.extractor = tf.keras.Model(
            inputs=[backbone.input], outputs=[pooler])

    def get_features(self, bgr):
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        rgb_as_float = rgb.astype(np.float32)
        input_tensor = tf.reshape(rgb_as_float, (1,) + self.input_shape)
        processed_tensor = mobilenet_v2.preprocess_input(input_tensor)
        return self.extractor.predict(processed_tensor)
