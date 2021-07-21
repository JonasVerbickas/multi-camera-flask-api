class BufferAdjuster:
    @staticmethod
    def getBuffersThenCrop(cam):
        bgr_buf = [cam.cropper.cropFrame(
            frame) for frame in cam.buf.getList()]
        subtracted_bg_buf = [cam.cropper.cropFrame(
            frame) for frame in cam.subtracted_bg_buf.getList()]
        return (bgr_buf, subtracted_bg_buf)
