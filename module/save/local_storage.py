import json
import logging


class LocalStorage:
    """
    本地存储对象
    """

    def __init__(self, json_file="user_default.json"):
        self.json_file = json_file
        try:
            with open(self.json_file, "r") as json_file:
                self.dict = json.load(json_file)
        except FileNotFoundError:
            logging.error(self.json_file, "文件不存在")

    def set_item(self, key, value):
        """
        存储数据
        """
        self.dict[key] = value
        self._save()

    def get_item(self, key, default=None):
        """
        读取数据
        """
        return self.dict.get(key, default)

    def remove_item(self, key):
        """
        移除键值对
        """
        if key in self.dict:
            del self.dict[key]
            self._save()

    def clear(self):
        """
        清空数据
        """
        self.dict = {}
        self._save()

    def _save(self):
        with open(self.json_file, "w") as json_file:
            json.dump(self.dict, json_file, indent=4)
