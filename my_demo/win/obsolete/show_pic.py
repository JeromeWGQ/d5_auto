import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os

import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class Qt_Window(QWidget):
    def __init__(self):
        self._app = QtWidgets.QApplication([])
        super(Qt_Window, self).__init__()
        self.setGeometry(30, 30, 600, 400)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        br = QtGui.QBrush(QtGui.QColor(50, 10, 200, 100))
        qp.setBrush(br)
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()

    def init_ui(self):
        self.win = QMainWindow()

        self.comboBox = QComboBox(self.win)
        self.number_lable = QLabel(self.win)
        self.open_Button = QPushButton(self.win)
        self.detect_image = QLabel(self.win)

        # 设置路径
        self.path = ("./")

        self.comboBox.resize(200, 50)
        self.comboBox.move(600, 800)
        self.img_list = os.listdir(self.path)
        self.comboBox.addItems([self.img_list[i] for i in range(len(self.img_list))])
        self.comboBox.activated.connect(self.show_img)

        self.open_Button.resize(200, 50)
        self.open_Button.move(1000, 800)
        self.open_Button.setText("退出")
        self.open_Button.clicked.connect(self.exit)

        self.detect_image.resize(700, 550)
        self.detect_image.move(550, 100)

        self.number_lable.resize(200, 50)
        self.number_lable.move(900, 700)

        self.win.showFullScreen()
        sys.exit(self._app.exec_())

    def show_img(self):
        img = self.comboBox.currentText()
        pix = QPixmap(self.path + "/" + img)
        self.detect_image.setPixmap(pix)
        self.detect_image.setScaledContents(True)
        lable = img.split(".")[0]
        self.number_lable.setText(lable)

    def exit(self):
        while True:
            sys.exit(0)


s = Qt_Window()
s.init_ui()
s.aboutToQuit.connect(s.deleteLater)
sys.exit(s.exec_())
