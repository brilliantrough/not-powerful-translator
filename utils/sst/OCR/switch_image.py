r"""
Author: brilliantrough pzyinnju@163.com
Date: 2023-12-07 20:09:20
LastEditors: brilliantrough pzyinnju@163.com
LastEditTime: 2023-12-07 23:31:08
FilePath: \not-powerful-translator\utils\sst\OCR\switch_image.py
Description: 

Copyright (c) 2023 by {brilliantrough pzyinnju@163.com}, All Rights Reserved. 
"""

import cv2

def switch_image():
    # 读取两张图像
    image1 = cv2.imread('screenshot.png')
    image2 = cv2.imread('screenshot_text.png')

    # 创建窗口
    cv2.namedWindow('Image Viewer', cv2.WINDOW_NORMAL)
    original_height, original_width = image1.shape[:2]
    cv2.resizeWindow('Image Viewer', original_width, original_height)

    # 初始状态设为1，表示展示image1
    toggle_state = 1

    while True:
        # 根据切换状态选择要展示的图像
        if toggle_state == 1:
            cv2.imshow('Image Viewer', image1)
        else:
            cv2.imshow('Image Viewer', image2)

        # 监听键盘输入，按 'q' 键退出循环
        key = cv2.waitKey(5) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('t'):
            # 切换按钮按下，切换图像
            toggle_state = 1 - toggle_state

        if cv2.getWindowProperty('Image Viewer', cv2.WND_PROP_VISIBLE) < 1:
            break
    # 释放窗口
    cv2.destroyAllWindows()
