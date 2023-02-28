import sys
import win32gui
from PyQt5.QtWidgets import *
# from PyQt5 import uic

import ui_first


def getScreenshot(window_name):
    hwnd_title = dict()

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    # python学习交流：903971231#

    win32gui.EnumWindows(get_all_hwnd, 0)
    # print(hwnd_title.items())
    for h, t in hwnd_title.items():
        if t != "":
            print(h, t)

    # 程序会打印窗口的hwnd和title，有了title就可以进行截图了。
    hwnd = win32gui.FindWindow(None, window_name)
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    img.save(window_name + '.bmp')


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    #
    # ui = ui_first.Ui_MainWindow()
    # # ui = uic.loadUi("./ui_first.ui")
    # ui.setupUi(MainWindow)
    #
    # MainWindow.show()

    getScreenshot('d5_1')

    # sys.exit(app.exec())
