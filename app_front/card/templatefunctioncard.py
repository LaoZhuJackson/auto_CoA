from typing import Union
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from qfluentwidgets import ExpandSettingCard, SwitchButton, \
    IndicatorPosition, LineEdit, FluentIconBase
from qfluentwidgets import FluentIcon as FIF


class TemplateFunctionCard(ExpandSettingCard):
    """ Expandable setting card """

    def __init__(self, title: str = '', content: str = None, parent=None, sub_view=None):
        super().__init__(FIF.CHECKBOX, title, content, parent)

        if sub_view is not None:
            self.expand_view = sub_view.Layout(self)
        else:
            self.expand_view = None

        self._adjustViewSize()
        self.__initWidget()

    def __initWidget(self):
        self.viewLayout.setSpacing(0)
        self.viewLayout.setAlignment(Qt.AlignTop)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        if self.expand_view is not None:
            self.viewLayout.addWidget(self.expand_view)
            self.expand_view.show()
        else:
            self.setExpand(False)
            self.card.expandButton.hide()
            self.card.setContentsMargins(0, 0, 30, 0)
        self._adjustViewSize()

    def setChecked(self, isChecked: bool):
        self.setValue(isChecked)
        # pass


class SimpleFunctionCard(ExpandSettingCard):
    """ Folder list setting card """

    def __init__(self, icon: Union[str, QIcon, FIF], sub_view, title: str = '', content: str = None, parent=None):
        super().__init__(icon, title, content, parent)
        self.expand_view = sub_view.Layout(self)
        # 调整视图大小
        self._adjustViewSize()
        self.__initWidget()

    def __initWidget(self):
        self.viewLayout.setSpacing(0)
        self.viewLayout.setAlignment(Qt.AlignTop)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        # Initialize layout
        self.viewLayout.addWidget(self.expand_view)
        self.expand_view.show()
        self._adjustViewSize()
