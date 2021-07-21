from numpy.lib.function_base import kaiser
import tensorflow as tf
import pickle
import numpy as np

class ClearSelector():
    def __init__(self, backbone_path, backbone_x, backbone_y, svm_path, mean, std, preprocess_func):
        self.backbone = tf.keras.models.load_model(backbone_path)
        self.x = backbone_x
        self.y = backbone_y
        self.svm = pickle.load(open(svm_path, 'rb'))
        self.mean = mean
        self.std = std
        self.preprocess_func = preprocess_func

    #might be getting BRG from open cv, so image array may need further processing
    def run_on_img(self, img_array):
        img_array = tf.image.resize(img_array, [self.x, self.y]).numpy()
        img_array = np.reshape(img_array, [1, self.x, self.y, 3])
        #with tf.device("/cpu:0"):
        if self.preprocess_func is not None:
            img_array = self.preprocess_func(img_array)
        features = self.backbone.predict(img_array)
        features = (features - self.mean) / self.std
        probs = self.svm.predict_proba(features)[0]
        return probs[0] #probability that the photo is clear


    def find_best_frame(self, images):
        best_dict = {"img_array":None, "clear_prob":0}
        for im in images:
            prob = self.run_on_img(im)
            if best_dict["clear_prob"] < prob:
                best_dict["clear_prob"] = prob
                best_dict["img_array"] = im
        return best_dict


if __name__ == "__main__":
    params = {"backbone_path": "", "backbone_x": 224, "backbone_y": 224, "svm_path": "", "mean":0, "std":1, "preprocess_func" : None}
    selector = ClearSelector(**params)