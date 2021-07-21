import cv2

def compressedJPG(img):
    COMPRESSION = 100  # 100 = no compression, the lower the number the higher the compression
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), COMPRESSION]
    _, converted = cv2.imencode('.jpg', img, encode_param)
    return converted.tobytes()
