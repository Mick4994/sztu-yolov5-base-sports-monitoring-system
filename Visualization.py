import cv2
import numpy as np
from TestPerson import Person

#可视化参数
class Visualization:
    def __init__(self, person : Person):
        #左侧测试员信息
        self.box = person.box
        self.line = person.linelist[-1]
        self.status = person.status
        self.name = person.name
        self.count = str(person.count)
        #传输信息
        self.data = [str(self.status),self.name,self.count,'0','unname','0']
        
    def ReturnVisualFrame(self,frame, points) -> np.uint8: #返回带可视化参数的画面
        box =self.box
        line = self.line
        name = self.name
        count = self.count

        if len(box)!= 0:
            cv2.rectangle(frame,(box[0],box[1]),(box[2],box[3]),(255,0,0),2) #画人物范围框
            if line != 0:
                cv2.line(frame,(box[0],line),(box[2],line),(0,0,255),2) #画杆线
                cv2.putText(frame,'name:'+name,(box[2],box[3]+14),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),2) #在框下标姓名
                cv2.putText(frame,'count:'+count,(box[2],box[3]+30),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),2)
        for x, y, c in points:
            # if c != 0:
                cv2.circle(frame, (int(x), int(y)),3,(0,255,0),cv2.FILLED)
                # cv2.putText(frame,'{:.8f}'.format(c),(int(x), int(y)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),2)

        frame = cv2.resize(frame,(1366,768))
        return frame

