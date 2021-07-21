import cv2
import numpy as np
from scipy.spatial import distance as dist
from timeit import timeit


def threshImg(img):
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
    # remove noise
    open_kernel = np.ones((9, 9), np.uint8)
    blurred = cv2.morphologyEx(res, cv2.MORPH_OPEN, open_kernel)
    gray_blurred = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_blurred, 1, 255, cv2.THRESH_BINARY)
    center = [thresh.shape[0] // 2, thresh.shape[1] // 2]
    max_D = dist.euclidean((0, 0), center)
    def f(i, j): return (center[0] - i)**2 + (center[1] - j)**2
    distances_squared = np.fromfunction(f, thresh.shape, dtype=float)
    distances = np.sqrt(distances_squared)
    ratios = 1 - (distances / max_D)
    adjusted_thresh = ratios * thresh
    adjusted_thresh = np.uint8(adjusted_thresh)
    return adjusted_thresh


def scoreThreshed(img):
    total = np.sum(img)
    num_of_pixels = img.shape[0] * img.shape[1]
    return total / num_of_pixels


def detectHand(img):
    thresh = threshImg(img)
    score = scoreThreshed(thresh)
    return round(score, 5)


if __name__ == "__main__":
    im = cv2.imread("mesa.png")
    print(timeit(lambda: print(scoreThreshed(detectHand(im))), number=1))
