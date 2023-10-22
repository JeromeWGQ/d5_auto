import os
import sys
import time

import win32gui
import win32con
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage

# 雷电模拟器    640 * 360    160 ppi
win_target = 'd5-1'


def load_pic():
    pics = os.listdir('./pic/')
    res = dict()
    for pic in pics:
        pure_name = pic.split('.png')[0]
        print(pure_name)
        res[pure_name] = QImage('./pic/' + pic)
    return res


def get_screenshot(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    win32gui.SetForegroundWindow(hwnd)

    time.sleep(0.001)
    img = screen.grabWindow(hwnd).toImage()
    return img


def compare_pic(window_name, pic_name, x, y):
    return get_screenshot(window_name).pixelColor(x, y) == image_dict[pic_name].pixelColor(x, y)


def judge_scene(window_name):
    if (compare_pic(window_name, 'gaming', 58, 39)
            and compare_pic(window_name, 'gaming', 62, 41)
            and compare_pic(window_name, 'gaming', 429, 349)
            and compare_pic(window_name, 'gaming', 436, 366)):
        print('游戏中')
    else:
        print('未知场景')


if __name__ == '__main__':
    image_dict = load_pic()
    print('===== 图片模板加载完成 =====\n')
    judge_scene(win_target)
