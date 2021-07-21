# (seconds) default delta is assumed if no req_time is specified
DEFAULT_DELTA = 0.05

# buffered cam
BG_HISTORY_SIZE = 2000
TEMP_GUI_DISPLAY_TIME = 10
GUI_ENABLED_DEFAULT = False  # should cam video GUIs be always on?

# folder/file datetime format
DEFAULT_TIME_FORMAT = "%m-%d-%Y %H.%M.%S"

# gif creation
# desired FPS
GIF_FPS = 30
# img used in gif if (img_index % IMG_STEP == 0)
IMG_STEP = 3

# buffered cam
TARGET_DISPLAY_WIDTH = 350  # size of the GUI window

# buffer saver
SAVE_BUFFERS = True
BUFFER_SAVE_DIR = "savedBuffers"
USE_CLICK_CROPPER = True  # if False a draggable cropper will be used
BUFFER_SIZE = 2  # footage length in seconds stored in buffer for rating

# rating system
USE_Nth_FRAME = 4  # frame index in buffer should be divisable by this number to be rated

# should footage from each cam be in a separate thread
THREADED_CAM_CAPTURE = False

# cropper
AREA_SIZE = (300, 300)  # the size of ROI drawn onClick
OUTLINE_THICKNESS = 2  # the thickness of the ROI outline

# cam recorder
RECORDING_SAVE_DIR = "capturedFootage"
CAPTURE_LIMIT = 300  # seconds
