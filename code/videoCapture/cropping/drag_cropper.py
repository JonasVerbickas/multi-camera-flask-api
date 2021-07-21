"""
Allows the user to draw ROI by holding down M1 and dragging their cursor
"""

import cv2
import numpy as np
from code.consts import OUTLINE_THICKNESS


class DragCropper:
    def __init__(self, OG_RESOLUTION):
        self.OG_RESOLUTION = OG_RESOLUTION
        self.crop_starting_coords = None
        self.crop_percentages = [[0.0, 0.0], [0.75, 1.0]]  # in percentages

    def convertRatiosToPixelVals(self, frame):
        res = [np.shape(frame)[1], np.shape(frame)[0]]
        pixel_vals = [[int(xy[0] * res[0]), int(xy[1] * res[1])]
                      for xy in self.crop_percentages]
        return pixel_vals

    def convertPixelValsToRatios(self, x, y):
        return [round(x/float(self.OG_RESOLUTION[0]), 2), round(y/float(self.OG_RESOLUTION[1]), 2)]

    # this function draws a box around the area which will be returned by crop frame

    def drawCropArea(self, frame):
        crop_coords = self.convertRatiosToPixelVals(frame)
        frame_with_indicator = np.array(frame)
        cv2.rectangle(frame_with_indicator,
                      (crop_coords[0][0], crop_coords[0][1]),
                      (crop_coords[1][0], crop_coords[1][1]),
                      (0, 255, 0), OUTLINE_THICKNESS)
        return frame_with_indicator

    # with a whole frame passed in
    # this function returns only the cropped out area set by the user

    def cropFrame(self, frame):
        crop_coords = self.convertRatiosToPixelVals(frame)
        cropped_frame = np.array(frame[crop_coords[0][1]+OUTLINE_THICKNESS:crop_coords[1][1]-OUTLINE_THICKNESS,
                                       crop_coords[0][0]+OUTLINE_THICKNESS:crop_coords[1][0]-OUTLINE_THICKNESS])
        return cropped_frame

    # this function gets executed whenever "main" window registers a click

    def cropOnClick(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.crop_starting_coords = self.convertPixelValsToRatios(x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            if x < self.crop_starting_coords[0]:
                x, self.crop_starting_coords[0] = self.crop_starting_coords[0], x
            if y < self.crop_starting_coords[1]:
                y, self.crop_starting_coords[1] = self.crop_starting_coords[1], y
            if x - self.crop_starting_coords[0] > 0 and y - self.crop_starting_coords[1] > 0:
                self.crop_percentages = [
                    self.crop_starting_coords, self.convertPixelValsToRatios(x, y)]
            self.crop_starting_coords = None

    def resetCropArea(self):
        self.crop_percentages = [[0, 0], [100, 100]]
