# coding: utf-8
import os
import sys
from enum import Enum
from module.utils.path_utils import PathUtils
from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """Style sheet"""

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

        return os.path.join(
            PathUtils.get_base_dir(),
            f"assets/app/qss/{theme.value.lower()}/{self.value}.qss",
        )
