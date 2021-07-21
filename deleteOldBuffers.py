import re
from os import listdir
from os import path
from datetime import datetime
from shutil import rmtree

PATTERN = "^cam\[\d+\] \d{2}-\d{2}-\d{4} \d{2}.\d{2}.\d{2}$"

"""
Deletes all subdirectories in parent that match PATTERN and are older than removal_age (in days).
AGE is measured using the names of folders!!
"""
def deleteOldSaves(parent_directory="savedBuffers", removal_age=7):
    now = datetime.now()
    removed_directories = []
    for i in listdir(parent_directory):
        if re.match(PATTERN, i):
            i_list = i.split(' ')
            d = datetime.strptime(i_list[1], '%m-%d-%Y')
            diff = now - d
            if diff.days >= removal_age:
                removed_directories.append(i)
                rmtree(path.join(parent_directory, i))
    if len(removed_directories) > 0:
        print("Removed:", removed_directories)
    else:
        print("No subdirectories matched the pattern.")


if __name__ == "__main__":
    deleteOldSaves(removal_age=0)
