from qfluentwidgets import (ComboBox, SettingCard, FluentIconBase)
from typing import Union
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from managers.config_manager import config


class ComboBoxSettingCard1(SettingCard):
    """ Setting card with a combo box """

    def __init__(self, configName: str, icon: Union[str, QIcon, FluentIconBase], title, content=None, texts=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.configName = configName
        self.comboBox = ComboBox(self)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        for text, option in zip(texts, texts):
            self.comboBox.addItem(text, userData=option)
        # 如果没有该配置就创一个
        if config.get_item(self.configName) is None:
            # 将当前复选框的值（即复选框中的第一个值）赋值到配置中
            config.set_item(self.configName, self.comboBox.text())
        self.comboBox.setCurrentText(config.get_item(self.configName))
        self.comboBox.currentIndexChanged.connect(self._onCurrentIndexChanged)

    def _onCurrentIndexChanged(self, index: int):
        config.set_item(self.configName, self.comboBox.itemData(index))
