
# import cv2
# import os

# os.environ[
#     "QT_QPA_PLATFORM_PLUGIN_PATH"
# ] = "/home/pzy000/miniconda3/envs/pyqt/lib/python3.10/site-packages/cv2/qt/plugins/platforms"

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon
import icon_rc

class SwitchImage(QWidget):
    def __init__(self):
        super().__init__()
        self.current_image = 0
        self.image_paths = ["screenshot.png", "screenshot_text.png"]
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Viewer")
        self.setWindowIcon(QIcon(":/candy.ico"))
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.image_label = QLabel(self)
        self.pixmap_tuple = (QPixmap(self.image_paths[0]), QPixmap(self.image_paths[1]))
        self.image_label.setPixmap(self.pixmap_tuple[self.current_image])
        self.layout.addWidget(self.image_label)
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_layout.addItem(spacer)

        self.toggle_button = QPushButton('Toggle', self)
        self.toggle_button.clicked.connect(self.toggle_image)
        self.button_layout.addWidget(self.toggle_button)

        self.close_button = QPushButton('Close', self)
        self.close_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.close_button)

    def toggle_image(self):
        self.current_image = 1 - self.current_image
        self.image_label.setPixmap(self.pixmap_tuple[self.current_image])


def switch_image():
    image_view = SwitchImage()
    image_view.show()

# def switch_image_tk():
#     # Initialize variables to keep track of the current image and state
#     image_paths = ["screenshot.png", "screenshot_text.png"]
#     current_image = 1

#     # Function to toggle between images
#     def toggle_image():
#         global current_image
#         current_image = 1 - current_image  # Toggle between 0 and 1
#         label.configure(image=tk_image_tuple[current_image])
#         print("toggle")
#         label.image = tk_image_tuple[current_image]  # Keep a reference to avoid garbage collection

#     # Create a tkinter window
#     root = tk.Tk()
#     root.title("Image Viewer")

#     # Load the initial image
#     image = Image.open(image_paths[current_image])
#     tk_image_tuple = (ImageTk.PhotoImage(Image.open(image_paths[0])), ImageTk.PhotoImage(Image.open(image_paths[1])))

#     # Display the image in a Label widget
#     label = tk.Label(root, image=tk_image_tuple[current_image])
#     label.pack()
#     button_frame = tk.Frame(root)
#     button_frame.pack(fill=tk.X, side=tk.BOTTOM)

#     # Create a toggle button
#     toggle_button = tk.Button(
#         button_frame,
#         text="Toggle Image",
#         command=toggle_image,
#         font=("Arial", 12, "bold"),
#     )
#     toggle_button.pack(side=tk.RIGHT, padx=5, pady=5)

#     # Function to close the window
#     def close_window():
#         root.destroy()

#     # Create a button to close the window
#     close_button = tk.Button(
#         button_frame, text="Close", command=close_window, font=("Arial", 12, "bold")
#     )
#     close_button.pack(side=tk.RIGHT, padx=5)

#     # Start the tkinter main loop
#     root.mainloop()


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
