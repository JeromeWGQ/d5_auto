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
    return img


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


def judge_scene(window_name):
    shot = get_screenshot(window_name)
    if (compare_pic(shot, 'gaming', 58, 39)
            and compare_pic(shot, 'gaming', 62, 41)
            and compare_pic(shot, 'gaming', 429, 349)
            and compare_pic(shot, 'gaming', 436, 366)):
        print('游戏中')
        is_hear = False
        is_l1 = False
        is_l2 = False
        is_throw1 = False
        is_throw2 = False
        is_1_still = False
        is_2_still = False
        is_1_fire = False
        is_2_fire = False
        if (compare_pic(shot, 'gaming', 579, 188)
                and compare_pic(shot, 'gaming', 578, 203)):
            print('聆听已充能')
            is_hear = True
        if (compare_pic(shot, 'gaming', 476, 115)
                and compare_pic(shot, 'gaming', 481, 119)):
            print('开一阶了')
            is_l1 = True
        if (compare_pic(shot, 'gaming-level2', 609, 118)
                and compare_pic(shot, 'gaming-level2', 612, 114)):
            print('开二阶了')
            is_l2 = True
        if (compare_pic_buffer(shot, 'gaming-level2', 519, 259)
                and compare_pic_buffer(shot, 'gaming-level2', 531, 265)):
            print('娃1可以扔')
            is_throw1 = True
        if (compare_pic_buffer(shot, 'gaming-level2', 575, 246)
                and compare_pic_buffer(shot, 'gaming-level2', 585, 252)):
            print('娃2可以扔')
            is_throw2 = True
        if (compare_pic_buffer(shot, 'gaming-transfer', 516, 269)
                and compare_pic_buffer(shot, 'gaming-transfer', 528, 265)):
            print('娃1静止可传')
            is_1_still = True
        if (compare_pic_buffer(shot, 'gaming-transfer', 572, 260)
                and compare_pic_buffer(shot, 'gaming-transfer', 584, 255)):
            print('娃2静止可传')
            is_2_still = True
        if compare_pic_buffer(shot, 'gaming-fire', 525, 284):
            print('娃1带火')
            is_1_fire = True
        if compare_pic_buffer(shot, 'gaming-fire', 580, 274):
            print('娃2带火')
            is_2_fire = True
        # if (compare_pic_buffer(shot, 'gaming-find1', 529, 270)
        #         or compare_pic_buffer(shot, 'gaming-find2', 528, 270)
        #         or compare_pic_buffer(shot, 'gaming-find3', 529, 270)
        #         or compare_pic_buffer(shot, 'gaming-find4', 528, 269)):
        #     print('娃1发现目标')
        # if (compare_pic_buffer(shot, 'gaming-find1', 583, 583)
        #         or compare_pic_buffer(shot, 'gaming-find2', 583, 260)
        #         or compare_pic_buffer(shot, 'gaming-find3', 583, 259)
        #         or compare_pic_buffer(shot, 'gaming-find4', 583, 259)):
        #     print('娃2发现目标')

        # is_hear = False
        # is_l1 = False
        # is_l2 = False
        # is_throw1 = False
        # is_throw2 = False
        # is_1_still = False
        # is_2_still = False
        # is_1_fire = False
        # is_2_fire = False

        # 开始逻辑判断
        if is_l2:
            if random.random() < 0.45:
                if is_throw1:
                    print('---> 扔出娃1')
                    pyautogui.press('num1')
                elif is_1_fire:
                    print('---> 娃1找人中')
                    pyautogui.press('num5')
                elif random.random() < 0.2:
                    print('---> 给娃1传火')
                    pyautogui.press('num7')
                else:
                    if is_1_still:
                        print('---> 目标可能在附近，传娃1刷刀')
                        pyautogui.press('num3')
                    elif is_2_still:
                        print('---> 目标可能在附近，传娃2刷刀')
                        pyautogui.press('num4')
                    else:
                        print('---> 两娃都在CD')
                        if is_hear and random.random() < 0.3:
                            pyautogui.press('num6')
                        else:
                            pyautogui.press('num5')
                    time.sleep(3)
            elif random.random() < 0.9:
                if is_throw2:
                    print('---> 扔出娃2')
                    pyautogui.press('num2')
                elif is_2_fire:
                    print('---> 娃2找人中')
                    pyautogui.press('num5')
                elif random.random() < 0.2:
                    print('---> 给娃2传火')
                    pyautogui.press('num8')
                else:
                    if is_1_still:
                        print('---> 目标可能在附近，传娃1刷刀')
                        pyautogui.press('num3')
                    elif is_2_still:
                        print('---> 目标可能在附近，传娃2刷刀')
                        pyautogui.press('num4')
                    else:
                        print('---> 两娃都在CD')
                        if is_hear and random.random() < 0.3:
                            pyautogui.press('num6')
                        else:
                            pyautogui.press('num5')
                    time.sleep(3)
            else:
                print('---> 开始聆听')
                pyautogui.press('num6')
        elif is_l1:
            if random.random() < 0.8:
                if is_throw1:
                    print('---> 扔出娃1')
                    pyautogui.press('num1')
                elif is_1_fire:
                    print('---> 娃1找人中')
                    pyautogui.press('num5')
                elif random.random() < 0.2:
                    print('---> 给娃1传火')
                    pyautogui.press('num7')
                else:
                    if is_1_still:
                        print('---> 目标可能在附近，传娃1刷刀')
                        pyautogui.press('num3')
                    else:
                        print('---> 娃在CD')
                        if is_hear and random.random() < 0.3:
                            pyautogui.press('num6')
                        else:
                            pyautogui.press('num5')
                    time.sleep(3)
            else:
                print('---> 开始聆听')
                pyautogui.press('num6')
        elif is_hear:
            print('---> 开始聆听')
            pyautogui.press('num6')
        else:
            print('---> 才刚开局')
            pyautogui.press('num5')
    elif (compare_pic(shot, 'scene-main', 575, 280)
          and compare_pic(shot, 'scene-main', 592, 295)
          and compare_pic(shot, 'scene-main', 575, 337)
          and compare_pic(shot, 'scene-main', 581, 364)):
        if (compare_pic(shot, 'scene-main-matching', 37, 139)
                and compare_pic(shot, 'scene-main-matching', 105, 221)):
            print('---> 等待匹配')
        else:
            print('---> 主菜单，进入匹配')
            pyautogui.press('\\')
        time.sleep(5)
    elif (compare_pic(shot, 'scene-common-box', 284, 345)
          and compare_pic(shot, 'scene-common-box', 363, 364)):
        print('---> 确认框')
    elif (compare_pic(shot, 'scene-matched', 293, 322)
          and compare_pic(shot, 'scene-matched', 344, 322)):
        print('---> 排到人了')
    elif (compare_pic(shot, 'scene-prepare', 469, 356)
          and compare_pic(shot, 'scene-prepare', 556, 354)
          and compare_pic(shot, 'scene-prepare', 552, 365)):
        print('---> 没点准备')
    elif (compare_pic(shot, 'scene-finish', 284, 357)
          and compare_pic(shot, 'scene-finish', 356, 372)):
        print('---> 结算界面')
    else:
        print('未知场景')
    print()


if __name__ == '__main__':
    image_dict = load_pic()
    print('===== 图片模板加载完成 =====\n')
    while True:
        judge_scene(win_target)
        time.sleep(5)
