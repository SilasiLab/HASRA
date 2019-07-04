"""
    Author: Junzheng Wu
    Email: jwu220@uottawa.ca
    Organization: University of Ottawa (Silasi Lab)

    To increase FPS, the whole stream is divided into two parallel threads.
    And then those two threads are organized to run as a subprocess in the main.py script
    1. Sample frames from camera.
    2. Save frames into a video file.
"""
import datetime
from threading import Thread
import cv2
import time
import inspect
import ctypes
import argparse

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
        # If you are under windows system using Dshow as backend
        self.stream = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        # If not go next line
        # self.stream = cv2.VideoCapture(src)
        print(self.stream.isOpened())
        self.width = width
        self.height = height
        ret1 = self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        ret2 = self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        ret3 = self.stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        ret4 = self.stream.set(cv2.CAP_PROP_EXPOSURE, -11)
        ret5 = self.stream.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        ret6 = self.stream.set(cv2.CAP_PROP_BRIGHTNESS, 0.0)
        ret7 = self.stream.set(cv2.CAP_PROP_FPS, 120)
        ret8 = self.stream.set(cv2.CAP_PROP_CONTRAST, 0)
        print(ret1, ret2, ret3, ret4, ret5, ret6, ret7, ret8)

        (self.grabbed, self.frame) = self.stream.read()
        self.thread = None
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
        self.flag = False
        self.FPS = FPS_camera()

    def start(self):
        # start the thread to read frames from the video stream

        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        self.FPS = self.FPS.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                break
            self.grabbed, self.frame = self.stream.read()
            if self.grabbed:
                # got a frame
                self.FPS.update()
            else:
                # no frame
                pass

        self.stream.release()
        self.flag = True

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        self.FPS.stop()
        print("[INFO] elasped time: {:.2f}".format(self.FPS.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.FPS.fps()))
        while not self.flag:
            continue
        if self.thread.is_alive():
            _async_raise(self.thread.ident, SystemExit)


class Recoder():

    def __init__(self, savePath='test.avi', show=False, vs=None):
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.writer = cv2.VideoWriter(savePath, self.fourcc, 100.0, (1280, 720), False)
        self.stopped = False
        self.FPS = FPS_camera()
        self.vs = vs
        self.thread = None
        self.show = show
        self.flag = False
        self.process = None

    def recording(self):
        self.FPS = self.FPS.start()
        time_str = str(time.time())
        while True:
            time_iter_start = datetime.datetime.now()
            if self.stopped:
                break
            frame = self.vs.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.writer.write(gray)
            self.FPS.update()

            if self.show:
                cv2.imshow(time_str, gray)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
            time_iter_end = datetime.datetime.now()
            iteration = float((time_iter_end - time_iter_start).microseconds) * 1e-6
            time.sleep(max((0.0075 - iteration), 0))

        self.writer.release()
        self.vs.stream.release()
        cv2.waitKey(1)
        cv2.destroyAllWindows()
        cv2.waitKey(1)

        self.flag = True

    def start(self):
        self.thread = Thread(target=self.recording, args=())
        self.thread.start()
        return self

    def stop(self):

        self.FPS.stop()
        print("[INFO] elasped time: {:.2f}".format(self.FPS.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.FPS.fps()))
        self.stopped = True

        while not self.flag:
            continue
        if self.thread.is_alive():
            _async_raise(self.thread.ident, SystemExit)


def _async_raise(tid, exctype):
    '''Raises an exception in the threads with id tid'''
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid),
                                                     ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def record_main(camera_src, video_path, show=False):
    print("[INFO] sampling THREADED frames from webcam...")
    vs = WebcamVideoStream(src=camera_src).start()
    r = Recoder(savePath=video_path, vs=vs, show=show).start()
    signal=input()
    print(signal)
    vs.stop()
    r.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--c', help='an integer for the camer index', dest='camera_index')
    parser.add_argument('--p', help='a string', dest='video_path')

    args = parser.parse_args()
    camera_index = args.camera_index
    video_path = args.video_path

    record_main(int(camera_index), video_path)



