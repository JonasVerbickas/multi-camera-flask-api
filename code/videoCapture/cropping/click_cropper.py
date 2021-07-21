"""
Draws ROI area of a set size after a single click
"""

import cv2
import numpy as np
from code.videoCapture.cropping.coord_converter import CoordConverter
from code.videoCapture.cropping.overlap_adjuster import adjustROIForOverlap
from code.consts import OUTLINE_THICKNESS, AREA_SIZE


class ClickCropper:
    def __init__(self, OG_res, DISPLAY_res):
        self.converter = CoordConverter(OG_res, DISPLAY_res)
        self.crop_coords = [[0, 0], [300, 300]]

    # this function draws a box around the area which will be returned by crop frame

    def drawCropArea(self, frame):
        crop_coords = self.crop_coords
        frame_with_indicator = frame.copy()
        cv2.rectangle(frame_with_indicator,
                      (crop_coords[0][0], crop_coords[0][1]),
                      (crop_coords[1][0], crop_coords[1][1]),
                      (0, 255, 0), OUTLINE_THICKNESS)
        return frame_with_indicator

    # with a whole frame passed in
    # this function returns only the cropped out area set by the user

    def cropFrame(self, frame):
        crop_coords = self.crop_coords
        cropped_frame = np.array(frame[crop_coords[0][1]:crop_coords[1][1],
                                       crop_coords[0][0]:crop_coords[1][0]])
        return cropped_frame

    # this function gets executed whenever "main" window registers a click

    def cropOnClick(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            x, y = self.converter.Single_Display2OG((x, y))
            start_coords = [x-AREA_SIZE[0]//2, y-AREA_SIZE[1]//2]
            end_coords = [x+AREA_SIZE[0]//2, y+AREA_SIZE[1]//2]
            self.crop_coords = [start_coords, end_coords]
            adjustROIForOverlap(self.crop_coords, [
                                [0, 0], self.converter.getOG()])
