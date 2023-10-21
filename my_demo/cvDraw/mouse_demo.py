import cv2


def mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        img1 = img.copy()
        xy = "(%d,%d)" % (x, y)  # 设置坐标显示格式
        cv2.circle(img1, (x, y), 1, (0, 255, 0), thickness=-1)
        cv2.putText(img1, xy, (x + 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), thickness=1)
        cv2.imshow("image", img1)  # 显示坐标


#按下鼠标时为True
drawing = False
#当mode为true时绘制矩形，按下m后mode变成false，用来绘制曲线
mode = True
ix,iy=-1,-1
#设置回调函数
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode
    #当单击时返回起始位置坐标
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy=x,y
    #当移动鼠标时绘制图形，event可以查看移动效果，flag检测是否发生单击
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        if drawing == True:
            if mode == True:
                cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
            else:
                #绘制圆圈，圆点连成线，3代表笔的粗细
                cv2.circle(img,(x,y),3,(0,255,0),-1)
    #当松开鼠标时停止绘制
    elif event == cv2.EVENT_LBUTTONUP:
        drawing == False

def get_coordinate_by_click(img_path):
    global img
    img = cv2.imread(img_path)  # 图片路径
    cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)  # 设置窗口标题和大小
    # cv2.resizeWindow('image', 1000, 400)
    cv2.setMouseCallback("image", mouse)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    img_path = "sky-big.png"
    get_coordinate_by_click(img_path)
