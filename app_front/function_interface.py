import inspect
import logging
import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from qfluentwidgets import ScrollArea, ExpandLayout, SettingCardGroup, PrimaryPushSettingCard, InfoBar, InfoBarPosition
from qfluentwidgets import FluentIcon as FIF

from app_front.card.comboboxsettingcard1 import ComboBoxSettingCard1
from app_front.card.comboboxsettingcard2 import ComboBoxSettingCard2
from app_front.card.switchsettingcard import SwitchSettingCard1
from app_front.common.style_sheet import StyleSheet
from managers.config_manager import config
from method.task_thread import TaskThread
from module.operation.click import Click
from module.operation.ultilities import activate


def get_current_function_name():
    """
    获取当前执行函数的函数名
    :return: 函数名
    """
    cf = inspect.currentframe()
    name = cf.f_back.f_code.co_name
    del cf  # 删除帧引用
    return name


class FunctionInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.scrollWidget = QWidget()
        # self.expandLayout = ExpandLayout(self.scrollWidget)
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        # 吸顶标题
        self.selectFunctionLabel = QLabel(self.tr("功能选择"), self)

        # 存储勾选任务
        self.chosen_tasks = []
        # 线程对象初始化为none
        self.task_thread = None

        # 原子操作
        self.click = Click()

        # 开启组
        self.startGroup = SettingCardGroup(self.tr("开启"), self.scrollWidget)
        # self.startOption = SimpleFunctionCard(
        #     icon=FIF.PLAY,
        #     title=self.tr('进入游戏'),
        #     content=self.tr('请打开启动器，开启后默认进入第一个游戏角色'),
        #     sub_view=expand.__dict__['startOption'],
        #     parent=self.startGroup
        # )
        self.startup_card = PrimaryPushSettingCard(
            self.tr('启动'),
            FIF.PLAY,
            self.tr('晶核，启动'),
            '点击开始启动脚本',
            self
        )
        self.startOption = SwitchSettingCard1(
            FIF.EMBED,
            self.tr('进入游戏'),
            "自动进入游戏，默认进入第一个角色",
            "start_option"
        )
        # 循环组
        self.cycleGroup = SettingCardGroup(self.tr("按角色循环"), self.scrollWidget)
        # self.doublePotionOption = SimpleFunctionCard(
        #     icon=FIF.CAFE,
        #     title=self.tr('制作双倍药水'),
        #     content=self.tr('自动去矿石镇制作双倍药水'),
        #     sub_view=expand.__dict__['doublePotionOption'],
        #     parent=self.cycleGroup
        # )
        self.doublePotionOption = SwitchSettingCard1(
            FIF.CAFE,
            self.tr('制作双倍药水'),
            "自动去矿石镇制作双倍药水",
            "double_potion_option"
        )
        # self.tiliOption = SimpleFunctionCard(
        #     icon=FIF.BASKETBALL,
        #     title=self.tr('刷体力'),
        #     content=self.tr('先选择要刷取的关卡'),
        #     sub_view=expand.__dict__['tiliOption'],
        #     parent=self.cycleGroup
        # )
        self.tiliOption = SwitchSettingCard1(
            FIF.CALORIES,
            self.tr('刷体力'),
            "先选择要刷取的关卡",
            "tili_option"
        )
        # self.exchangeOption = SimpleFunctionCard(
        #     icon=FIF.SHOPPING_CART,
        #     title=self.tr('商人信用兑换'),
        #     content=self.tr('可以选择是否要商城购买缺失的装备'),
        #     sub_view=expand.__dict__['exchangeOption'],
        #     parent=self.cycleGroup
        # )
        self.exchangeOption = SwitchSettingCard1(
            FIF.SHOPPING_CART,
            self.tr('商人信用兑换'),
            "可以选择是否要商城购买缺失的装备",
            "exchange_option"
        )
        # self.receiveOption = SimpleFunctionCard(
        #     icon=FIF.IOT,
        #     title=self.tr('领取奖励'),
        #     content=self.tr('把能领的都领一遍'),
        #     sub_view=expand.__dict__['receiveOption'],
        #     parent=self.cycleGroup
        # )
        self.receiveOption = SwitchSettingCard1(
            FIF.IOT,
            self.tr('领取奖励'),
            "把能领的都领一遍",
            "receive_option"
        )
        self.finishGroup = SettingCardGroup(self.tr("完成"), self.scrollWidget)
        self.afterFinishCard = ComboBoxSettingCard1(
            "after_finish",
            FIF.POWER_BUTTON,
            self.tr('任务完成后'),
            self.tr('其中“退出”指退出游戏'),
            texts={'无': 'None', '退出': 'Exit', '关机': 'Shutdown', '休眠': 'Hibernate', '睡眠': 'Sleep'}
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("functionInterface")

        # 初始化样式
        self.selectFunctionLabel.setObjectName('selectFunctionLabel')
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.FUNCTION_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.selectFunctionLabel.move(10, 20)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.startGroup.addSettingCard(self.startup_card)
        self.startGroup.addSettingCard(self.startOption)

        self.cycleGroup.addSettingCard(self.doublePotionOption)
        self.cycleGroup.addSettingCard(self.tiliOption)
        self.cycleGroup.addSettingCard(self.exchangeOption)
        self.cycleGroup.addSettingCard(self.receiveOption)

        self.finishGroup.addSettingCard(self.afterFinishCard)

        self.vBoxLayout.addWidget(self.startGroup)
        self.vBoxLayout.addWidget(self.cycleGroup)
        self.vBoxLayout.addWidget(self.finishGroup)

    def __connectSignalToSlot(self):
        self.startup_card.clicked.connect(self.start_tasks)

    def start_tasks(self):
        # 如果点击按钮的时候存在任务流并且该任务流正在运行
        if self.task_thread and self.task_thread.isRunning():
            self.task_thread.stop()
        else:
            # 收集所有任务
            if config.get_item("start_option"):
                self.chosen_tasks.append(self.start_task)
            if config.get_item("double_potion_option"):
                self.chosen_tasks.append(self.double_potion_task)
            if config.get_item("tili_option"):
                self.chosen_tasks.append(self.tili_task)
            if config.get_item("exchange_option"):
                self.chosen_tasks.append(self.exchange_task)
            if config.get_item("receive_option"):
                self.chosen_tasks.append(self.receive_task)

            self.task_thread = TaskThread(self.chosen_tasks)
            self.task_thread.finished.connect(self.task_finished)
            self.task_thread.stopped.connect(self.task_stopped)
            self.task_thread.start()
            # 侧边通知
            InfoBar.success(
                title='启动成功',
                content="日志任务栏中可查看进度",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
            # 激活窗口使窗口置顶
            activate(self.task_thread.is_running)
            # logging.debug(f"start:{self.task_thread.isRunning()}")
            self.startup_card.button.setText('停止')

    def task_finished(self):
        logging.debug(f"finish:{self.task_thread.isRunning()}")
        self.startup_card.button.setText('启动')

    def task_stopped(self):
        logging.debug(f"stopped:{self.task_thread.isRunning()}")
        self.startup_card.button.setText('启动')

    # 以下是每个任务流程
    def start_task(self):
        """
        从启动器首页进入到角色选择页面，可能需要把选角色这个操作单独独立出来
        :return:
        """
        logging.info(f"当前执行：{get_current_function_name()}")
        # 点击“开始游戏”
        self.click.common_click("start_up\\start_game.png", self.task_thread.isRunning)
        if not self.task_thread.isRunning:
            return
        # 判断是否在更新

        # 判断是否出现更新中断

        # 关闭公告

        # 进入游戏选择角色。。。

    def double_potion_task(self):
        """
        制作双倍药水
        :return:
        """
        # while True:
        #     print(f"{time.time()}")
        #     if not self.task_thread.isRunning:
        #         break
        print("task2")
        time.sleep(3)
        if not self.task_thread.isRunning:
            return

    def tili_task(self):
        """
        刷体力（估计很复杂）
        :return:
        """
        print("task3")
        time.sleep(3)
        if not self.task_thread.isRunning:
            return

    def exchange_task(self):
        """
        商人交易
        :return:
        """
        print("task4")
        time.sleep(3)
        if not self.task_thread.isRunning:
            return

    def receive_task(self):
        """
        领取游戏奖励
        :return:
        """
        print("task5")
        time.sleep(3)
        if not self.task_thread.isRunning:
            return
