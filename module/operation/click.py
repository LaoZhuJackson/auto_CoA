import logging
import os
import sys
import time
from PIL import Image

import pyautogui


def is_valid_image_path(relative_path):
    # 将相对路径转换成绝对路径
    abs_path = os.path.abspath(relative_path)
    logging.debug(f"当前工作路径是：{os.getcwd()}")

    # 检查转换后的路径是否存在
    if not os.path.exists(abs_path):
        logging.error(f"{abs_path} 不存在")
        return False

    # 尝试打开图片文件
    try:
        with Image.open(abs_path) as img:
            # 可以在这里做额外的检查，例如检查图像大小
            img.verify()  # 验证文件是不是图片
            logging.debug(f" {abs_path} 是有效路径")
            return True
    except (IOError, FileNotFoundError, Image.UnidentifiedImageError):
        print(f"{abs_path}处的文件不是有效的映像或已损坏")
        logging.error(f"{abs_path}处的文件不是有效的映像或已损坏")
        return False


class Click:
    def __init__(self):
        self.path = None
        self.timeout = 30
        self.confidence = 0.7
        # 为了保证资源路径在开发和打包后都正确
        if getattr(sys, 'frozen', False):
            # 如果是打包后的应用，使用系统的绝对路径
            self.basedir = os.path.join(sys._MEIPASS, "image")
        else:
            # 如果是开发中的代码，使用当前目录的相对路径
            self.basedir = 'image'

    def common_click(self, image, is_running: bool, timeout=3, confidence=0.7):
        start_time = time.time()
        image_path = os.path.join(self.basedir, image)
        while time.time() - start_time < timeout and is_running and is_valid_image_path(image_path):
            try:
                # 尝试定位界面中的特定图像
                location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
                if location is not None:
                    # 图像找到，执行点击，退出循环
                    pyautogui.click(location)
                    print("单击")
                    time.sleep(0.3)
                    break
                # 图像未找到，等待一小段时间后重试
                time.sleep(0.5)
            except pyautogui.ImageNotFoundException:
                # 如果跳过没有检测到图片就跳过
                pass

    def alt_click(self,img_path, timeout=2, confidence=0.8):
        pyautogui.keyDown('alt')
        self.common_click()
        pyautogui.keyUp('alt')