from flask import make_response
import os
import io
from PIL import Image
from code.consts import GIF_FPS, IMG_STEP

# here I multiply by IMG_STEP to preserve the total GIF duration
# if we use only every other frame, then each one's duration is twice as long
TIME_PER_FRAME = (1000//GIF_FPS)*IMG_STEP


def directory2GIF(dir):
    try:
        _, _, filenames = next(os.walk(dir))
    except:
        return None
    filenames.sort(key=lambda a: int(a[1:a.index("]")]))
    # add images only if their index is divisible by IMG_STEP
    images = [Image.open(os.path.join(dir, filename)) for i, filename in enumerate(
        filenames) if (i % IMG_STEP == 0 and '.jpg' in filename)]
    buffer = io.BytesIO()
    images[0].save(buffer, format="GIF",
                   save_all=True, append_images=images[1:], duration=TIME_PER_FRAME, loop=0, optimize=True)
    GIFforClient = buffer.getvalue()
    return GIFforClient


def directory2GIF_response(dir):
    gif = directory2GIF(dir)
    if gif is not None:
        response = make_response(gif)
        response.headers['Content-Type'] = 'image/gif'
        return response
    else:
        return "Directory for this timestamp does not exist", 404
