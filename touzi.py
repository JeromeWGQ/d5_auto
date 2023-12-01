import os
import random
import sys
import time

import win32gui
import win32con
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
import pyautogui

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

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)

    return img, left, top


def compare_pic(shot, pic_name, x, y):
    return shot.pixelColor(x, y) == image_dict[pic_name].pixelColor(x, y)


def compare_pic_buffer(shot, pic_name, x, y):
    buffer = 3
    rgb1 = shot.pixelColor(x, y).getRgb()
    rgb2 = image_dict[pic_name].pixelColor(x, y).getRgb()
    diff_r = rgb1[0] - rgb2[0]
    diff_g = rgb1[1] - rgb2[1]
    diff_b = rgb1[2] - rgb2[2]
    return -buffer < diff_r < buffer and -buffer < diff_g < buffer and -buffer < diff_b < buffer


def click_window(left, top, x, y):
    pyautogui.click(left + x, top + y)


def judge_scene(window_name):
    shot, left, top = get_screenshot(window_name)
    if (compare_pic(shot, 'touzi-first', 309, 344)
            and compare_pic(shot, 'touzi-first', 338, 359)):
        print('---> 扔骰子')
        pyautogui.press('P')
    elif (compare_pic_buffer(shot, 'touzi-box', 193, 162)
            and compare_pic_buffer(shot, 'touzi-box', 228, 168)):
        print('---> 弹窗了')
        click_window(left, top, 310, 345)
    elif (compare_pic(shot, 'touzi-confirm', 285, 348)
          and compare_pic(shot, 'touzi-confirm', 354, 362)):
        print('---> 确认记录')
        click_window(left, top, 300, 350)
    else:
        print('未知场景')
    print()


if __name__ == '__main__':
    image_dict = load_pic()
    print('===== 图片模板加载完成 =====\n')
    while True:
        judge_scene(win_target)
        time.sleep(5)
