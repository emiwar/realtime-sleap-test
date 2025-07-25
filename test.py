import io
import tqdm

import encoder
import camera

import importlib
importlib.reload(encoder)
importlib.reload(camera)

cam = camera.FakeCamera("/home/emil/Development/example-dannce-videos/coltrane/2021_07_28_1/videos/Camera1/0.mp4")

enc = encoder.VideoEncoder(cam.width, cam.height)

for i in tqdm.trange(100):
    frame = cam.grab_frame()
    enc.encode_frame(frame)
enc.end_encode()
enc.flush_to_file()


