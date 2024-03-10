import os
import sys


class PathUtils:
    """
    路径工具类
    """

    @staticmethod
    def get_base_dir():
        """
        获取根目录
        """
        basedir = "."
        if getattr(sys, "frozen", False):
            # 我们在一个 PyInstaller 打包的环境中运行。
            # 为了保证图标在开发和打包后都能够使用，你需要正确地检测图标路径
            basedir = getattr(sys, '_MEIPASS', ".")
        return basedir

    @staticmethod
    def get_path(relative_path: str):
        """
        获取路径
        """
        basedir = os.path.abspath(PathUtils.get_base_dir())
        return os.path.normpath(os.path.join(basedir, relative_path))
