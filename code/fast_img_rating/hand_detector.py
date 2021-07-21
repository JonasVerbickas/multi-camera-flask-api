import cv2
import numpy as np

"""
Returns true if hand was found and false if it was not.
"""


def detectHand(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Hue is from 0 to 10 AKA lower
    lower_red = np.array([0, 30, 140])
    upper_red = np.array([10, 80, 220])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    lower_res = cv2.bitwise_and(img, img, mask=mask)
    # Hue is from 170 to 180 AKA upper
    lower_red = np.array([170, 30, 140])
    upper_red = np.array([180, 80, 220])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    upper_res = cv2.bitwise_and(img, img, mask=mask)
    # combine lower and upper
    res = cv2.bitwise_or(lower_res, upper_res)
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    non_zeroes = np.shape(np.nonzero(gray))[1]
    total_num_of_pixels = np.shape(hsv)[0] * np.shape(hsv)[1]
    percentage_of_nonzeroes = round(non_zeroes/total_num_of_pixels, 3)
    return percentage_of_nonzeroes
