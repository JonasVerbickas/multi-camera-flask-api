import os
from time import strftime
from datetime import datetime
from code.consts import DEFAULT_TIME_FORMAT


def formattedDirectoryName(parent_dir, cam_id, req_time=None):
    if req_time is None:
        curr_time = strftime(DEFAULT_TIME_FORMAT)
    else:
        curr_time = datetime.fromtimestamp(req_time)
        curr_time = curr_time.strftime(DEFAULT_TIME_FORMAT)
    formatted_dir = os.path.join(
        parent_dir, f"cam[{cam_id}] {curr_time}")
    return formatted_dir
