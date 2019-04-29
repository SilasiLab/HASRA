import datetime
from threading import Thread
import cv2
import time
import subprocess

class FPS_camera:
    def __init__(self):
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # start the timer
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()


class WebcamVideoStream:
    def __init__(self, src=0, width=1280, height=720):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.width = width
        self.height = height
        ret1 = self.stream.set(3, self.width)
        ret2 = self.stream.set(4, self.height)
        (self.grabbed, self.frame) = self.stream.read()
        self.thread = None
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
        # print(self.stream.get(cv2.CAP_PROP_AUTO_EXPOSURE))
        # print(self.stream.get(cv2.CAP_PROP_EXPOSURE))
    def start(self):
        # start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

class Recoder():

    def __init__(self, savePath='test.avi', show=False, vs=None):
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.writer = cv2.VideoWriter(savePath, self.fourcc, 120.0, (1280, 720), False)
        self.stopped = False
        self.FPS = FPS_camera()
        self.vs = vs
        self.thread = None
        self.show = show

    def recording(self):
        self.FPS = self.FPS.start()
        while True:
            if self.stopped:
                break
            frame = self.vs.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.writer.write(gray)
            if self.show:
                cv2.imshow('video', gray)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            self.FPS.update()
        self.writer.release()

    def start(self):
        # start the thread to read frames from the video stream
        self.thread = Thread(target=self.recording, args=())
        self.thread.start()
        return self

    def stop(self):
        # indicate that the thread should be stopped
        self.FPS.stop()
        print("[INFO] elasped time: {:.2f}".format(self.FPS.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.FPS.fps()))
        self.stopped = True

if __name__ == '__main__':
    print("[INFO] sampling THREADED frames from webcam...")
    vs = WebcamVideoStream(src=0).start()
    r = Recoder(savePath='test.avi', vs=vs, show=True).start()
    time.sleep(5)
    r.stop()
    vs.stop()
