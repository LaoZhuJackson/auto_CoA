import logging

import pygetwindow as gw

from managers.config_manager import config
from module.operation.click import Click


def activate(is_running: bool):
    """
    激活游戏窗口使置顶
    :param is_running:
    :return:
    """
    game_path = config.get_item("game_path")
    game_name = game_path.split('\\')[-1]
    click = Click()
    try:
        coa_window = gw.getWindowsWithTitle(game_name)[0]
        # 激活窗口，使置顶
        coa_window.activate()
        # 再点击一下窗口标题
        click.common_click('receiving_resources\\title.png', is_running)
    except IndexError:
        logging.error("请先打开游戏启动器再运行")
