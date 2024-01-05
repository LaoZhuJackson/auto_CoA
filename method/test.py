import os
import time

import pyautogui

from method.setting import load_settings, update_settings
from method.daily import waiting_loading, parent_absolute
from method.utilities import is_exist

# daily_resources()

# click_start()

# import threading
# import time
#
#
# def my_thread_function():
#     print("Thread started")
#     time.sleep(5)  # 模拟线程执行一些操作
#     print("Thread finished")
#
# def listener_function(thread_to_monitor):
#     # 监听线程的状态
#     while thread_to_monitor.is_alive():
#         print("Listener: Thread is still running...")
#         time.sleep(2)
#
#     print("Listener: Thread has stopped")
#
# # 创建线程
# my_thread = threading.Thread(target=my_thread_function)
#
# # 启动线程
# my_thread.start()
#
# # 等待线程结束
# my_thread.join()
#
# # 检查线程是否停止
# if not my_thread.is_alive():
#     print("Thread has stopped")
# else:
#     print("Thread is still running")

# operation_list = load_settings()["checked_list"]
# print(operation_list)
# print(operation_list[5])


# to_do_list = [1,2,2,3]
# append_message("hahaha")
# append_message(f"当前的工作列表为：{to_do_list}")

# import pygetwindow as gw
#
# # 获取所有窗口
# windows = gw.getAllTitles()
# coa_window = gw.getWindowsWithTitle("晶核：魔导觉醒")[0]
# coa_window.maximize()
# coa_window.activate()
# window = gw.Window(67670)
# # print(window.isActive)
#
# # 选择第一个窗口
# window_handle = windows[0]
#
# print(f"Window Handle: {coa_window}")
# print(window.title)

# from config.config import cfg
# print(cfg.coa_window_name.value)
# print(type(cfg.coa_window_name.value))
# script_dir = os.path.dirname(os.path.abspath(__file__))
# print(os.path.abspath(os.path.join(script_dir, '..')))

# while True:
#     if is_exist(parent_absolute+"\\image\\receiving_resources\\now_in_ore_town.png"):
#         print("现在正在矿石镇")
#     else:
#         print("现在在矿石镇以外的地方")

update_settings({
    "coa_window_name": "晶核：魔导觉醒",
})
