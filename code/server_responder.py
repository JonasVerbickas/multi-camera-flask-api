"""
Server which responds to a GET request with the "best" image in JPG format captured in a certain interval
"""

from code.cam_recorder import CamRecorder
from code.get_jpg_funcs import GetJPGFuncs
from code.rating_system import RatingSystem
from code.buffer.buffer_saver import BufferSaver
from code.videoCapture.cam_manager import CamManager
from code.server_methods.bgr_to_response import BGR2Response
from code.utils.formatted_dir_4_gif import formattedDirectoryName
from code.utils.directory2GIF import directory2GIF_response
from code.consts import SAVE_BUFFERS, BUFFER_SAVE_DIR


class ServerResponder:
    def __init__(self, json_config):
        self.BUFFER_BEFORE_REQUEST = json_config["BUFFER_BEFORE_REQUEST"]
        if SAVE_BUFFERS:
            self.buf_saver = BufferSaver()
        self.cam_man = CamManager(json_config['CamManager'])
        self.rating_system = RatingSystem(json_config["USE_RATING_MODEL"])
        self.jpg_funcs = GetJPGFuncs(self.cam_man, self.rating_system, self.buf_saver,
                                     self.BUFFER_BEFORE_REQUEST, json_config["USE_TRASH_DETECTION"])
        self.cam_recorder = CamRecorder(
            self.cam_man, self.jpg_funcs.getBestBGRInCam)

    def getJPG(self, cam_id, req_time=None):
        print('\n')
        self.jpg_funcs.sleepAfterRequest(req_time)
        validation_res = self.cam_man.validateCamId(cam_id)
        if validation_res != "OK":
            return validation_res
        else:
            best_image = self.jpg_funcs.getBestBGRInCam(
                cam_id, req_time=req_time, save_buffers=SAVE_BUFFERS)
            if best_image is not None:
                response = BGR2Response(best_image)
                return response
            else:
                return ""

    def getGIF(self, cam_id, req_time):
        directory_name = formattedDirectoryName(
            BUFFER_SAVE_DIR, cam_id, req_time)
        res = directory2GIF_response(directory_name)
        return res
