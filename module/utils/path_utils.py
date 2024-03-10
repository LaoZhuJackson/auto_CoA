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
            # 为了保证图标在开发和打包后都能够使用，你需要正确地检测图标路径
            # 如果是打包后的应用，使用系统的绝对路径
            basedir = sys._MEIPASS
        return basedir
