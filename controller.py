import numpy as np
import tensorflow as tf
import torch

import encoder
import inference

class Controller:

    def __init__(self, cameras, device="/GPU:0", sleap_model="./250715_124120.single_instance.n=9748.batch3.trt.FP32"):
        #Basic validation of input
        if not cameras:
            raise ValueError("Need at least one camera")
        width = cameras[0].width
        height = cameras[0].height
        for camera in cameras:
            if camera.width != width or camera.height != height:
                raise ValueError("All cameras must have the same resolution")
        
        self.cameras = cameras
        self.encoders = [encoder.VideoEncoder(width, height) for cam in cameras]
        self.sleap_model = inference.OptimizedModel(sleap_model)

        self.cpu_framebuffer = np.zeros((len(cameras), height, width, 4), np.uint8)
        with tf.device(device):
            self.gpu_framebuffer = tf.zeros((len(cameras), height, width, 4), np.uint8)

        #Tensorflow tensors can't be directly passed to PyNvVideoCodec, but torch tensors can.
        #So we create a view of the same GPU memory as a torch tensor without copying
        self.torch_buffer = torch.from_dlpack(tf.experimental.dlpack.to_dlpack(self.gpu_framebuffer))

        #Trigger JIT compilation
        self.track_frames()

    def step(self):
        self.grab_frames()
        self.move_frames_to_gpu()
        self.track_frames()
        self.encode_frames()

    def grab_frames(self):
        for (i, camera) in enumerate(self.cameras):
            self.cpu_framebuffer[i, :, :, 0:3] = camera.grab_frame()
        
    def move_frames_to_gpu(self):
        self.torch_buffer[:] = torch.tensor(self.cpu_framebuffer) #.assign(self.cpu_framebuffer)
        torch.cuda.synchronize()

    def track_frames(self):
        self.sleap_model.run_inference(self.gpu_framebuffer)

    def encode_frames(self):
        #Here we access a tensorflow tensor implicitly thourgh dlpack. Need to
        #Since torch and tensorflow have separate CUDA contexts/schedulers, we
        #sync explicitly to be on the safe side
        #tf.test.experimental.sync_devices()
        for (i, encoder) in enumerate(self.encoders):
            encoder.encode_frame(self.torch_buffer[i, :, :, :])
    
    def finish(self):
        for i, encoder in enumerate(self.encoders):
            encoder.flush_to_file(f"encoded_videos/{i}.h264")
