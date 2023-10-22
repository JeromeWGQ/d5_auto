# coding:utf-8

from aip import AipImageClassify

""" 这里输入你创建应用获得的三个参数"""
APP_ID = '41492073'
API_KEY = 'ZNrlm7G84G75mHi7MdSIFzIc'
SECRET_KEY = '9Qk24q9UwEEp6EmXRg7lhvKfSEhEMPfV'

client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


image = get_file_content('2.png')

""" 调用通用物体识别 """
print(client.advancedGeneral(image))
