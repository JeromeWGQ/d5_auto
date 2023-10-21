# https://blog.csdn.net/qq_57703870/article/details/128673658

import datetime
import os
import os.path
import random
import sys
from datetime import datetime
from io import BytesIO
import pyautogui
import win32clipboard
from PIL import Image
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QObject, pyqtSignal, QRect, Qt
from PyQt5.QtGui import QIcon, QPainter, QPen
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QMenu
from system_hotkey import SystemHotkey


class MyWindow(QWidget, QObject):
    # 定义一个热键信号
    sig_keyhot = pyqtSignal(str)

    def __init__(self):
        # 创建窗口并且隐藏
        super().__init__()
        self.setWindowTitle('截屏工具')
        self.setWindowIcon(QIcon(":/vi.ico"))
        self.hide()

        # 记录鼠标的初始坐标和结束坐标
        self.x0, self.x1, self.y0, self.y1 = 0, 0, 0, 0
        # 鼠标是否松开
        self.flag = False
        self.pixmap = None
        # 保存文件的地址
        self.file_path = "~/Documents/Screen"
        self.lbl = QLabel(self)

        # 系统托盘
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(QIcon("vi.ico"))
        tray_menu = QMenu()
        exit_action = tray_menu.addAction("退出")
        exit_action.triggered.connect(self.Exit)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip('Ctrl+Q截屏')
        self.tray_icon.setVisible(True)
        # 全局热键，电脑任何地方开始截图
        self.sig_keyhot.connect(self.MKey_pressEvent)
        self.hk_shot = SystemHotkey()
        self.hk_shot.register(('control', 'q'), callback=lambda x: self.send_key_event("shot"))
        # 局部热键，只能在窗口范围内使用
        QtWidgets.QShortcut(QtGui.QKeySequence('Esc', ), self, self.chanls)
        QtWidgets.QShortcut(QtGui.QKeySequence(self.tr("S")), self, self.crop)

    # 将图片放到剪切版
    def paste_img(self, file_img):
        image = Image.open(file_img)
        output = BytesIO()
        image.save(output, 'BMP')
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    def Exit(self):
        # 点击关闭按钮或者点击退出事件会出现图标无法消失的bug，需要手动将图标内存清除
        self.tray_icon = None
        sys.exit(app.exec_())

    # 生成随机文件名
    def generate_random_filename(self):
        # 获取用户的文档文件夹路径
        documents_path = os.path.expanduser(self.file_path)
        if os.path.exists(documents_path) is False:
            os.mkdir(documents_path)
        # 生成一个随机整数
        random_int = random.randint(1, 10000)
        # 生成一个随机文件名
        random_filename = f"screenshot_{random_int}.png"

        # 检查文件是否存在，如果存在，则重新生成一个随机文件名
        while os.path.exists(random_filename):
            random_int = random.randint(1, 10000)
            now = datetime.now()
            random_filename = f"screenshot_{random_int}_{now.strftime('%Y%m%d%H%M%S')}.png"
        # 构造文件的完整路径
        file_path = os.path.join(documents_path, random_filename)

        return file_path

    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()

    def mouseReleaseEvent(self, event):
        self.flag = False

    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event):
        try:
            super().paintEvent(event)
            if self.flag:
                rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
                self.pixmap = QPixmap(self.file_path)
                painter = QPainter(self.pixmap)
                painter.setPen(QPen(Qt.blue, 1, Qt.SolidLine))
                painter.drawRect(rect)
                self.lbl.setPixmap(self.pixmap)
        except Exception as e:
            print("Error:", e)

    def crop(self):
        try:
            if self.flag is False and self.x0 != self.x1:
                box = (self.x0, self.y0, self.x1, self.y1)
                self.hide()
                img = Image.open(self.file_path)
                img = img.crop(box)
                os.remove(self.file_path)
                img.save(self.file_path)
            else:
                self.hide()
            self.paste_img(self.file_path)
        except Exception as e:
            print("Error:", e)

    def chanls(self):
        self.hide()
        os.remove(self.file_path)

    def MKey_pressEvent(self):
        self.x0, self.x1, self.y0, self.y1 = 0, 0, 0, 0
        self.file_path = self.generate_random_filename()
        img = pyautogui.screenshot()
        img.save(self.file_path)
        self.pixmap = QPixmap(self.file_path)  # 按指定路径找到图片
        self.lbl.setPixmap(self.pixmap)  # 在label上显示图片
        self.lbl.setScaledContents(True)  # 让图片自适应label大小
        self.showFullScreen()

    def send_key_event(self, i_str):
        self.sig_keyhot.emit(i_str)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    app.exec_()
