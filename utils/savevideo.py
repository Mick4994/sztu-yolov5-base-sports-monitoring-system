import cv2
import os
import time
import numpy as np

def SaveRunVideo(cap = None, frame_gather = []):
    print('Saving Run Video Now:',len(frame_gather))
    if cap != None:
        weight = int(cap.get(3))
        hight = int(cap.get(4))
        fps = int(cap.get(5))
    else:
        weight = 1280
        hight = 720
        fps = 30
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_name = time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))
    video_name = my_save_path+video_name+'_res.mp4'
    my_save_path = './res/'
    out = cv2.VideoWriter(video_name, fourcc, fps, (weight,hight), True )
    print('save:',len(frame_gather))
    for frame in frame_gather:
        out.write(frame)
    if os.path.getsize(video_name) < 1024:
        print("fail encode video")
        np.save(my_save_path+'frame_gather.npy',np.array(frame_gather))
    print('save finished')

def AppendFrame(frame,frame_gather):
    if len(frame_gather) > 1:
        if frame is not None and frame.shape == frame_gather[-1].shape:
            # print(frame.shape)
            frame_gather.append(frame)
    else:
        if frame is not None:
            # print(frame.shape)
            frame_gather.append(frame)
    return frame_gather