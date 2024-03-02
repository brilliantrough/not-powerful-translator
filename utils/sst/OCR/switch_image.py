r"""
Author: brilliantrough pzyinnju@163.com
Date: 2023-12-07 20:09:20
LastEditors: brilliantrough pzyinnju@163.com
LastEditTime: 2023-12-07 23:31:08
FilePath: \not-powerful-translator\utils\sst\OCR\switch_image.py
Description: 

Copyright (c) 2023 by {brilliantrough pzyinnju@163.com}, All Rights Reserved. 
"""

# import cv2
# import os

# os.environ[
#     "QT_QPA_PLATFORM_PLUGIN_PATH"
# ] = "/home/pzy000/miniconda3/envs/pyqt/lib/python3.10/site-packages/cv2/qt/plugins/platforms"

from PIL import Image, ImageTk
import tkinter as tk

current_image = 1


def switch_image():
    return switch_image_tk()


def switch_image_tk():
    # Initialize variables to keep track of the current image and state
    image_paths = ["screenshot.png", "screenshot_text.png"]

    # Function to toggle between images
    def toggle_image():
        global current_image
        current_image = 1 - current_image  # Toggle between 0 and 1
        image = Image.open(image_paths[current_image])
        tk_image = ImageTk.PhotoImage(image)
        label.configure(image=tk_image)
        label.image = tk_image  # Keep a reference to avoid garbage collection

    # Create a tkinter window
    root = tk.Tk()
    root.title("Image Viewer")

    # Load the initial image
    image = Image.open(image_paths[current_image])
    tk_image = ImageTk.PhotoImage(image)

    # Display the image in a Label widget
    label = tk.Label(root, image=tk_image)
    label.pack()
    button_frame = tk.Frame(root)
    button_frame.pack(fill=tk.X, side=tk.BOTTOM)

    # Create a toggle button
    toggle_button = tk.Button(
        button_frame,
        text="Toggle Image",
        command=toggle_image,
        font=("Arial", 12, "bold"),
    )
    toggle_button.pack(side=tk.RIGHT, padx=5, pady=5)

    # Function to close the window
    def close_window():
        root.destroy()

    # Create a button to close the window
    close_button = tk.Button(
        button_frame, text="Close", command=close_window, font=("Arial", 12, "bold")
    )
    close_button.pack(side=tk.RIGHT, padx=5)

    # Start the tkinter main loop
    root.mainloop()


# def switch_image():
#     # 读取两张图像
#     image1 = cv2.imread("screenshot.png")
#     image2 = cv2.imread("screenshot_text.png")

#     # 创建窗口
#     cv2.namedWindow("Image Viewer")
#     original_height, original_width = image1.shape[:2]
#     # cv2.resizeWindow("Image Viewer", original_width, original_height)

#     # 初始状态设为1，表示展示image1
#     toggle_state = 1

#     while True:
#         # 根据切换状态选择要展示的图像
#         if toggle_state == 1:
#             cv2.imshow("Image Viewer", image1)
#         else:
#             cv2.imshow("Image Viewer", image2)

#         # 监听键盘输入，按 'q' 键退出循环
#         key = cv2.waitKey(5) & 0xFF
#         if key == ord("q"):
#             break
#         elif key == ord("t"):
#             # 切换按钮按下，切换图像
#             toggle_state = 1 - toggle_state

#         if cv2.getWindowProperty("Image Viewer", cv2.WND_PROP_VISIBLE) < 1:
#             break
#     # 释放窗口
#     cv2.destroyAllWindows()
