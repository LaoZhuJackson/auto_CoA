import logging
import os
import time

# import pywinauto.findwindows
from PIL import Image, ImageChops
import pygetwindow as gw

import pyautogui

# from pywinauto import Application, Desktop

from managers.config_manager import config
from managers.utilities_manager import utilities
from module.utils.path_utils import PathUtils


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
        self.game_path = config.get_item("game_path")
        self.game_name = self.game_path.split("/")[-1]  # “晶核：魔导觉醒.exe”
        self.game_title = self.game_name.split(".")[0]  # “晶核：魔导觉醒”
        self.basedir = os.path.join(PathUtils.get_base_dir(), "image")

    def common_click(self, image, is_running: bool, timeout=1, confidence=0.7):
        if utilities.is_exist(image):
            start_time = time.time()
            image_path = os.path.join(self.basedir, image)
            timeout_flag = True
            while (
                time.time() - start_time < timeout
                and is_running
                and is_valid_image_path(image_path)
            ):
                try:
                    # 尝试定位界面中的特定图像
                    location = pyautogui.locateCenterOnScreen(
                        image_path, confidence=confidence
                    )
                    if location is not None:
                        # 说明出现了能点的坐标
                        logging.debug(str(location))
                        box_area = (
                            int(location[0] - 20),
                            int(location[1] - 20),
                            int(location[0] + 20),
                            int(location[1] + 20),
                        )
                        # 获取初始屏幕截图
                        prev_image = pyautogui.screenshot(region=box_area)
                        while time.time() - start_time < timeout:
                            # 执行点击
                            pyautogui.click(location)
                            time.sleep(0.3)
                            new_image = pyautogui.screenshot(region=box_area)
                            # difference这个函数用于比较两幅图像，并生成一幅新图像,工作原理是对每个对应的像素进行相减操作。在结果图像中，如果两个输入图像在某个像素上完全相同，那么对应的结果图像上的该像素点将会是黑色（值为0）
                            diff = ImageChops.difference(prev_image, new_image)
                            if diff.getbbox() is not None:
                                # 如果图像有变化则退出循环，说明点击生效了
                                logging.debug("图像发生变化")
                                timeout_flag = False
                                break
                            else:
                                logging.debug("图像未检测出变化")
                except pyautogui.ImageNotFoundException:
                    # 图像未找到，等待一小段时间后重试
                    time.sleep(0.5)
            if timeout_flag:
                logging.error("点击操作超时")

    def alt_click(self, image, is_running, timeout=2, confidence=0.8):
        pyautogui.keyDown("alt")
        self.common_click(image, is_running, timeout, confidence)
        pyautogui.keyUp("alt")

    def activate_coa(self, is_running: bool):
        """
        激活游戏窗口使置顶
        :param is_running:
        :return:
        """
        logging.debug(f"activate:{is_running}")
        if is_running:
            try:
                # app = Application(backend="uia").connect(path=self.game_title)
                coa_window = gw.getWindowsWithTitle(self.game_title)[0]
                # 激活窗口，使置顶
                coa_window.activate()

                # 获取当前桌面上的所有顶层窗口
                # windows = Desktop(backend="uia").windows()
                #
                # 打印所有窗口的标题和进程ID
                # for w in windows:
                #     logging.debug(f"{w.window_text()}, {w.process_id()}")

                # window = app.window(title=self.game_title)
                # if window.is_minimized():
                #     window.restore()
                # 再点击一下窗口标题
                self.common_click("receiving_resources\\title.png", is_running)
            except IndexError:
                logging.info(self.game_name)
                logging.error("请先打开游戏启动器再运行")
            # except pywinauto.findwindows.ElementNotFoundError:
            #     logging.error(f"未能找到标题为{self.game_title}的窗口")
