import multiprocessing
import cv2
import datetime
import time
import numpy as np
import threading

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

class camera_driver:
    def __init__(self, src=0, width=1280, height=720):
        self.src = src
        self.width = width
        self.height = height
        self.p = None

    def update(self, eventQ, frameQ):
        cap = cv2.VideoCapture(0)
        print(cap.isOpened())
        ret1 = cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        ret2 = cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        ret3 = cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        ret4 = cap.set(cv2.CAP_PROP_EXPOSURE, -11)
        ret5 = cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        ret6 = cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.0)
        ret7 = cap.set(cv2.CAP_PROP_FPS, 120)
        ret8 = cap.set(cv2.CAP_PROP_CONTRAST, 0)
        print(ret1, ret2, ret3, ret4, ret5, ret6, ret7, ret8)
        time.sleep(0.2)
        fps = FPS_camera()
        fps = fps.start()
        while True:
            if not eventQ.empty():
                if eventQ.get() == 'stop':
                    break
            hello, img = cap.read()
            if hello:
                frameQ.put(img)
                fps.update()
        cap.release()
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        eventQ.put('stopped')

    def start(self, eventQ, frameQ):
        self.p = multiprocessing.Process(target=self.update, args=(eventQ, frameQ))
        self.p.start()

    def stop(self, eventQ):
        eventQ.put('stop')
        time.sleep(0.2)
        while eventQ.empty():
            continue
        self.p.terminate()

class camera_writer:

    def __init__(self, video_path='1.avi', show=False):
        self.p = None
        self.video_path = video_path
        self.show = show

    def update(self, eventQ, frameQ):
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        writer = cv2.VideoWriter(self.video_path, fourcc, 100.0, (1280, 720), False)
        fps = FPS_camera()
        fps = fps.start()
        gray = np.zeros(1)
        #time_iter_start = datetime.datetime.now()
        #last_time_point = time_iter_start

        while True:
            if not eventQ.empty():
                if eventQ.get() == 'stop':
                    break
            if not frameQ.empty():
                gray = cv2.cvtColor(frameQ.get(), cv2.COLOR_BGR2GRAY)


            if len(gray.shape)>1:
                if self.show:
                    cv2.imshow('camera live', gray)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        break

                #time_iter_end = datetime.datetime.now()
                #iteration = float((time_iter_end - last_time_point).microseconds) * 1e-6
                #if iteration >= 0.005:
                writer.write(gray)
                fps.update()
                #last_time_point = time_iter_start


        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        writer.release()
        eventQ.put('stopped')

    def start(self, eventQ, frameQ):
        self.p = multiprocessing.Process(target=self.update, args=(eventQ, frameQ))
        self.p.start()

    def stop(self, eventQ):
        eventQ.put('stop')
        time.sleep(0.2)
        while eventQ.empty():
            continue
        self.p.terminate()

class camera_writer_test:

    def __init__(self, video_path='1.avi', show=False):
        self.p = None
        self.video_path = video_path
        self.show = show

    def update(self, eventQ, frameQ):
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        writer = cv2.VideoWriter(self.video_path, fourcc, 100.0, (1280, 720), False)
        fps = FPS_camera()
        fps = fps.start()
        gray = np.zeros(1)
        #time_iter_start = datetime.datetime.now()
        #last_time_point = time_iter_start

        while True:
            if not eventQ.empty():
                if eventQ.get() == 'stop':
                    break
            if not frameQ.empty():
                gray = cv2.cvtColor(frameQ.get(), cv2.COLOR_BGR2GRAY)


            if len(gray.shape)>1:
                if self.show:
                    cv2.imshow('camera live', gray)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        break

                #time_iter_end = datetime.datetime.now()
                #iteration = float((time_iter_end - last_time_point).microseconds) * 1e-6
                #if iteration >= 0.005:
                writer.write(gray)
                fps.update()
                #last_time_point = time_iter_start


        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        writer.release()
        eventQ.put('stopped')

    def start(self, eventQ, frameQ):
        #self.p = multiprocessing.Process(target=self.update, args=(eventQ, frameQ))
        self.p = threading.Thread(target=self.update, args=(eventQ, frameQ))
        self.p.start()

    def stop(self, eventQ):
        eventQ.put('stop')
        time.sleep(0.2)
        while eventQ.empty():
            continue
        #self.p.terminate()

if __name__ == '__main__':
    '''
    for i in range(10):
        eventQD = multiprocessing.Queue()
        eventQW = multiprocessing.Queue()
        frameQ = multiprocessing.Queue()
        cmd = camera_driver()
        cmw = camera_writer(show=False)
        cmd.start(eventQD, frameQ)
        cmw.start(eventQW, frameQ)
        time.sleep(10)
        cmd.stop(eventQD)
        cmw.stop(eventQW)
        print("free time")
        time.sleep(5)
        eventQD.close()
        eventQW.close()
        frameQ.close()
    '''
    from subprocess import Popen, PIPE
    for i in range(10):
        print("==============starting=================")
        p = Popen(["python", "driver_for_a_better_camera.py", "--c","1", "--p", "1.avi"], stdin=PIPE, stdout=PIPE)
        time.sleep(5)
        p.stdin.write(b"stop\n")
        p.stdin.flush()
        for line in p.stdout.readlines():
            print(line)
        print("==============free time=================")
        time.sleep(10)
