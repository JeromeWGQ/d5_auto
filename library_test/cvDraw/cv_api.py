import sys
import time

import cv2 as cv


global image


def mouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        img1 = image.copy()
        xy = "(%d,%d)" % (x, y)  # 设置坐标显示格式
        cv.circle(img1, (x, y), 1, (0, 255, 0), thickness=-1)
        cv.putText(img1, xy, (x+10, y-10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), thickness=1)
        cv.imshow("image", img1)  # 显示坐标


if __name__ == "__main__":
    image = cv.imread("sky-big.png")
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    cv.rectangle(image, (100, 100), (110, 110), (0, 200, 10), 2, 8, 0)

    a = 120
    while True:
        start = time.time()

        # cv.rectangle(image, (100, 100), (a, 140), (0, 0, 200), 2, 8, 0)
        cv.setMouseCallback("image", mouse)

        cv.imshow('image_window', image)
        cv.waitKey(0)
        print(time.time() - start)
        a += 1
        break

    pass
