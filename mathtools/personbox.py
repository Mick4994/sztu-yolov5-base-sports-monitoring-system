import cv2

def ReturnBox(points):
    max_hight = min([points[i][1] for i in range(len(points)) if points[i][1] != 0])
    min_hight = max([points[i][1] for i in range(len(points)) if points[i][1] != 0])
    right = min([points[i][0] for i in range(len(points)) if points[i][0] != 0])
    left = max([points[i][0] for i in range(len(points)) if points[i][0] != 0])
    n_left = int(left - 0.3*(right - left)/2)
    n_right = int(right + 0.3*(right - left)/2)
    n_max = int(max_hight-0.2*(min_hight - max_hight)/2)
    n_min = int(min_hight+0.2*(min_hight - max_hight)/2)
    return [[n_left,n_max],[n_right,n_min]]

def DrawBox(box_list,frame):
    for (x1,y1),(x2,y2) in box_list:
        cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
    return frame

def ReturnCutFrame(box_list,frame):
    cv_frame_gather = []
    for (x1,y1),(x2,y2) in box_list:
        cv_frame = frame[y1:y2,x1:x2]
        cv_frame = cv_frame.copy()
        cv_frame_gather.append(cv_frame)
    return cv_frame_gather
