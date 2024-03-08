from qfluentwidgets import (ComboBox, SettingCard, FluentIconBase)
from typing import Union
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from managers.config_manager import config


class ComboBoxSettingCard2(SettingCard):
    """ Setting card with a combo box """

    def __init__(self, configname: str, icon: Union[str, QIcon, FluentIconBase], title, content=None, texts=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.configname = configname
        self.comboBox = ComboBox(self)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        for key, value in texts.items():
            self.comboBox.addItem(key, userData=value)
            # 从配置文件中获取保存的设置
            if value == config.get_item(configname):
                self.comboBox.setCurrentText(key)

        self.comboBox.currentIndexChanged.connect(self._onCurrentIndexChanged)

    def _onCurrentIndexChanged(self, index: int):
        # 检测到更新后保存到设置中
        config.set_value(self.configname, self.comboBox.itemData(index))
