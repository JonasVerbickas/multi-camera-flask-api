import cv2

def detectSharpness(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        gray = img
    lap = cv2.Laplacian(gray, cv2.CV_64F).var()
    lap = round(lap, 2)
    return lap
