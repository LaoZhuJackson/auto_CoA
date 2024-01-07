import logging
import sys
import time

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

from font_pyqt.mainWindow import Ui_MainWindow
from loguru import logger
from method.setting import load_settings, update_settings
from method.threads import Worker_Thread
from qfluentwidgets import FluentIcon as FIF

checked_list = load_settings()["checked_list"]
daily_setting = load_settings()["daily_setting"]


# message_dict = {
#     'finish': '已完成所有任务',
#     'start_reward': '开始领取奖励',
#     'start_reward_market': '开始领取商城奖励',
#     'start_reward_fleet': '开始领取舰队奖励',
#     'start_reward_mail': '开始领取邮件奖励',
#     'exit_reward': '退出领取奖励',
#     'exit_tili': '退出刷体力',
#     'start_tili': '开始刷体力',
#     'exit_double_potion': '退出制作双倍药水',
#     'start_double_potion': '开始制作双倍药水',
#     'finish_entry_game': '完成进入游戏',
#     'start_entry_game': '开始进入游戏',
#     'select_characters_timeout': '选择角色超时',
#     'check_monthly_card': '开始检测月卡',
#     'is_monthly_card': '该玩家是月卡党',
#     'not_monthly_card': '该玩家不是月卡党',
# }


class QtHandler(logging.Handler):
    def __init__(self, text_edit):
        super(QtHandler, self).__init__()
        self.text_edit = text_edit

    def emit(self, record):
        log_entry = self.format(record)
        # 将日志添加到 QTextEdit
        self.text_edit.appendPlainText(log_entry)


def check_box_state_change_1(state):
    if state == 2:
        checked_list[1] = True
    else:
        checked_list[1] = False
    # 更新设置
    update_settings({
        "checked_list": checked_list
    })


def check_box_state_change_2(state):
    if state == 2:
        checked_list[2] = True
    else:
        checked_list[2] = False
    # 更新设置
    update_settings({
        "checked_list": checked_list
    })


def check_box_state_change_3(state):
    if state == 2:
        checked_list[3] = True
    else:
        checked_list[3] = False
    # 更新设置
    update_settings({
        "checked_list": checked_list
    })


def check_box_state_change_4(state):
    if state == 2:
        checked_list[4] = True
    else:
        checked_list[4] = False
    # 更新设置
    update_settings({
        "checked_list": checked_list
    })


def check_box_state_change_5(state):
    if state == 2:
        checked_list[5] = True
    else:
        checked_list[5] = False
    # 更新设置
    update_settings({
        "checked_list": checked_list
    })


def check_box_state_change_6(state):
    if state == 2:
        checked_list[6] = True
    else:
        checked_list[6] = False
    # 更新设置
    update_settings({
        "checked_list": checked_list
    })


def daily_setting_mail(state):
    if state == 2:
        daily_setting[2] = True
    else:
        daily_setting[2] = False
    # 更新设置
    update_settings({
        "daily_setting": daily_setting
    })


def daily_setting_fleet(state):
    if state == 2:
        daily_setting[1] = True
    else:
        daily_setting[1] = False
    # 更新设置
    update_settings({
        "daily_setting": daily_setting
    })


def daily_setting_market(state):
    if state == 2:
        daily_setting[0] = True
    else:
        daily_setting[0] = False
    # 更新设置
    update_settings({
        "daily_setting": daily_setting
    })


def daily_setting_shana(state):
    if state == 2:
        daily_setting[3] = True
    else:
        daily_setting[3] = False
    # 更新设置
    update_settings({
        "daily_setting": daily_setting
    })


def daily_setting_online(state):
    if state == 2:
        daily_setting[4] = True
    else:
        daily_setting[4] = False
    # 更新设置
    update_settings({
        "daily_setting": daily_setting
    })


def message_info_append(message):
    logger.info(message)


def message_error_append(error):
    logger.error(error)


class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('auto_CoA')
        self.setWindowIcon(QIcon('icon.ico'))

        self.handler = QtHandler(self.plainTextEdit_log)
        self.logger = logger.add(self.handler,
                                 format="<green>{time:HH:mm:ss}</green> | "  # 颜色>时间
                                        "<level>{level}</level>: "  # 等级
                                        "<level>{message}</level>",  # 日志内容
                                 )

        # 设置图标
        self.TransparentToolButton_entry_game.setIcon(FIF.SETTING)
        self.TransparentToolButton_double_potion.setIcon(FIF.SETTING)
        self.TransparentToolButton_tili.setIcon(FIF.SETTING)
        self.TransparentToolButton_daily.setIcon(FIF.SETTING)
        self.TransparentToolButton_resources.setIcon(FIF.SETTING)
        self.TransparentToolButton_exchange.setIcon(FIF.SETTING)
        # 设置下拉框内容
        self.ComboBox_after_finish.setPlaceholderText("选择一个操作")
        items = ['退出auto_CoA', '退出auto_CoA和游戏']
        self.ComboBox_after_finish.addItems(items)
        self.ComboBox_after_finish.setCurrentIndex(-1)
        self.ComboBox_after_finish.currentTextChanged.connect(print)
        # 二级设置初始化
        self.frame_daily.hide()
        self.frame_tili.show()

        self.plainTextEdit_log.setReadOnly(True)
        self.PushButton_start.clicked.connect(self.start_btn)
        self.PushButton_stop.clicked.connect(self.stop_btn)
        self.PushButton_select_all.clicked.connect(self.select_all_btn)
        self.PushButton_clean_all.clicked.connect(self.clean_all_btn)
        self.TransparentToolButton_daily.clicked.connect(self.daily_setting_btn)
        self.TransparentToolButton_tili.clicked.connect(self.tili_setting_btn)
        # checkbox绑定方法
        self.CheckBox_open_game.stateChanged.connect(check_box_state_change_1)
        self.CheckBox_double_potion.stateChanged.connect(check_box_state_change_2)
        self.CheckBox_tili.stateChanged.connect(check_box_state_change_3)
        self.CheckBox_reward.stateChanged.connect(check_box_state_change_4)
        self.CheckBox_resources.stateChanged.connect(check_box_state_change_5)
        self.CheckBox_exchange.stateChanged.connect(check_box_state_change_6)

        self.CheckBox_receive_mail.stateChanged.connect(daily_setting_mail)
        self.CheckBox_gift_of_shana.stateChanged.connect(daily_setting_shana)
        self.CheckBox_market.stateChanged.connect(daily_setting_market)
        self.CheckBox_fleet.stateChanged.connect(daily_setting_fleet)
        self.CheckBox_online_gift.stateChanged.connect(daily_setting_online)
        # 设置初始勾选状态
        self.CheckBox_open_game.setChecked(checked_list[1])
        self.CheckBox_double_potion.setChecked(checked_list[2])
        self.CheckBox_tili.setChecked(checked_list[3])
        self.CheckBox_reward.setChecked(checked_list[4])
        self.CheckBox_resources.setChecked(checked_list[5])
        self.CheckBox_exchange.setChecked(checked_list[6])
        self.CheckBox_receive_mail.setChecked(checked_list[6])

        self.CheckBox_receive_mail.setChecked(daily_setting[2])
        self.CheckBox_gift_of_shana.setChecked(daily_setting[3])
        self.CheckBox_market.setChecked(daily_setting[0])
        self.CheckBox_fleet.setChecked(daily_setting[1])
        self.CheckBox_online_gift.setChecked(daily_setting[4])

        logger.info("欢迎使用auto_CoA")

    def start_btn(self):
        # 初始化消息窗口
        self.plainTextEdit_log.clear()
        # 点击后，再创建线程实例
        self.worker_thread = Worker_Thread(checked_list)
        self.worker_thread.finished_signal.connect(self.task_finished)
        self.worker_thread.message_signal.connect(message_info_append)
        self.worker_thread.error_signal.connect(message_error_append)
        logger.info("开始")
        if not self.worker_thread.isRunning():
            self.worker_thread.start()

    def stop_btn(self):
        self.worker_thread.stop()
        logger.info("正在停止...")
        while self.worker_thread.isRunning():
            time.sleep(1)
        logger.info("已停止")

    def task_finished(self):
        self.worker_thread.quit()

    def select_all_btn(self):
        global checked_list
        # 推导式把全部替换为True
        checked_list = [True for _ in checked_list]
        self.CheckBox_open_game.setChecked(checked_list[1])
        self.CheckBox_double_potion.setChecked(checked_list[2])
        self.CheckBox_tili.setChecked(checked_list[3])
        self.CheckBox_reward.setChecked(checked_list[4])
        self.CheckBox_resources.setChecked(checked_list[5])
        self.CheckBox_exchange.setChecked(checked_list[6])

    def clean_all_btn(self):
        global checked_list
        # 推导式把全部替换为True
        checked_list = [False for _ in checked_list]
        self.CheckBox_open_game.setChecked(checked_list[1])
        self.CheckBox_double_potion.setChecked(checked_list[2])
        self.CheckBox_tili.setChecked(checked_list[3])
        self.CheckBox_reward.setChecked(checked_list[4])
        self.CheckBox_resources.setChecked(checked_list[5])
        self.CheckBox_exchange.setChecked(checked_list[6])

    def daily_setting_btn(self):
        self.frame_daily.show()
        self.frame_tili.hide()

    def tili_setting_btn(self):
        self.frame_daily.hide()
        self.frame_tili.show()


if __name__ == '__main__':
    # 适配hidpi
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # 适配缩放比例
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    # 图片适配hidpi
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    w = App()
    w.show()

    sys.exit(app.exec())
