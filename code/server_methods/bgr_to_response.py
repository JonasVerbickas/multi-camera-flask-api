from code.server_methods.convert_to_JPG import compressedJPG
from flask import make_response


def BGR2Response(img):
    jpg = compressedJPG(img)
    response = make_response(jpg)
    response.headers['Content-Type'] = 'image/jpg'
    return response
