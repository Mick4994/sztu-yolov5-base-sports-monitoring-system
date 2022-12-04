import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def cv2AddChineseText(img, text, position, textColor=(0, 255, 0), textSize=30):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "TextType/HarmonyOS_Sans_SC_Regular.ttf", textSize, encoding="utf-8")
    # 绘制文本
    draw.text(position, text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

def jiaozun():
    cap = cv2.VideoCapture("一分钟仰卧起坐.mp4")
    up_bound, down_bound = 350, 400
    jiaozun_str = "请校准杆线到指定位置，然后按下z确认"
    is_jiaozun = False
    img3 = np.full((down_bound - up_bound ,1920,3), 50, dtype = np.uint8)
    while 1:
        _, img = cap.read()
        if len(img) != 0:
            if not is_jiaozun:
                img = cv2AddChineseText(img, jiaozun_str, (20, up_bound - 100),(255, 255, 255), 40)
            img[up_bound:down_bound,:] += img3
            cv2.imshow('img',img)
            key = cv2.waitKey(30)
            if key == ord('b'):
                cv2.destroyAllWindows()
                break
            elif key == ord('z'):
                is_jiaozun = True

if __name__ == "__main__":
    jiaozun()
