from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from qfluentwidgets import ScrollArea, ExpandLayout, SettingCardGroup, PrimaryPushSettingCard
from qfluentwidgets import FluentIcon as FIF

from app_front.card.comboboxsettingcard2 import ComboBoxSettingCard2
from app_front.card.switchsettingcard import SwitchSettingCard1
from app_front.common.style_sheet import StyleSheet


class LogInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        # 吸顶标题
        self.logLabel = QLabel(self.tr("当前正在进行："), self)

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("logInterface")

        # 初始化样式
        self.logLabel.setObjectName('logLabel')
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.LOG_INTERFACE.apply(self)

        self.__initLayout()

    def __initLayout(self):
        self.logLabel.move(10, 20)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

