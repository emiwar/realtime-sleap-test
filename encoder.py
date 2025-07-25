import io

import PyNvVideoCodec as nvc
import tensorflow as tf
import numpy as np 

class VideoEncoder:
    def __init__(self, width, height, surface_format="ARGB"):
        self.encoder = nvc.CreateEncoder(width=width,
                                         height=height,
                                         fmt=surface_format,
                                         usecpuinputbuffer=True)
        self.buffer = io.BytesIO()
        self.framebuffer = np.ones((1, height, width, 4))

    def encode_frame(self, frame):
        #with tf.device('/GPU:0'):
        #    gpu_frame = tf.cast(frame, tf.float32) / 255.0
        #frame = tf.image.rgb_to_yuv(frame)
        self.framebuffer[0, :, :, 0:3] = frame
        bitstream = self.encoder.Encode(self.framebuffer)
        if bitstream:
            self.buffer.write(bytearray(bitstream))

    def end_encode(self):
        bitstream = self.encoder.EndEncode()
        if bitstream:
            self.buffer.write(bytearray(bitstream))

    def flush_to_file(self, output_file="output.h264"):
        with open(output_file, 'wb') as f:
            f.write(self.buffer.getvalue())
