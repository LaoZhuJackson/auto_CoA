# coding: utf-8
import os
import sys
from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """
    HOME_INTERFACE = "home_interface"
    FUNCTION_INTERFACE = "function_interface"
    LOG_INTERFACE = "log_interface"

    LINK_CARD = "link_card"
    SAMPLE_CARD = "sample_card"
    ICON_INTERFACE = "icon_interface"
    VIEW_INTERFACE = "view_interface"
    SETTING_INTERFACE = "setting_interface"
    GALLERY_INTERFACE = "gallery_interface"
    NAVIGATION_VIEW_INTERFACE = "navigation_view_interface"

    TASKS_INTERFACE = "tasks_interface"
    FAQ_INTERFACE = "faq_interface"
    Tutorial_INTERFACE = "tutorial_interface"
    CHANGELOGS_INTERFACE = "changelogs_interface"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        # 为了保证图标在开发和打包后都能够使用，你需要正确地检测图标路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的应用，使用系统的绝对路径
            basedir = sys._MEIPASS
        else:
            # 如果是开发中的代码，使用当前目录的相对路径
            basedir = '.'
        return os.path.join(basedir, f"assets/app/qss/{theme.value.lower()}/{self.value}.qss")
