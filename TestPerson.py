import numpy as np
from mathtools.hangline import ReturnHangLine
from mathtools.counter import ReturnCount

# Body Key Points Value
NOSE, R_HAND, L_HAND = 0, 9, 10

X,Y,C = 0, 1, 2

HARD, EASY = 5, 2

# 被测者对象
class Person:
    def __init__(self):
        self.head_list:list[int] = [0]                              # 头部y位置，                     类型： 一维列表
        self.box:list[int,int,int,int] = []            # 被测者所在的位置框，             类型：一维四位列表【左上角x，y,右下角x，y】
        
        self.linelist:list[int] = [0]                               # 比较线的y位置，                 类型：一维列表

        self.status:int = 1                                         # 被测者状态，0为未就绪，1为就绪   类型：整数（布尔）
        self.name:str = '1'                                         # 被测者姓名                     类型：字符串
        self.count:int = 0                                          # 被测者过线计数                 类型：整数

        self.frame:np.uint8 = []                                    # 被测者存在的画面               类型：三维numpy.uint8数组 Eg:720P RGB:（1280, 720, 3） 
        self.is_count:bool = False                                  # 是否符合计数条件               类型：布尔型

    # -----------------获取当前被测者状态（对比线是否位于正常状态）的算法-----------------
    def getstatus(self,points):
        if self.linelist[-1] != 0 and self.status == 0 and self.name!=' ':
            if points[R_HAND][C] != 0 and points[L_HAND][C] != 0 and points[NOSE][C] != 0:
                if points[R_HAND][Y] < points[NOSE][Y] and points[L_HAND][Y] < points[NOSE][Y]:
                    self.status = 1
        if self.linelist[-1] != 0 and self.status == 1:
            if points[R_HAND][C] != 0 and points[L_HAND][C] != 0:
                if abs(points[R_HAND][Y]-self.linelist[-1]) > 30 or abs(points[L_HAND][Y]-self.linelist[-1]) > 30:
                    self.status = 0
                    self.count = 0
                    self.name = 'unnamed'
    # -----------------获取当前被测者状态（对比线是否位于正常状态）的算法-----------------

    # -----------------获取比较线的算法-----------------  可行度（1~5）：3
    def getline(self,frame,points):
        if len(self.box) > 0:
            if len(self.linelist) > 30:
                # 比较最后一位与从后往前数前 18 位的差值小于5的数不少于2 且最后一位不为0（置信度达标即不为 0）
                if len([self.linelist[-i] for i in range(2,20) if abs(self.linelist[-i] - self.linelist[-1])<5 ] ) >= 2 and self.linelist[-1]!=0:
                    pass
                else:
                    self.linelist.append(ReturnHangLine(frame,self.box,points))
            else:
                # 长度小于 30 直接添加
                self.linelist.append(ReturnHangLine(frame,self.box,points))
    # -----------------获取比较线的算法-----------------

    def getframe(self,frame):
        self.frame = frame

    def getcount(self):
        if self.name != 'unnamed':
            self.count,self.is_count = ReturnCount(self.count,self.head_list,self.is_count,self.linelist[-1])

    def main(self,points, frame, box):
        self.box = box
        if len(points) != 0:
            head = points[NOSE][Y]
            self.head_list.append(head)

            self.getline(frame,points)
            self.getstatus(points)
            self.getcount()