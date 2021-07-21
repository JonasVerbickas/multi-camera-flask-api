from code.fast_img_rating.sharpness_detector import detectSharpness
from code.fast_img_rating.hand_detectorNEW import detectHand
import numpy as np
from joblib import load


clf = load('svmModel.joblib')


def calcEmptyProb(fg):
    fg_pixels = np.count_nonzero(fg)
    total_pixels = (fg.shape[0]*fg.shape[1])
    return fg_pixels/total_pixels


def img2vector(bgr, fg):
    lap = detectSharpness(bgr)
    hand_percentage = detectHand(bgr)
    empty_prob = calcEmptyProb(fg)
    return np.array([lap, hand_percentage, empty_prob])


def fastImgScore(bgr, fg):
    rating_vector = img2vector(bgr, fg)
    rating_vector = rating_vector.reshape(1, -1)
    weightedScore = clf.predict_proba(rating_vector)[0][1]
    return weightedScore
