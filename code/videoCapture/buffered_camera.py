"""
Stores footage captured by our camera to a buffer

The "main" window shows footage in real time and displays the area which is sent to the buffer
"""

import cv2
from time import perf_counter
from code.buffer.buffer import Buffer
from code.videoCapture.cropping.click_cropper import ClickCropper
from code.videoCapture.cropping.drag_cropper import DragCropper
from code.utils.img_resizing import calculateResizeKeepAspectRatio, imageAspectRatioResize
from code.consts import BG_HISTORY_SIZE, TEMP_GUI_DISPLAY_TIME, GUI_ENABLED_DEFAULT, TARGET_DISPLAY_WIDTH, USE_CLICK_CROPPER, BUFFER_SIZE


class VideoInputNotFound(Exception):
    def __init__(self, video_url):
        self.message = video_url
        super().__init__(self.message)


class BufferedCamera():
    def __init__(self, streamURL, cam_id):
        self.cam = cv2.VideoCapture(streamURL)
        resolution = self.getResolution()
        if 0 in resolution:
            raise VideoInputNotFound(streamURL)
        self.GUI_enabled = GUI_ENABLED_DEFAULT
        self.id = cam_id
        self.__initCropper(resolution)
        self.__initBuffers()
        self.fgbg = cv2.createBackgroundSubtractorMOG2(
            history=BG_HISTORY_SIZE, detectShadows=False)

    def createTempGUI(self):
        cv2.namedWindow(str(self.id))
        cv2.setMouseCallback(str(self.id), self.cropper.cropOnClick)
        self.GUI_enabled = True
        self.GUI_creation_time = perf_counter()
        print(f"Displaying cam[{self.id}]")

    def __destroyGUI(self):
        self.GUI_enabled = False
        cv2.destroyWindow(str(self.id))
        print(f"cam[{self.id}] GUI destroyed")

    def __initCropper(self, resolution):
        if USE_CLICK_CROPPER:
            self.cropper = ClickCropper(resolution, calculateResizeKeepAspectRatio(
                resolution[0], resolution[1], width=TARGET_DISPLAY_WIDTH))
        else:
            self.cropper = DragCropper(calculateResizeKeepAspectRatio(
                resolution[0], resolution[1], width=TARGET_DISPLAY_WIDTH))

    def __initBuffers(self):
        FPS = self.cam.get(5)
        buf_size = int(FPS*BUFFER_SIZE)
        self.buf = Buffer(buf_size)
        self.subtracted_bg_buf = Buffer(buf_size)

    # =============================================================
    # private methods

    def __downscaleToTarget(self, img):
        return imageAspectRatioResize(img, width=TARGET_DISPLAY_WIDTH)

    def __addFrameToBuffer(self, frame):
        self.buf.add(frame)

    # =================================================================
    # PUBLIC methods
    def GUI_newestFrame(self):
        if len(self.buf.getList()) > 0:
            if self.GUI_enabled:
                if perf_counter() - self.GUI_creation_time > TEMP_GUI_DISPLAY_TIME:
                    self.__destroyGUI()
                else:
                    newest_frame = self.buf.get(0)
                    outlined_ROI = self.cropper.drawCropArea(newest_frame)
                    downsized_with_ROI = self.__downscaleToTarget(outlined_ROI)
                    cv2.imshow(str(self.id), downsized_with_ROI)

    def readloop(self):
        while True:
            self.read()

    def read(self):
        _, frame = self.cam.read()
        if frame is not None:
            self.__addFrameToBuffer(frame)
            subtractedBG = self.fgbg.apply(frame)
            self.subtracted_bg_buf.add(subtractedBG)

    def getResolution(self):
        res = (int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)),
               int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        return res
