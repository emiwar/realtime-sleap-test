import tensorflow as tf

#from tensorflow.python.compiler.tensorrt import trt_convert as tf_trt
from tensorflow.python.saved_model import tag_constants

class OptimizedModel:

    def __init__(self, model_path):
        saved_model_loaded = tf.saved_model.load(model_path, tags=[tag_constants.SERVING])
        wrapper_fp32 = saved_model_loaded.signatures['serving_default']
        self.loaded_model_fn = wrapper_fp32

    @tf.function
    def run_inference(self, frames):
        frames = frames[:, :, :, 0:3]
        resized = tf.image.resize(frames, size=[600, 960], method='bilinear',
                                  preserve_aspect_ratio=False, antialias=False)
        casted  = tf.cast(resized, tf.float32)
        transposed = tf.transpose(casted, perm=[0,3,1,2])
        return self.loaded_model_fn(transposed)
