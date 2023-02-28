import win32api
import win32gui
import win32con

if __name__ == '__main__':
    print('start')
    win32api.MessageBox(0, "hello pywin32", "messagebox", win32con.MB_OK | win32con.MB_ICONWARNING)
