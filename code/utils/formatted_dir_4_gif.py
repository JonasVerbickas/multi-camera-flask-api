import os
from datetime import datetime
from code.consts import DEFAULT_TIME_FORMAT


def formatUsingReqTime(parent_dir, cam_id, req_time):
    curr_time = datetime.fromtimestamp(req_time)
    curr_time = curr_time.strftime(DEFAULT_TIME_FORMAT)
    formatted_dir = os.path.join(
        parent_dir, f"cam[{cam_id}] {curr_time}")
    return formatted_dir


def convertFolderName2Time(folder_name, cam_id):
    date_string = folder_name.split(f"cam[{cam_id}] ")[1]
    datetime_var = datetime.strptime(date_string, "%m-%d-%Y %H.%M.%S")
    return datetime_var


def formatWithoutReqTime(parent_dir, cam_id):
    latest = {'folder': None, 'time': None}
    for root, dirs, files in os.walk(parent_dir):
        if f"cam[{cam_id}]" in root:
            if latest['folder'] is None:
                latest['folder'] = root
                latest['time'] = convertFolderName2Time(root, cam_id)
            else:
                new_time = convertFolderName2Time(root, cam_id)
                if new_time > latest['time']:
                    latest['folder'] = root
                    latest['time'] = new_time
    return latest['folder']


def formattedDirectoryName(parent_dir, cam_id, req_time=None):
    if req_time is None:
        return formatWithoutReqTime(parent_dir, cam_id)
    else:
        return formatUsingReqTime(parent_dir, cam_id, req_time)
