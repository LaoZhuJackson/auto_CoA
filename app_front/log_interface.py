import sys

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit
from qfluentwidgets import ScrollArea, ExpandLayout, SettingCardGroup, PrimaryPushSettingCard
from qfluentwidgets import FluentIcon as FIF

from app_front.common.style_sheet import StyleSheet
from managers.logger_manager import text_stream


class LogInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        # 吸顶标题
        self.logLabel = QLabel(self.tr("日志："), self)

        self.text_edit = QTextEdit()

        self.__initWidget()
        # 重定向输出到gui
        self.__redirectOutput()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("logInterface")

        # 设置为只读
        self.text_edit.setReadOnly(True)

        # 初始化样式
        self.logLabel.setObjectName('logLabel')
        self.text_edit.setObjectName('log')
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.LOG_INTERFACE.apply(self)

        self.__initLayout()

    def __initLayout(self):
        self.logLabel.move(10, 20)

        self.vBoxLayout.addWidget(self.text_edit)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

    def __redirectOutput(self):
        # 普通输出
        sys.stdout = text_stream
        # 报错输出
        sys.stderr = text_stream
        # 将新消息信号连接到QTextEdit
        text_stream.message.connect(self.__updateDisplay)

    def __updateDisplay(self, message):
        # 将消息添加到 QTextEdit，自动识别 HTML
        self.text_edit.insertHtml(message)
        self.text_edit.insertPlainText('\n')  # 为下一行消息留出空间
        self.text_edit.ensureCursorVisible()  # 滚动到最新消息
