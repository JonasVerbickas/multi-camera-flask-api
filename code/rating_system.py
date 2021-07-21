from code.fast_img_rating.fast_img_rating import fastImgScore
from code.model_components.model_frame_selection import ClearSelector
from code.model_components.configuration import config
from code.consts import USE_Nth_FRAME


class RatingSystem:
    def __init__(self, USE_MODEL):
        self.USE_MODEL = USE_MODEL
        if self.USE_MODEL:
            self.adomo_modelis = ClearSelector(**config)

    def rateImg(self, bgr, fg):
        if self.USE_MODEL:
            score = self.adomo_modelis.run_on_img(bgr)
            return score
        else:
            score = fastImgScore(bgr, fg)
            return score

    def rateBuffer(self, bgr_buf, fg_buf):
        l = []
        for i, img in enumerate(bgr_buf):
            if i % USE_Nth_FRAME == 0:
                l.append(self.rateImg(bgr_buf[i], fg_buf[i]))
            else:
                l.append(0)
        return l
