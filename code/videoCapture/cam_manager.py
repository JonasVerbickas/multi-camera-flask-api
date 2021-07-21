from threading import Thread
from code.videoCapture.buffered_camera import BufferedCamera
from code.utils.KBHit import KBHit
from cv2 import waitKey
from code.consts import THREADED_CAM_CAPTURE

import logging
logger = logging.getLogger("API")


class CamManager:
    def __init__(self, json_config):
        self.KBHit = KBHit()
        self.STREAM_URLS = json_config['STREAM_URLS']
        self.cams = []
        for i, url in enumerate(self.STREAM_URLS):
            cam = BufferedCamera(url, i)
            self.cams.append(cam)
        logger.info(
            "INIT ============> Camera manager initialzed")

    def validateCamId(self, cam_id):
        try:
            cam_id = int(cam_id)
        except ValueError:
            return f"Could not convert {cam_id=} to int"
        try:
            self.cams[cam_id]
        except IndexError:
            return "Cam_id is out of bounds"
        return "OK"

    def startCapturingCamStreams(self):
        if THREADED_CAM_CAPTURE:
            ts = [Thread(target=cam.readloop) for cam in self.cams]
            for t in ts:
                t.start()
        logger.info(
            "INIT DONE ============> Accepting requests.")
        print(
            f"!===== Press keys 0-{len(self.cams)-1} to GUI each camera")
        while True:
            if self.KBHit.kbhit():
                c = self.KBHit.getch()
                validation_res = self.validateCamId(c)
                if validation_res == 'OK':
                    self.cams[int(c)].createTempGUI()
                else:
                    print(validation_res)
            for c in self.cams:
                if not THREADED_CAM_CAPTURE:
                    c.read()
                c.GUI_newestFrame()
            waitKey(1)
