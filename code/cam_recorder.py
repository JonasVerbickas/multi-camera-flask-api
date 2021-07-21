import os
from threading import Thread
from pathlib import Path
from time import sleep, time
from code.server_methods.convert_to_JPG import compressedJPG
from code.consts import RECORDING_SAVE_DIR, CAPTURE_LIMIT, BUFFER_SIZE

import logging
logger = logging.getLogger("API")


class CamRecorder:
    def __init__(self, cam_man, getBestBGRInCam):
        self.cam_man = cam_man
        self.getBestBGRInCam = getBestBGRInCam
        self.currently_capturing = []

    def spawnThreadForRecording(self, cam_id, item_code):
        validation_res = self.cam_man.validateCamId(cam_id)
        if validation_res != "OK":
            return validation_res
        else:
            cam_id = int(cam_id)
            self.currently_capturing.append(cam_id)
            t = Thread(target=self.recordFootage, args=[cam_id, item_code])
            t.start()
            logger.info(f"Started recording cam[{cam_id}]")
            return "Caputure started successfully"

    def rateBufferAndSaveBestImg(self, cam_id, directory_path):
        best_image = self.getBestBGRInCam(cam_id)
        if best_image is not None:
            jpg = compressedJPG(best_image)
            path, dirs, files = next(os.walk(directory_path))
            num_of_older_files = len(files)
            curr_jpg_path = os.path.join(
                directory_path, f"{num_of_older_files}.jpg")
            with open(curr_jpg_path, 'wb') as f:
                f.write(jpg)

    def recordFootage(self, cam_id, item_code):
        # create parent directory if it does not exist
        item_code = str(item_code)
        directory_path = os.path.join(RECORDING_SAVE_DIR, item_code)
        Path(directory_path).mkdir(
            parents=True, exist_ok=True)
        starting_time = time()
        while time() - starting_time < CAPTURE_LIMIT and cam_id in self.currently_capturing:
            sleep(BUFFER_SIZE)
            # the use of threading allows python to make a better use of the time spent sleeping
            # otherwise the delays between captures are bigger than expected
            t = Thread(target=self.rateBufferAndSaveBestImg, args=[
                       cam_id, directory_path])
            t.start()
        else:
            logger.info(
                f"cam[{cam_id}] recording has been stopped")

    def stopRecording(self, cam_id):
        try:
            cam_id = int(cam_id)
            self.currently_capturing.remove(cam_id)
            return "Capture stopped"
        except ValueError:
            return "Wrong cam id"
