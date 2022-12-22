import copy
import cv2
import threading
import time
import argparse
import numpy as np
import logging

from KeyPoints_module import Process_keyPoint
from TestPerson import Person
from Visualization import Visualization
from utils.savevideo import SaveRunVideo,AppendFrame
from utils.mylog import log_init, record_start_info

class Process:
    def __init__(self, args:argparse.Namespace, logger:logging.Logger):
        self.data:list[str] = [1, '', '', 1, '', '']
        self.frame:np.uint8 = np.array([])
        
        self.args = args
        self.logger = logger

        self.is_jiaozun = False
        self.mode = args.mode
        self.stop = False
        if self.mode == "引体向上":
            self.up_bound = 50
            self.down_bound = 60
        elif self.mode == "仰卧起坐":
            self.up_bound = 350
            self.down_bound = 400

    def Main(self) -> None:

        keypoint_process = Process_keyPoint(self.args, self.logger)
        main_thread = threading.Thread(target = keypoint_process.main, daemon = True)
        main_thread.start()

        # print('loading yolo')
        self.logger.info("loading yolo")
        while not keypoint_process.state:
            self.logger.warning("Not ready")
            time.sleep(0.5)

        time.sleep(2)
        args = self.args
        frame_gather = []
        frame = self.frame.copy()

        person = Person(self.args, self.up_bound, self.down_bound)

        while 1:
            # 停止监测
            self.stop = True if keypoint_process.stop else False
            # self.logger.warning(f'is_stop:{self.stop}')

            frame:np.ndarray = copy.deepcopy(keypoint_process.frame) #从帧抓取线程中取尾帧
            points:list = copy.deepcopy(keypoint_process.poses[0]) if len(keypoint_process.poses) > 0 else []
            box = copy.deepcopy(keypoint_process.bboxes[0]) if len(keypoint_process.bboxes) > 0 else []
            
            box = [int(i) for i in box]

            if frame is None or len(frame) == 0:
                if args.save:
                    if len(frame_gather) > 50:
                        SaveRunVideo(frame_gather=frame_gather)
                time.sleep(1)
                # print('None Frame')
                self.logger.error("None Frame!")
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

    # ============================ 参数初始化 ================================ #
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--source",default='C:/FFOutput/5s.mp4')
    # source_list
    "机械盘:/FFOutput/5.mp4"
    "rtmp://120.78.203.51:1034/live/jetson"
    "机械盘:/FFOutput/now.mp4"
    "6 #:for HIK"
    "仰卧起坐.mp4"
    parser.add_argument("-r","--save", default=False)
    parser.add_argument("-m","--mode", default="引体向上", help="仰卧起坐")
    parser.add_argument("-l","--loglevel", default=logging.INFO, help="DEBUG, INFO, WARNING, ERROR")
    args = parser.parse_args()
    # ============================ 参数初始化 ================================ #

    # ===================== 日志系统初始化 ===================== #
    logger = log_init()
    args_dict = vars(args)
    record_start_info(args_dict, logger)
    # ===================== 日志系统初始化 ===================== #

    # ============== 主程序初始化 ============== #
    process = Process(args, logger)
    # ============== 主程序初始化 ============== #

    thread_main = threading.Thread(target=process.Main,daemon=True)
    thread_main.start()

    while thread_main.is_alive() and not process.stop:
        logger.info(f"process.data:{process.data[:3]}")
        time.sleep(1)
    else:
        logger.warning("Thread Died and Exit MainThread!")
        exit(0)

