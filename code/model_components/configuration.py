from posixpath import join
import tensorflow as tf
import os

model_compenents_dir = os.path.join(os.getcwd(), "code", "model_components")

config = {"backbone_path":  os.path.join(model_compenents_dir, "backbone"),
          "backbone_x": 224,
          "backbone_y": 224,
          "svm_path": os.path.join(model_compenents_dir, "svm.sav"),
          "mean": 0.4908021,
          "std": 0.6553372,
          "preprocess_func": tf.keras.applications.mobilenet.preprocess_input}
