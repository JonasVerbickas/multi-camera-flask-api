"""
Currently not in use.
Will be integrated later.
"""


import os.path
import json

SAVE_NAME = "coords.json"

class Saving:
    def __init__(self):
        self.data = self.__loadSavedData()


    def getDataFor(self, key):
        key = str(key)
        if key in self.data.keys():
            return self.data[key]
        else:
            return None


    @staticmethod
    def __loadSavedData():
        if os.path.isfile(SAVE_NAME):
            with open(SAVE_NAME, "r") as f:
                data = json.load(f)
                return data
        else:
            return dict()


    @staticmethod
    def saveData(data):
        with open(SAVE_NAME, "w") as f:
            json.dump(data, f)

