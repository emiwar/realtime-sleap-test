import cv2

class FakeCamera:
    """
    Simulates a camera by reading frames from a video file using OpenCV.
    """

    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")

    def grab_frame(self):
        """
        Returns the next frame from the video file.
        If the end is reached, it loops back to the start.
        """
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        return frame

    def release(self):
        """
        Releases the video capture object.
        """
        self.cap.release()

    @property
    def width(self):
        """
        Returns the width of the video frames.
        """
        return int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self):
        """
        Returns the height of the video frames.
        """
        return int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    