import time

import tqdm

import controller
import camera


input_video = "./sample_input_video.mp4"
n_cameras = 3

cameras = [camera.FakeCamera(input_video) for i in range(n_cameras)]
con = controller.Controller(cameras)

#for i in range(100):
#    con.step()
#con.finish()

start_time = time.perf_counter()
for i in tqdm.trange(1000):
    con.move_frames_to_gpu()
    con.track_frames()
    con.encode_frames()
run_time = time.perf_counter() - start_time
print(run_time)

