from ruamel.yaml import YAML
from pylnk3 import Lnk
import time
import sys
import os


class Config:
    _instance = None

    # 的是确保这个类只实例化一次，无论你尝试创建多少次对象。这对于管理全局配置、日志记录或数据库连接等场景非常有用
    def __new__(cls, version_path, config_example_path, config_path):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.yaml = YAML()
            cls._instance.version = cls._instance._version(version_path)
            cls._instance.config = cls._instance._default_config(config_example_path)
            cls._instance.config_path = config_path
        return cls._instance

    @staticmethod
    def _version(version_path):
        try:
            with open(version_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"未找到版本文件夹:{version_path}")
            time.sleep(3)
            sys.exit(1)

    def save_config(self):
        with open(self.config_path, 'w', encoding='utf-8') as file:
            self.yaml.dump(self.config, file)

    def _default_config(self, config_example_path):
        try:
            with open(config_example_path, 'r', encoding='utf-8') as file:
                loaded_config = self.yaml.load(file)
                if loaded_config:
                    return loaded_config
        except FileNotFoundError:
            print(f"未找到默认设置，请检查config_example_path：{config_example_path}")
            time.sleep(3)
            sys.exit(1)

    def _load_config(self, path=None):
        # 如果没有提供路径就用默认的路径
        path = self.config_path if path is None else path
        try:
            with open(path, 'r', encoding='utf-8') as file:
                loaded_config = self.yaml.load(file)
                if loaded_config:
                    self._detect_game_path(loaded_config)
                    self.config.update(loaded_config)
                    self.save_config()
        except FileNotFoundError:
            self.save_config()
        except Exception as e:
            print(f"Error loading YAML config from {path}: {e}")

    # 检测游戏路径
    def _detect_game_path(self, config):
        game_path = config['game_path']
        if os.path.exists(game_path):
            # 如果路径存在，则直接返回退出
            return
        start_menu_path = os.path.join(
            os.environ["ProgramData"], "Microsoft", "Windows", "Start Menu", "Programs", "晶核：魔导觉醒")
        # 尝试从开始菜单打开
        try:
            with open(os.path.join(start_menu_path, "晶核：魔导觉醒.lnk"), "rb") as lnk_file:
                lnk = Lnk(lnk_file)
                print(f"lnk:{lnk}")
                print(f"lnk.work_dir:{lnk.work_dir}")
                program_config_path = os.path.join(lnk.work_dir, "config.ini")
        # 没在开始菜单找到
        except Exception as e:
            print(f"没有找到游戏路径：{e}")
        if os.path.exists(program_config_path):
            with open(program_config_path, 'r', encoding='utf-8') as file:
                for line in file.readlines():
                    if line.startswith("game_install_path="):
                        game_path = line.split('=')[1].strip()
                        if os.path.exists(game_path):
                            config['game_path'] = os.path.join(game_path, "StarRail.exe")
                            return

    def get_value(self, key, default=None):
        return self.config.get(key, default)

    def set_value(self, key, value):
        self._load_config()
        self.config[key] = value
        self.save_config()

    def save_timestamp(self, key):
        self.set_value(key, time.time())
