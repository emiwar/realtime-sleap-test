import time

import tqdm

import controller
import camera


input_video = "./sample_input_video.mp4"
n_cameras = 3

cameras = [camera.FakeCamera(input_video) for i in range(n_cameras)]
con = controller.Controller(cameras)

con.step()
#for i in range(100):
#    con.step()
#con.finish()

run_times = []
for i in tqdm.trange(1000):
    start_time = time.perf_counter()
    #con.step()
    con.move_frames_to_gpu()
    con.track_frames()
    con.encode_frames()
    run_time = time.perf_counter() - start_time
    run_times.append(run_time)
    
import matplotlib.pyplot as plt
plt.plot(run_times)#.join(","))
plt.xlabel("Frame #")
plt.ylabel("Runtime [s]")
plt.ylim(0, 0.025)
plt.savefig("per_step_timing_processing_only.png", dpi=200)
#plt.show()
