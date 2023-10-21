import sys
import cv2 as cv
import numpy as np


def mouse_event(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # print(str(event) + ',' + str(x) + ',' + str(y) + ',' + str(flags) + ',' + str(param))
        print('left down')
        # cv.circle(img, (x, y), 10, (0, 100, 200), -1)
    elif event == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_LBUTTON:
        print('drawing')
        # img
        # img[x][y] = img_ori[x][y]
        pass
    elif event == cv.EVENT_LBUTTONUP:
        print('left up')
        for i in range(x - 2, x + 3):
            for j in range(y - 2, y + 3):
                cv.rectangle(img, (i, j), (i, j), (int(img_ori[j][i][0]), int(img_ori[j][i][1]), int(img_ori[j][i][2])),
                             -1)
                cv.rectangle(img_out, (i, j), (i, j), (255, 255, 255), -1)
                cv.imwrite('out.png', img_out)
        # cv.rectangle(img, (x - 1, y - 1), (x + 1, y + 1), (0, 100, 200), -1)
    pass


# 修改图像的亮度，brightness取值0～2 <1表示变暗 >1表示变亮
def change_brightness(img, brightness):
    dst = np.zeros(img.shape, img.dtype)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            (b, g, r) = img[i, j]
            bb = int(b) / brightness
            gg = int(g) / brightness
            rr = int(r) / brightness
            if bb < 0:
                bb = 0
            if gg < 0:
                gg = 0
            if rr < 0:
                rr = 0
            dst[i, j] = (bb, gg, rr)
    return dst


img_ori = cv.imread("d5_big.bmp")
# img = cv.copy(img_ori)
img = np.copy(img_ori)
img_out = np.zeros(img_ori.shape, img_ori.dtype)
# img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
img = change_brightness(img, 3)
# img = np.random.random(img_ori.shape)
cv.namedWindow('image')
cv.setMouseCallback('image', mouse_event)
cv.imshow('image-ori', img_ori)
while 1:
    cv.waitKey(1)
    cv.imshow('image', img)
