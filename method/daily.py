import os
import time
import pyautogui

from method.setting import load_settings, update_settings
from method.utilities import click, long_press_key, is_exist, get_parent_absolute, press_key_once

pyautogui.PAUSE = 1
parent_absolute = get_parent_absolute()


def waiting_loading():
    print("正在等待加载界面")
    while True:
        if is_exist(parent_absolute + "\\image\\loading\\factory_loading.png", timeout=0.1):
            print("正在加载克罗姆工厂")
        elif is_exist(parent_absolute + "\\image\\loading\\giant_tree_loading.png", timeout=0.1):
            print("正在加载古代巨树")
        elif is_exist(parent_absolute + "\\image\\loading\\ore_town_loading.png", timeout=0.1):
            print("正在加载矿石镇")
        elif is_exist(parent_absolute + "\\image\\loading\\rhine_city_loading.png", timeout=0.1):
            print("正在加载莱茵城")
        elif is_exist(parent_absolute + "\\image\\loading\\void_loading.png", timeout=0.1):
            print("正在加载虚空")
        else:
            print("未进行加载地图")
            break
    # while is_exist(loading_image_path):
    #     time.sleep(1)
    #     pass
    time.sleep(1)
    print("退出等待")


def auto_next_character(now_character_num):
    print(f"当前需要选择第{now_character_num}个角色")
    # 如果不是第一个角色
    pivot_select_dict = load_settings()['pivot_select_dict']
    if now_character_num != 1:
        press_key_once("esc")
        click(parent_absolute + '\\image\\tili\\setting.png', 2)
        click(parent_absolute + '\\image\\tili\\switch_character.png', 2)
        start_time = time.time()
        # 此时列表不再移动，用这个位置作为基准点
        while time.time() - start_time < 5:
            try:
                if now_character_num == 2:
                    now_selected = pyautogui.locateCenterOnScreen(parent_absolute + '\\image\\tili\\now_selected_2.png',
                                                                  confidence=0.9)
                elif now_character_num == 3:
                    now_selected = pyautogui.locateCenterOnScreen(parent_absolute + '\\image\\tili\\now_selected_3.png',
                                                                  confidence=0.9)
                    pivot_select = [now_selected[0], now_selected[1]]
                    pivot_select_dict["pivot_select_x"] = int(now_selected[0])
                    pivot_select_dict["pivot_select_y"] = int(now_selected[1])
                    print(type(now_selected[0]))
                    update_settings({
                        "pivot_select_dict": pivot_select_dict
                    })
                # elif now_character_num == 4:
                #     now_selected = pyautogui.locateCenterOnScreen(parent_absolute + '\\image\\tili\\now_selected_4.png',
                #                                                   confidence=0.9)
                # elif now_character_num == 5:
                #     now_selected = pyautogui.locateCenterOnScreen(parent_absolute + '\\image\\tili\\now_selected_6.png',
                #                                                   confidence=0.9)
                # elif now_character_num == 6:
                #     now_selected = pyautogui.locateCenterOnScreen(parent_absolute + '\\image\\tili\\now_selected_6.png',
                #                                                   confidence=0.9)
                # elif now_character_num == 7:
                #     now_selected = pyautogui.locateCenterOnScreen(parent_absolute + '\\image\\tili\\now_selected_7.png',
                #                                                   confidence=0.9)
                else:
                    now_selected = [pivot_select_dict["pivot_select_x"], pivot_select_dict["pivot_select_y"] + 100]
                    pivot_select_dict["pivot_select_x"] = int(now_selected[0])
                    pivot_select_dict["pivot_select_y"] = int(now_selected[1])
                    update_settings({
                        "pivot_select_dict": pivot_select_dict
                    })
                if now_selected:
                    next_click = (now_selected[0], now_selected[1] + 100)
                    pyautogui.moveTo(next_click)
                    pyautogui.click(next_click)
                    time.sleep(1)
                    click(parent_absolute + '\\image\\start_up\\enter_game.png', 5)
                    waiting_loading()
            except pyautogui.ImageNotFoundException:
                time.sleep(1)
