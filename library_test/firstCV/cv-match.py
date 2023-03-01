import cv2 as cv
import time
import sys
import win32gui
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

use_mask = False
img = None
templ = None
mask = None
image_window = "Source Image"
result_window = "Result window"
match_method = 0
max_Trackbar = 5


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
    return img
    # img.save(window_name + '.bmp')

def qtpixmap_to_cvimg(qtpixmap):

    qimg = qtpixmap.toImage()
    temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
    temp_shape += (4,)
    ptr = qimg.bits()
    ptr.setsize(qimg.byteCount())
    result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
    result = result[..., :3]

    return result


# from PyQt5.QtGui import QImage
# pyqt的截图转换到opencv可以读的格式，这个测试是可用的
def QImageToCvMat(incomingImage):
    '''  Converts a QImage into an opencv MAT format  '''

    incomingImage = incomingImage.convertToFormat(QImage.Format.Format_RGB888)

    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.bits()
    ptr.setsize(height * width * 4)
    arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
    return arr



def main(argv):
    if (len(sys.argv) < 3):
        print('Not enough parameters')
        print('Usage:\nmatch_template_demo.py <image_name> <template_name> [<mask_name>]')
        return -1

    global img
    global templ
    # img = cv.imread(sys.argv[1], cv.IMREAD_COLOR)
    img_src = getScreenshot('d5_1')
    img = QImageToCvMat(img_src)
    templ = cv.imread(sys.argv[2], cv.IMREAD_COLOR)
    if (len(sys.argv) > 3):
        global use_mask
        use_mask = True
        global mask
        mask = cv.imread(sys.argv[3], cv.IMREAD_COLOR)
    if ((img is None) or (templ is None) or (use_mask and (mask is None))):
        print('Can\'t read one of the images')
        return -1

    cv.namedWindow(image_window, cv.WINDOW_AUTOSIZE)
    cv.namedWindow(result_window, cv.WINDOW_AUTOSIZE)

    trackbar_label = 'Method: \n 0: SQDIFF \n 1: SQDIFF NORMED \n 2: TM CCORR \n 3: TM CCORR NORMED \n 4: TM COEFF \n 5: TM COEFF NORMED'
    cv.createTrackbar(trackbar_label, image_window, match_method, max_Trackbar, MatchingMethod)

    MatchingMethod(match_method)

    cv.waitKey(0)
    return 0


def MatchingMethod(param):
    global match_method
    match_method = param

    img_display = img.copy()

    start = time.time()

    method_accepts_mask = (cv.TM_SQDIFF == match_method or match_method == cv.TM_CCORR_NORMED)
    if (use_mask and method_accepts_mask):
        result = cv.matchTemplate(img, templ, match_method, None, mask)
    else:
        result = cv.matchTemplate(img, templ, match_method)

    end = time.time()
    print(end - start)

    cv.normalize(result, result, 0, 1, cv.NORM_MINMAX, -1)

    _minVal, _maxVal, minLoc, maxLoc = cv.minMaxLoc(result, None)

    if (match_method == cv.TM_SQDIFF or match_method == cv.TM_SQDIFF_NORMED):
        matchLoc = minLoc
    else:
        matchLoc = maxLoc

    cv.rectangle(img_display, matchLoc, (matchLoc[0] + templ.shape[0], matchLoc[1] + templ.shape[1]), (0, 0, 200), 2, 8,
                 0)
    cv.rectangle(result, matchLoc, (matchLoc[0] + templ.shape[0], matchLoc[1] + templ.shape[1]), (0, 0, 200), 2, 8, 0)
    cv.imshow(image_window, img_display)
    cv.imshow(result_window, result)

    pass


if __name__ == "__main__":
    main(sys.argv[1:])
