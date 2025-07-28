import io
import PyNvVideoCodec as nvc

class VideoEncoder:
    def __init__(self, width, height, surface_format="ARGB"):
        self.encoder = nvc.CreateEncoder(width=width,
                                         height=height,
                                         fmt=surface_format,
                                         usecpuinputbuffer=False)
        self.buffer = io.BytesIO()

    def encode_frame(self, frame):
        bitstream = self.encoder.Encode(frame)
        if bitstream:
            self.buffer.write(bytearray(bitstream))

    def end_encode(self):
        bitstream = self.encoder.EndEncode()
        if bitstream:
            self.buffer.write(bytearray(bitstream))

    def flush_to_file(self, output_file="output.h264"):
        with open(output_file, 'wb') as f:
            f.write(self.buffer.getvalue())
