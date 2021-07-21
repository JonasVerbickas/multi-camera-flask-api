def getBestRatedImageUsingRatings(img_list, rating_list):
    return img_list[rating_list.index(max(rating_list))]
