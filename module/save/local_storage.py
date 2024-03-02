import json


class LocalStorage:
    """
    本地存储对象
    """

    def __init__(self, name):
        self.__json_file = name + ".json"

        try:
            with open(self.__json_file, "r") as json_file:
                self.__dict = json.load(json_file)
        except FileNotFoundError:
            self.__dict = {}

    def set_item(self, key, value):
        """
        存储数据
        """
        self.__dict[key] = value
        self._save()

    def get_item(self, key: str, default=None):
        """
        读取数据
        """
        return self.__dict.get(key, default)

    def remove_item(self, key):
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
