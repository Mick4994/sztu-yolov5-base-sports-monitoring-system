import copy
import cv2
import threading
import time
import argparse
import numpy as np

from KeyPoints_module import Process_keyPoint
from TestPerson import Person
from Visualization import Visualization
from utils.savevideo import SaveRunVideo,AppendFrame

class Process:
    def __init__(self, args:argparse.Namespace):
        self.data:list[str] = [1, '', '', 1, '', '']
        self.frame:np.uint8 = np.array([])
        self.args = args
        self.is_jiaozun = False
        self.mode = args.mode
        if self.mode == "引体向上":
            self.up_bound = 50
            self.down_bound = 60
        elif self.mode == "仰卧起坐":
            self.up_bound = 350
            self.down_bound = 400

    def Main(self) -> None:

        keypoint_process = Process_keyPoint(self.args)
        main_thread = threading.Thread(target = keypoint_process.main, daemon = True)
        main_thread.start()

        print('loading yolo')
        while not keypoint_process.state:
            time.sleep(0.1)

        time.sleep(2)
        args = self.args
        frame_gather = []
        frame = self.frame.copy()

        person = Person(self.args, self.up_bound, self.down_bound)

        while 1:
            frame:np.ndarray = copy.deepcopy(keypoint_process.frame) #从帧抓取线程中取尾帧
            points:list = copy.deepcopy(keypoint_process.poses[0]) if len(keypoint_process.poses) > 0 else []
            box = copy.deepcopy(keypoint_process.bboxes[0]) if len(keypoint_process.bboxes) > 0 else []
            
            box = [int(i) for i in box]

            if frame is None or len(frame) == 0:
                if args.save:
                    if len(frame_gather) > 50:
                        SaveRunVideo(frame_gather=frame_gather)
                time.sleep(1)
                print('None Frame')
                break

            #数据处理部分
            cv_frame = frame.copy()
            #算法部分
            person.main(points, cv_frame, box)

            #可视化部分
            visualization = Visualization(person, self.up_bound, self.down_bound)
            frame = visualization.ReturnVisualFrame(frame, points, self.is_jiaozun)
            #更新数据
            self.data = visualization.data

            cv2.imshow('frame',frame)
            frame_gather = AppendFrame(frame=frame,frame_gather=frame_gather)
            if len(frame_gather) > 500:
                frame_gather = []
            else:
                if args.save :
                    t = threading.Thread(target = SaveRunVideo)
                    t.start()
                    frame_gather = []
            key = cv2.waitKey(10)
            if key == ord('b'): #按b退出
                cv2.destroyAllWindows()
                if args.save and len(frame_gather) > 500:
                    SaveRunVideo(frame_gather=frame_gather)
                break
            elif key == ord('z'):
                self.is_jiaozun = True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--source",default=0)
    # source_list
    "C:/FFOutput/5.mp4"
    "rtmp://120.78.203.51:1034/live/jetson"
    "D:/FFOutput/now.mp4"
    "6 #:for HIK"
    "仰卧起坐.mp4"
    parser.add_argument("-r","--save", default=False)
    parser.add_argument("-m","--mode", default="引体向上", help="仰卧起坐")
    args = parser.parse_args()
    process = Process(args)
    thread_main = threading.Thread(target=process.Main,daemon=True)
    thread_main.start()
    last_time = time.time()
    while thread_main.is_alive():
        print(process.data[:3])
        time.sleep(1)
        if last_time - time.time() > 1:
            process.data = [0, '', '', 0, '', '']
    else:
        print('Thread Died')

