import cv2
import numpy as np

# 按下鼠标时为True
drawing = False
# 当mode为true时绘制矩形，按下m后mode变成false，用来绘制曲线
mode = True
ix, iy = -1, -1


# 设置回调函数
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode
    # 当单击时返回起始位置坐标
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    # 当移动鼠标时绘制图形，event可以查看移动效果，flag检测是否发生单击
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        # if drawing:
        #     if mode:
        #         cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
        #     else:
        #         # 绘制圆圈，圆点连成线，3代表笔的粗细
        #         cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
        pass
    # 当松开鼠标时停止绘制
    elif event == cv2.EVENT_LBUTTONUP:
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0, 100), -1)
        drawing = False


# 创建图像与窗口并将窗口与回调函数进行绑定
img = cv2.imread("sky-big.png")
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)
while 1:
    cv2.imshow('image', img)
    k = cv2.waitKey(1)
    if k == ord('m'):
        mode = not mode
    elif k == ord('q'):
        break
    elif k == ord('r'):
        img = np.zeros((500, 500, 3), np.uint8)
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', draw_circle)
cv2.destroyAllWindows()
