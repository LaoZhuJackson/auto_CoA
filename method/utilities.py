import os
import sys
import time
from datetime import datetime

import pyautogui

from method.setting import load_settings, update_settings

# pyautogui.PAUSE = 1
pyautogui.FAILSAFE = False


def click(image_path, timeout=30, confidence=0.7):
    start_time = time.time()
    flag = False
    message = {
        # 0:初始状态，1：点击成功，2：超时
        "status": 0,
        "error": ''
    }
    while time.time() - start_time < timeout:
        # print(time.time() - start_time)
        try:
            # 尝试定位界面中的特定图像
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if location is not None:
                # 图像找到，执行点击，退出循环
                flag = True
                pyautogui.click(location)
                message['status'] = 1
                print("单击")
                time.sleep(0.3)
                break
            # 图像未找到，等待一小段时间后重试
            time.sleep(0.5)
        except pyautogui.ImageNotFoundException:
            # 如果跳过没有检测到图片就跳过
            pass
    if not flag:
        message['status'] = 2
        message['error'] = '本次操作检测超时'

    return message


def alt_click(img_path, timeout=2, confidence=0.8):
    pyautogui.keyDown('alt')
    click(img_path, timeout, confidence)
    pyautogui.keyUp('alt')


# 长按键盘的示例函数
def long_press_key(key, duration):
    # 模拟按下键
    pyautogui.keyDown(key)
    # 等待一段时间，模拟长按效果
    time.sleep(duration)
    # 释放键
    pyautogui.keyUp(key)


def press_key_once(key):
    pyautogui.press(key)
    time.sleep(0.3)


def get_parent_absolute():
    # 获取当前脚本文件所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取上一层目录的绝对路径
    parent_directory = os.path.abspath(os.path.join(script_dir, '..'))
    return parent_directory


def is_exist(image_path, confidence=0.9, timeout=1):
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


def is_timeout(start_time, timeout):
    if time.time() - start_time < timeout:
        return False
    else:
        return True


def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.normpath(os.path.join(base_path, relative_path))


def run_next(to_do_list: list, current_index: int):
    """
    根据现在执行的操作返回下一个要执行的操作
    :param to_do_list: 要执行的checkbox组成的列表
    :param current_index: 目前执行到第几个checkbox
    :return: 下一个要执行的是第几个checkbox
    """
    for (index, todo) in enumerate(to_do_list):
        if todo == current_index:
            # 如果下一个下标依旧在合法下标内，则返回下一个要执行的操作下标
            if index + 1 <= len(to_do_list) - 1:
                return to_do_list[index + 1]
            # 如果已经执行到最后一个操作
            return 0
