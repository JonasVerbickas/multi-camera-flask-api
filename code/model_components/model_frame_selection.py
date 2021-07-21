import tensorflow as tf
import numpy as np


class ClearSelector():
    def __init__(self, backbone_path, backbone_x, backbone_y, svm_path, mean, std, preprocess_func):
        self.backbone = tf.keras.models.load_model(backbone_path)
        self.x = backbone_x
        self.y = backbone_y

    # might be getting BRG from open cv, so image array may need further processing
    def run_on_img(self, im):
        im = tf.image.resize(im, [self.x, self.y]).numpy()
        im = np.reshape(im, [1, self.x, self.y, 3])
        return self.backbone.predict(tf.image.resize(im, [224, 224]))[0][0]


if __name__ == "__main__":
    params = {"backbone_path": "", "backbone_x": 224, "backbone_y": 224,
              "svm_path": "", "mean": 0, "std": 1, "preprocess_func": None}
    selector = ClearSelector(**params)
