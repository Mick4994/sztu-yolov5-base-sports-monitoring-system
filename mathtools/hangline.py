import cv2
import numpy as np

NOSE, R_HAND, L_HAND = 0, 9, 10
X,Y = 0, 1

def ReturnHangLine(cv_frame,box,points):
    
    if points[R_HAND][Y] != 0 and points[L_HAND][Y] != 0:
        head_y = points[NOSE][Y]
        # print(head_y)
        # print(points[R_HAND][Y])
        # print(points[L_HAND][Y])
        if head_y != 0 and points[R_HAND][Y] < head_y and points[L_HAND][Y] < head_y: 
            # print('1')
            hand_y = int((points[R_HAND][Y] + points[L_HAND][Y]) / 2)
            hand_l = box[0]
            hand_r = box[2]
            cv_frame = cv_frame[hand_y-20:hand_y,hand_l:hand_r]
            # cv2.imshow('cv_frame',cv_frame)
            cv_frame = cv_frame.copy()
            if len(cv_frame[0]) > 0:
                gray_frame = cv2.cvtColor(cv_frame,cv2.COLOR_BGR2GRAY)
                blur_frame = cv2.GaussianBlur(gray_frame,(3,3),0)
                canny_frame = cv2.Canny(blur_frame, 100 ,100)
                try:
                    lines = cv2.HoughLines(canny_frame, 1, np.pi/2, 40, hand_r-hand_l-20, hand_r-hand_l-5) #取基尔霍夫直线
                except:
                    lines = []
                line_y_list = []
                if lines is not None:
                    for line in lines:
                        if line[0][1] != 0:
                            rho,theta = line[0]
                            a = np.cos(theta)
                            b = np.sin(theta)
                            y0 = b*rho
                            y1 = int(y0 + 1000*(a))
                            y2 = int(y0 - 1000*(a))
                            line_y_list.append( int( (y1 + y2) / 2) )
                    if len(line_y_list) > 0:
                        hangline = int( np.mean(line_y_list) )
                        hangline_repair = hand_y - 20 + hangline
                        return hangline_repair
    return 0

