from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from qfluentwidgets import ScrollArea, ExpandLayout, SettingCardGroup, PrimaryPushSettingCard
from qfluentwidgets import FluentIcon as FIF

from app_front.card.comboboxsettingcard2 import ComboBoxSettingCard2
from app_front.card.switchsettingcard import SwitchSettingCard1
from app_front.common.style_sheet import StyleSheet


class FunctionInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.scrollWidget = QWidget()
        # self.expandLayout = ExpandLayout(self.scrollWidget)
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        # 吸顶标题
        self.selectFunctionLabel = QLabel(self.tr("功能选择"), self)

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
            "请打开启动器，开启后默认进入第一个游戏角色",
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
        self.afterFinishCard = ComboBoxSettingCard2(
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
