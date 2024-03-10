import logging
import os
import sys
import time

import pyautogui

from managers.config_manager import config


class Utilities:
    def __init__(self):
        self.game_path = config.get_item("game_path")
        self.game_name = self.game_path.split('/')[-1].split('.')[0]  # “晶核：魔导觉醒”
        # 为了保证资源路径在开发和打包后都正确
        if getattr(sys, 'frozen', False):
            # 如果是打包后的应用，使用系统的绝对路径
            self.basedir = os.path.join(sys._MEIPASS, "image")
        else:
            # 如果是开发中的代码，使用当前目录的相对路径
            self.basedir = 'image'

    def is_exist(self, image_path, timeout=1, confidence=0.7):
        """
        判断画面中是否存在某个图像，用于对判断游戏状态
        :param image_path: 需要判断匹配的图片路径
        :param confidence: 置信度
        :param timeout: 超时阈值
        :return:
        """
        image_path = os.path.join(self.basedir, image_path)
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                if location is not None:
                    return True
            except pyautogui.ImageNotFoundException:
                # 如果跳过没有检测到图片就跳过
                pass
        return False
