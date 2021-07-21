from cv2 import resize, INTER_AREA


def calculateResizeKeepAspectRatio(original_w, original_h,  width=None, height=None):
    if original_h == 0 or original_w == 0:
        return None
    if width is None and height is None:
        return (original_w, original_h)
    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(original_h)
        new_res = (int(original_w * r), height)
        return new_res
    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(original_w)
        new_res = (width, int(original_h * r))
        return new_res


def imageAspectRatioResize(image, width=None, height=None, inter=INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    dim = calculateResizeKeepAspectRatio(w, h, width, height)
    # resize the image
    resized = resize(image, dim, interpolation=inter)
    # return the resized image
    return resized
