"""
Server which responds to a GET request with the "best" image in JPG format captured in a certain interval
"""

import os
import logging
from threading import Thread
from flask import Flask, send_from_directory
from code.server_responder import ServerResponder
from time import strftime
from code.consts import DEFAULT_TIME_FORMAT


class Server:
    def __init__(self, json_config):
        self.run_flag = True
        self.app = Flask("API")
        self.__setupLogging()
        self.__createEndpoints()
        self.server_responder = ServerResponder(json_config)
        self.server_responder.cam_man.startCapturingCamStreams()

    def __setupLogging(self):
        try:
            os.mkdir("logs")
        except FileExistsError:
            pass
        handler = logging.FileHandler(
            f'logs/{strftime(DEFAULT_TIME_FORMAT)}.log')  # Create the file logger
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
        handler.setFormatter(formatter)
        self.app.logger.addHandler(handler)
        self.app.logger.setLevel(logging.DEBUG)

    def __createEndpoints(self):

        @self.app.route('/favicon.ico')
        def favicon():
            return send_from_directory(os.path.join(self.app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

        @ self.app.route('/<int:cam_id>', methods=['GET'])
        def getImage(cam_id):
            self.app.logger.debug(
                f'GET ===========> Request for cam[{cam_id}] received! ')
            response = self.server_responder.getJPG(cam_id)
            self.app.logger.debug(f'Responded to cam[{cam_id}]')
            return response

        @ self.app.route('/<int:cam_id>/gif', methods=['GET'])
        def getGIF(cam_id):
            response = self.server_responder.getGIF(cam_id, req_time=None)
            self.app.logger.debug(f'Responded to cam[{cam_id}]')
            return response

        @ self.app.route('/cam_id=<int:cam_id>&req_time=<float:req_time>', methods=['GET'])
        def getImageUsingReqTime(cam_id, req_time):
            self.app.logger.debug(
                f'GET request (with Delta) for cam[{cam_id}] received')
            response = self.server_responder.getJPG(cam_id, req_time=req_time)
            self.app.logger.debug(f'Responded to cam[{cam_id}]')
            return response

        @ self.app.route('/cam_id=<int:cam_id>&req_time=<float:req_time>/gif', methods=['GET'])
        def getGIFUsingReqTime(cam_id, req_time):
            response = self.server_responder.getGIF(cam_id, req_time=req_time)
            self.app.logger.debug(f'Responded to cam[{cam_id}]')
            return response

        @ self.app.route('/<int:cam_id>/start/<int:item_code>', methods=['GET'])
        def startRecording(cam_id, item_code):
            return self.server_responder.cam_recorder.spawnThreadForRecording(cam_id, item_code)

        @ self.app.route('/<int:cam_id>/stop/<int:item_code>', methods=['GET'])
        def stopRecording(cam_id, item_code):
            return self.server_responder.cam_recorder.stopRecording(cam_id)
        server_thread = Thread(target=self.app.run)
        server_thread.setDaemon(True)
        server_thread.start()
        self.app.logger.info("INIT ============> Server created")
