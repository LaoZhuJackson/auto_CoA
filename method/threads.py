import time
import pyautogui
import pygetwindow as gw
import pyscreeze
from PyQt5.QtCore import QThread, pyqtSignal
from method.daily import waiting_loading, auto_next_character
from method.setting import load_settings
from method.utilities import click, get_parent_absolute, is_exist, long_press_key, alt_click, press_key_once


# pyautogui.PAUSE = 1


class Worker_Thread(QThread):
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)
    message_signal = pyqtSignal(str)

    def __init__(self, task_list, parent=None):
        super(Worker_Thread, self).__init__(parent)
        self.coa_window = None
        self.task_list = task_list
        self._stop_flag = False
        self.parent_absolute = get_parent_absolute()
        self.daily_setting = load_settings()['daily_setting']
        self.all_character = load_settings()['all_character']

    def stop(self):
        self._stop_flag = True

    def run(self):
        try:
            self.coa_window = gw.getWindowsWithTitle(load_settings()['coa_window_name'])[0]
            # 激活窗口，使置顶
            self.coa_window.activate()
            # 再点击一下窗口标题
            click(self.parent_absolute + '\\image\\receiving_resources\\title.png', 2)
        except IndexError:
            self.error_signal.emit("请先打开游戏启动器再运行本程序")
            self.stop()
        # 单独移出登录过程
        if self.task_list[1] is True and not self._stop_flag:
            self.start_task()
        # 减去第一个
        for now_character in range(1, self.all_character + 1):
            if not self._stop_flag:
                self.message_signal.emit(f"开始第{now_character}个角色")
                auto_next_character(now_character)
            for (index, task) in enumerate(self.task_list):
                if task and not self._stop_flag:
                    task_index = index
                    if task_index == 2:
                        self.double_potion_task()
                    elif task_index == 3:
                        self.tili()
                    elif task_index == 4:
                        self.daily()
        self.message_signal.emit("已完成所有任务")
        self.finished_signal.emit()
        self._stop_flag = True

    def start_task(self):
        self.message_signal.emit("开始进入游戏")
        # 激活窗口，使置顶
        self.coa_window.activate()
        # 再点击一下窗口标题
        click(self.parent_absolute + '\\image\\receiving_resources\\title.png', 2)
        # 等待程序打开,获取“开始游戏”图标位置
        click(self.parent_absolute + '\\image\\start_up\\start_game.png', 5, 0.7)
        click(self.parent_absolute + '\\image\\start_up\\cancel.png', 15)
        click(self.parent_absolute + '\\image\\start_up\\click_to_continue.png', 5)

        # 选择第一个角色进入
        character_list = []
        image_path = self.parent_absolute + '\\image\\start_up\\character_list.png'
        # 用“角色列表”当基准点
        start_time = time.time()
        result_flag = False
        while time.time() - start_time < 5:
            try:
                character_list = pyautogui.locateCenterOnScreen(image_path)
                result_flag = True
            except pyautogui.ImageNotFoundException:
                time.sleep(1)
        if result_flag:
            # 通过偏移创造两个拖拽点
            start_position = (character_list[0], character_list[1] + 100)
            offset = (0, 400)  # 相对移动的距离
            # 移动鼠标到起始位置
            pyautogui.moveTo(start_position)
            # 通过相对位置执行拖拽操作
            pyautogui.dragRel(offset[0], offset[1], duration=0.7)  # duration 参数表示拖拽的时间（秒）
            time.sleep(1)
            # 确定第一个角色的头像位置
            first_character = (character_list[0], character_list[1] + 120)
            pyautogui.moveTo(first_character)
            pyautogui.click()
            time.sleep(1)
            click(self.parent_absolute + '\\image\\start_up\\enter_game.png', 5)

            # 等待读条（和月卡领取界面跳出）
            waiting_loading()
            print("开始检测月卡")
            self.message_signal.emit("开始检测月卡")
            image_path = self.parent_absolute + '\\image\\receiving_resources\\monthly_card.png'
            try:
                # match = pyautogui.locateCenterOnScreen(image_path, confidence=0.9)
                # match = (1358, 540, 10, 10)

                if is_exist(image_path):
                    match = pyautogui.locateCenterOnScreen(image_path, confidence=0.9)
                    print("该玩家是月卡党")
                    self.message_signal.emit("该玩家是月卡党")
                    pyautogui.click(match)
                    pyautogui.click(match)
                    # 是否直接开启月令礼盒
                    # press_key_once('g')
            except pyautogui.ImageNotFoundException:
                print("该玩家不是月卡党")
                self.message_signal.emit("该玩家不是月卡党")
                pass
        else:
            print("选择角色超时")
            self.error_signal.emit("选择角色超时")
            self._stop_flag = True
        # 正常退出
        print("完成进入游戏")
        self.message_signal.emit("完成进入游戏")

    def double_potion_task(self):
        print("开始制作双倍药水")
        self.message_signal.emit("开始制作双倍药水")
        # 激活窗口，使置顶
        self.coa_window.activate()
        # 再点击一下窗口标题
        click(self.parent_absolute + '\\image\\receiving_resources\\title.png', 2)
        # 打开地图
        press_key_once("m")
        click(self.parent_absolute + '\\image\\receiving_resources\\world_map.png', 2)
        # 判断当前位置
        if is_exist(self.parent_absolute + "\\image\\receiving_resources\\now_in_ore_town.png"):
            # 在矿石镇，通过重新传送恢复位置
            click(self.parent_absolute + '\\image\\receiving_resources\\rhine_city_map.png', 2)
            waiting_loading()
            press_key_once("m")
        click(self.parent_absolute + '\\image\\receiving_resources\\world_map.png', 2)
        click(self.parent_absolute + '\\image\\receiving_resources\\ore_town.png', 2)
        waiting_loading()

        long_press_key('w', 3.4)
        long_press_key('a', 0.8)
        press_key_once("f")
        click(self.parent_absolute + '\\image\\receiving_resources\\purchase_minerals.png', 2)
        # 如果购买过
        if is_exist(self.parent_absolute + '\\image\\receiving_resources\\have_purchased.png'):
            press_key_once("esc")
        else:
            click(self.parent_absolute + '\\image\\receiving_resources\\select_number.png', 2)
            click(self.parent_absolute + '\\image\\receiving_resources\\3.png', 2)
            click(self.parent_absolute + '\\image\\receiving_resources\\0.png', 2, 0.9)
            click(self.parent_absolute + '\\image\\receiving_resources\\purchase_3000.png', 2)
            # 如果够钱
            if not is_exist(self.parent_absolute + '\\image\\receiving_resources\\no_money.png'):
                click(self.parent_absolute + '\\image\\receiving_resources\\yes.png', 2)
                click(self.parent_absolute + '\\image\\receiving_resources\\buy_success.png', 2)
            else:
                press_key_once("esc")
            press_key_once("esc")
        # 初始化位置移动到制作台
        press_key_once("m")
        click(self.parent_absolute + '\\image\\receiving_resources\\world_map.png', 2)
        click(self.parent_absolute + '\\image\\receiving_resources\\rhine_city_map.png', 2)
        waiting_loading()
        press_key_once("m")
        click(self.parent_absolute + '\\image\\receiving_resources\\world_map.png', 2)
        click(self.parent_absolute + '\\image\\receiving_resources\\ore_town.png', 2)
        waiting_loading()
        # 移动到工作台
        long_press_key('w', 2.9)
        long_press_key('a', 0.5)
        press_key_once("f")
        click(self.parent_absolute + '\\image\\receiving_resources\\double_potion.png', 2)
        click(self.parent_absolute + '\\image\\receiving_resources\\make_select.png', 2)
        click(self.parent_absolute + '\\image\\receiving_resources\\5.png', 2, 0.9)
        # 精力不够
        if is_exist(self.parent_absolute + '\\image\\receiving_resources\\not_enough_energy.png'):
            press_key_once("esc")
            press_key_once("esc")
        else:
            click(self.parent_absolute + '\\image\\receiving_resources\\make.png', 2)
            click(self.parent_absolute + '\\image\\receiving_resources\\buy_success.png', 5)
            press_key_once("esc")

        # 正常退出
        print("退出制作双倍药水")
        self.message_signal.emit("退出制作双倍药水")

    def tili(self):
        # todo
        print("开始刷体力")
        self.message_signal.emit("开始刷体力")
        # 激活窗口，使置顶
        self.coa_window.activate()
        self.message_signal.emit("功能还在开发中...")
        # 正常退出
        print("退出刷体力")
        self.message_signal.emit("退出刷体力")

    def daily(self):
        print("开始做日常")
        self.message_signal.emit("开始做日常")
        # 激活窗口，使置顶
        self.coa_window.activate()
        # 再点击一下窗口标题
        click(self.parent_absolute + '\\image\\receiving_resources\\title.png', 2)
        for (index, set_check) in enumerate(self.daily_setting):
            if set_check:
                # 领取商城每日奖励
                if index == 0:
                    print("开始领取商城奖励")
                    self.message_signal.emit("开始领取商城奖励")
                    alt_click(self.parent_absolute + '\\image\\receiving_resources\\market.png', 5)
                    click(self.parent_absolute + '\\image\\receiving_resources\\gift.png', 2)
                    click(self.parent_absolute + '\\image\\receiving_resources\\daily_gift.png', 2)
                    click(self.parent_absolute + '\\image\\receiving_resources\\daily_gift.png', 2)
                    if not is_exist(self.parent_absolute + '\\image\\receiving_resources\\already_daily_benefits.png'):
                        click(self.parent_absolute + '\\image\\receiving_resources\\daily_benefits.png', 2)
                        # press_key_once("esc")
                        click(self.parent_absolute + '\\image\\receiving_resources\\buy_success.png', 2)
                    click(self.parent_absolute + '\\image\\receiving_resources\\special_offer.png', 2)
                    if not is_exist(
                            self.parent_absolute + '\\image\\receiving_resources\\already_daily_supply_bag.png'):
                        click(self.parent_absolute + '\\image\\receiving_resources\\daily_supply_bag.png', 2, 0.9)
                        click(self.parent_absolute + '\\image\\receiving_resources\\free_buy.png', 2)
                        click(self.parent_absolute + '\\image\\receiving_resources\\buy_success.png', 2)
                    # press_key_once("esc")
                    # 返回游戏界面
                    press_key_once("esc")
                    # 打开日常礼包
                    if is_exist(self.parent_absolute + '\\image\\receiving_resources\\open_daily_gift.png'):
                        press_key_once('g')
                        press_key_once("esc")
                    self.message_signal.emit("完成领取商城奖励")
                # 领取舰队奖励
                elif index == 1:
                    print("开始舰队日常")
                    self.message_signal.emit("开始舰队日常")
                    # 呼出菜单
                    press_key_once("esc")
                    click(self.parent_absolute + '\\image\\receiving_resources\\fleet.png', 2)
                    click(self.parent_absolute + '\\image\\receiving_resources\\meeting_place.png', 2)
                    # 如果未打卡
                    if not is_exist(self.parent_absolute + '\\image\\receiving_resources\\already_punch_card.png'):
                        click(self.parent_absolute + '\\image\\receiving_resources\\punch_card.png', 2)
                        click(self.parent_absolute + '\\image\\receiving_resources\\buy_success.png', 2)
                        # press_key_once("esc")
                        press_key_once("esc")
                        click(self.parent_absolute + '\\image\\receiving_resources\\research_and_development.png', 2)
                        if is_exist(self.parent_absolute + '\\image\\receiving_resources\\speed_up.png'):
                            click(self.parent_absolute + '\\image\\receiving_resources\\speed_up.png', 2)
                            click(self.parent_absolute + '\\image\\receiving_resources\\speed_up_2.png', 2,0.9)
                            click(self.parent_absolute + '\\image\\receiving_resources\\buy_success.png', 2)
                            press_key_once("esc")
                    press_key_once("esc")
                    press_key_once("esc")
                    self.message_signal.emit("完成舰队日常")
                # 领取邮件
                elif index == 2:
                    print("开始领取邮件奖励")
                    self.message_signal.emit("开始领取邮件")
                    press_key_once("esc")
                    click(self.parent_absolute + '\\image\\receiving_resources\\mail.png', 2)
                    click(self.parent_absolute + '\\image\\receiving_resources\\receive_all.png', 2)
                    if not is_exist(self.parent_absolute + '\\image\\receiving_resources\\no_mail.png'):
                        click(self.parent_absolute + '\\image\\receiving_resources\\buy_success.png', 2)
                    press_key_once("esc")
                    self.message_signal.emit("完成领取邮件")
                # 七日签到并且抽夏娜的赠礼
                elif index == 3:
                    self.message_signal.emit("开始签到并抽取夏娜的赠礼")
                    alt_click(self.parent_absolute + '\\image\\receiving_resources\\welfare.png', 5)
                    if is_exist(self.parent_absolute + '\\image\\receiving_resources\\awaiting_collection.png', 0.8):
                        click(self.parent_absolute + '\\image\\receiving_resources\\awaiting_collection.png', 5)
                        click(self.parent_absolute + '\\image\\receiving_resources\\buy_success.png', 2)
                    click(self.parent_absolute + '\\image\\receiving_resources\\gift_of_shana.png', 2, 0.8)
                    if not is_exist(self.parent_absolute + '\\image\\receiving_resources\\already_lottery.png'):
                        click(self.parent_absolute + '\\image\\receiving_resources\\lottery.png', 2)
                        time.sleep(5)
                        click(self.parent_absolute + '\\image\\receiving_resources\\buy_success.png', 7)
                    press_key_once("esc")
                    self.message_signal.emit("完成签到并抽取夏娜的赠礼")
                # 领取在线礼物
                elif index == 4:
                    self.message_signal.emit("开始领取在线礼物")
                    alt_click(self.parent_absolute + '\\image\\receiving_resources\\welfare.png', 5)
                    if not is_exist(self.parent_absolute + '\\image\\receiving_resources\\online_gift_receive.png'):
                        click(self.parent_absolute + '\\image\\receiving_resources\\online_gift.png', 2, 0.9)
                    # click(self.parent_absolute + '\\image\\receiving_resources\\online_gift_receive.png')
                    n = 0
                    match_list = []
                    try:
                        need_click = pyautogui.locateAllOnScreen(
                            self.parent_absolute + '\\image\\receiving_resources\\online_gift_receive.png',
                            confidence=0.9)
                        # 确定点击次数
                        for match in need_click:
                            n += 1
                            match_list.append(match[:2])
                        # 取出最左边那个
                        x, y = match_list[0]
                        for i in range(n):
                            pyautogui.click(x, y)
                            click(self.parent_absolute + '\\image\\receiving_resources\\buy_success.png', 3)
                    except pyscreeze.ImageNotFoundException:
                        pass
                    press_key_once("esc")
                    self.message_signal.emit("完成领取在线礼物")
                # todo 领取战令
                elif index == 5:
                    self.message_signal.emit("开始领取战令")

                    self.message_signal.emit("完成领取战令")

        # 正常退出
        print("已完成日常")
        self.message_signal.emit("已完成日常")
