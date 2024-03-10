import json
import os
import sys
from typing import Any


class LocalStorage:
    """
    本地存储对象
    """

    def __init__(self, name: str):
        # 为了保证图标在开发和打包后都能够使用，你需要正确地检测图标路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的应用，使用系统的绝对路径
            basedir = sys._MEIPASS
        else:
            # 如果是开发中的代码，使用当前目录的相对路径
            basedir = '.'
        self.__json_file = name + ".json"
        self.__json_file = os.path.join(basedir, self.__json_file)
        try:
            with open(self.__json_file, "r") as json_file:
                self.__dict = json.load(json_file)
        except FileNotFoundError:
            self.__dict = {}

    def set_item(self, key: str, value: Any):
        """
        存储数据
        """
        self.__dict[key] = value
        self._save()

    def get_item(self, key: str, default=None) -> Any:
        """
        读取数据
        """
        return self.__dict.get(key, default)

    def remove_item(self, key: str):
        """
        移除键值对
        """
        if key in self.__dict:
            del self.__dict[key]
            self._save()

    def clear(self):
        """
        清空数据
        """
        self.__dict = {}
        self._save()

    def _save(self):
        """
        保存
        """
        with open(self.__json_file, "w") as json_file:
            json.dump(self.__dict, json_file, indent=4)


sys.path.append("..\\..\\auto_CoA")
from module.base.singleton import Singleton


class LocalStorageMgr(Singleton):
    """
    本地存储管理器
    """

    def __init__(self):
        self.__storage_dict = {}

    def getLocalStorage(self, name="user_default") -> LocalStorage:
        """
        获取本地存储对象
        """
        if name not in self.__storage_dict:
            self.__storage_dict[name] = LocalStorage(name)
        return self.__storage_dict[name]
