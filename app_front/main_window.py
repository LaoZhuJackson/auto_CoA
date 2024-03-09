import logging
import subprocess
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QSize
from contextlib import redirect_stdout

from app_front.common.signal_bus import signalBus
from managers.config_manager import config

with redirect_stdout(None):
    from qfluentwidgets import NavigationItemPosition, MSFluentWindow, SplashScreen, setThemeColor, \
        NavigationBarPushButton, toggleTheme, setTheme, darkdetect, Theme, ScrollArea
    from qfluentwidgets import FluentIcon as FIF
    from qfluentwidgets import InfoBar, InfoBarPosition

from app_front.home_interface import HomeInterface
from app_front.setting_interface import SettingInterface
from app_front.function_interface import FunctionInterface
from app_front.log_interface import LogInterface


def open_game():
    path = config.get_item("game_path")
    game_dir = config.get_item("game_dir")  # 游戏的目录
    try:
        # 需要设置工作目录，不然晶核会在python文件所在文件夹建立工作区
        subprocess.Popen(path, cwd=game_dir)
        logging.info("打开游戏成功")
    except Exception as e:
        logging.error(f"打开游戏出错，请前往设置修改游戏路径后重启auto_coa：{e}")


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        setThemeColor('#FF6A6A')
        setTheme(Theme.AUTO)
        self.setMicaEffectEnabled(False)

        self.initWindow()

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.settingInterface = SettingInterface(self)
        self.functionInterface = FunctionInterface(self)
        self.logInterface = LogInterface(self)

        self.initNavigation()
        self.splashScreen.finish()

        # 检查更新
        # if config.check_update:
        #     checkUpdate(self)
        # 检查是否自动打开游戏
        if config.get_item("auto_open") is True:
            open_game()
        # 绑定信号槽，实现快捷跳转
        self.connectSignalToSlot()

    def connectSignalToSlot(self):
        # print("调用了connectSignalToSlot")
        signalBus.switchToSampleCard.connect(self.switchToSample)

    def initNavigation(self):
        # add navigation items
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('主页'))
        self.addSubInterface(self.functionInterface, FIF.COMPLETED, self.tr('主要功能'))
        self.addSubInterface(self.logInterface, FIF.MEGAPHONE, self.tr('任务日志'))

        # self.navigationInterface.addWidget(
        #     'themeButton',
        #     NavigationBarPushButton(FIF.BRUSH, '主题', isSelectable=False),
        #     self.toggleTheme,
        #     NavigationItemPosition.BOTTOM)
        #
        # self.navigationInterface.addWidget(
        #     'avatar',
        #     NavigationBarPushButton(FIF.HEART, '赞赏', isSelectable=False),
        #     self.onSupport,
        #     NavigationItemPosition.BOTTOM
        # )

        self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr('设置'),
                             position=NavigationItemPosition.BOTTOM)
        # 启动时跳转到日志页面
        # self.switchTo(self.logInterface)

    def initWindow(self):
        # 禁用最大化
        self.titleBar.maxBtn.setHidden(True)
        self.titleBar.maxBtn.setDisabled(True)
        self.titleBar.setDoubleClickEnabled(False)
        self.setResizeEnabled(False)
        # self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)

        self.resize(900, 700)
        self.setWindowIcon(QIcon(r'icon.ico'))
        self.setWindowTitle("CoA Assistant")
        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(128, 128))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    # def handleUpdate(self, status):
    #     if status == 2:
    #         w = MessageBoxUpdate(self.update_thread.title, self.update_thread.content, self.window())
    #         if w.exec():
    #             import subprocess
    #             source_file = r".\\Update.exe"
    #             assert_url = FastestMirror.get_github_mirror(self.update_thread.assert_url)
    #             subprocess.run(['start', source_file, assert_url], shell=True)
    #     elif status == 1:
    #         InfoBar.success(
    #             title=self.tr('当前是最新版本(＾∀＾●)'),
    #             content="",
    #             orient=Qt.Horizontal,
    #             isClosable=True,
    #             position=InfoBarPosition.TOP,
    #             duration=1000,
    #             parent=self
    #         )
    #     else:
    #         InfoBar.warning(
    #             title=self.tr('检测更新失败(╥╯﹏╰╥)'),
    #             content="",
    #             orient=Qt.Horizontal,
    #             isClosable=True,
    #             position=InfoBarPosition.TOP,
    #             duration=1000,
    #             parent=self
    #         )
    def switchToSample(self, routeKey, index):
        """
        用于跳转到指定页面
        :param routeKey: 跳转路径
        :param index:
        :return:
        """
        interfaces = self.findChildren(ScrollArea)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                # w.scrollToCard(index)
