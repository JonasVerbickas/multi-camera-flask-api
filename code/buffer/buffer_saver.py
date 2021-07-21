import os
from pathlib import Path
from code.server_methods.convert_to_JPG import compressedJPG
from code.utils.formatted_dir_4_saving import formattedDirectoryName
from threading import Thread
from code.consts import BUFFER_SAVE_DIR


class BufferSaver:

    def spawnAThreadToSaveBuffer(self, cam, cropped_buffer, ratings, req_time=None, best_index=None):
        t = Thread(
            target=self.saveBuffer,
            args=[
                cam,
                cropped_buffer,
                ratings,
                req_time,
                best_index
            ]
        )
        t.start()

    def saveBuffer(self, cam, reversed_buffer, ratings, req_time=None, best_index=None):
        try:
            # create saved buffer directory if it does not exist
            subdirectory_for_this_buffer = formattedDirectoryName(
                BUFFER_SAVE_DIR, cam.id, req_time)
            Path(subdirectory_for_this_buffer).mkdir(
                parents=True, exist_ok=False)
            # save each image in the buffer
            downsized = reversed_buffer
            for i, img in enumerate(downsized):
                if i < len(ratings):
                    if best_index == i:
                        rating = f"BEST IN BUFFER {round(ratings[i]*100, 2)}"
                    else:
                        rating = round(ratings[i]*100, 2)
                else:
                    rating = "None"
                jpg = compressedJPG(img)
                with open(os.path.join(subdirectory_for_this_buffer, f'[{i}] {rating}.jpg'), 'wb') as f:
                    f.write(jpg)
        except FileExistsError:
            print("This buffer is already saved")
