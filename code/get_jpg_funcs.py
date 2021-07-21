from time import sleep
from joblib import load
from datetime import datetime
from code.buffer.buffer_adjuster import BufferAdjuster
from code.utils.get_best_rated_img import getBestRatedImageUsingRatings
from code.utils.benchmark_wrapper import benchmarkWrapper
from code.feature_extractor.feature_extractor import FeatureExtractor
from code.consts import DEFAULT_DELTA, BUFFER_SIZE

import logging
logger = logging.getLogger("API")


class GetJPGFuncs:
    # this is a class because that way these funcs share their constants
    def __init__(self, cam_man, rating_system, buf_saver, BUFFER_BEFORE_REQUEST, USE_TRASH_DETECTION):
        self.cam_man = cam_man
        self.rating_system = rating_system
        self.buf_saver = buf_saver
        self.BUFFER_BEFORE_REQUEST = BUFFER_BEFORE_REQUEST
        self.USE_TRASH_DETECTION = USE_TRASH_DETECTION
        if self.USE_TRASH_DETECTION:
            self.extractor = FeatureExtractor()
            self.extracted_clf = load('newestExtractor.joblib')

    def rateCroppedBuffer(self, bgr, fg):
        ratings = self.rating_system.rateBuffer(bgr.copy(), fg.copy())
        return ratings

    def sleepAfterRequest(self, req_time=None):
        if req_time is None:
            print("No delta specified (assuming 50ms)")
            sleep_time = (1 - self.BUFFER_BEFORE_REQUEST) * \
                BUFFER_SIZE - DEFAULT_DELTA
        else:
            req_time = datetime.fromtimestamp(req_time)
            print("req:", req_time)
            curr_time = datetime.now()
            print("curr:", curr_time)
            delta = (curr_time - req_time).total_seconds()
            sleep_time = BUFFER_SIZE - delta
        if sleep_time > 0:
            # in case delta is negative and req_time is in the future
            # sleep for no longer than 1 buffer_size
            if sleep_time > BUFFER_SIZE:
                sleep_time = BUFFER_SIZE
            logger.info(
                f"Will collect frames AFTER the request for {sleep_time}s and {BUFFER_SIZE - sleep_time}s BEFORE the req")
            sleep(sleep_time)
        else:
            logger.info(
                "No time to sleep and collect images!!\n (Probably to delta was too big)")

    def getBestBGRInCam(self, cam_id, req_time=None, save_buffers=False):
        cropped_bgr, cropped_fg = BufferAdjuster.getBuffersThenCrop(
            self.cam_man.cams[cam_id])
        ratings = benchmarkWrapper(
            lambda: self.rateCroppedBuffer(cropped_bgr, cropped_fg))
        best_image = getBestRatedImageUsingRatings(cropped_bgr, ratings)
        best_index = ratings.index(max(ratings))
        if self.USE_TRASH_DETECTION:
            extracted_features = self.extractor.get_features(best_image)
            good_quality = self.extracted_clf.predict(extracted_features)
        else:
            good_quality = True
        if not good_quality:
            ratings = [-1 for _ in ratings]
            best_image = None
        if save_buffers:
            self.buf_saver.spawnAThreadToSaveBuffer(
                self.cam_man.cams[cam_id], cropped_bgr, ratings, req_time, best_index)
        return best_image
