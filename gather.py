import sys
import time

import win32gui
import win32con
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

# 雷电模拟器    640 * 360    160 ppi
gather_target = 'd5-1'
# gather_target = '雷电多开器'
# gather_target = 'd5_auto – gather.py'


def get_screenshot(window_name):
    hwnd_title = dict()

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    print(hwnd_title.items())
    # for h, t in hwnd_title.items():
    #     if t != "":
    #         print(h, t)
    # 程序会打印窗口的hwnd和title，有了title就可以进行截图了。
    hwnd = win32gui.FindWindow(None, window_name)
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    # 设置前台显示
    win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    win32gui.SetForegroundWindow(hwnd)

    time.sleep(0.01)
    img = screen.grabWindow(hwnd).toImage()
    pic_name = input('截屏已完成，请输入场景名称：')
    img.save('pic/' + pic_name + '.png')
    return pic_name


# file_handle = open('pos.txt', mode='a')
# pic_name = ''
# import pymysql
#
# cursor = None
#
# try:
#     db = pymysql.connect(host='localhost', user='root', passwd='123456', port=3306, db='d5_auto')
#     cursor = db.cursor()
#     print('连接成功！')
# except pymysql.Error as e:
#     print(e)


class MyQLabel(QLabel):
    def __init__(self):
        super().__init__()

    # 重写鼠标单击事件
    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        print(int(x / 3 + 0.5), int(y / 3 + 0.5))
        # cursor.execute('insert into scene_pos values {},{},{}'.format('win1', x, y))
        # global file_handle, pic_name
        # file_handle.write('111' + '\n')
        # text = pic_name + '\t' + x + '\t' + y + '\n'
        # print(text)
        # file_handle.write(text + '\n')


def get_key_point(pic_name):
    app = QApplication([])
    file_path = 'pic/' + pic_name + '.png'
    pixmap = QPixmap(file_path)
    label = MyQLabel()
    label.setWindowTitle("请点击关键点")
    rate = 3
    label.setPixmap(pixmap.scaled(pixmap.width() * rate, pixmap.height() * rate))
    label.resize(pixmap.width() * rate, pixmap.height() * rate)
    label.show()
    sys.exit(app.exec())


def gather(window_name):
    print('gather ' + window_name)
    pic_name = get_screenshot(window_name)
    time.sleep(0.3)
    get_key_point(pic_name)


if __name__ == '__main__':
    gather(gather_target)
