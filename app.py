import ctypes
import os
import sys

os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False)
         else os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from app_front.main_window import MainWindow
import sys

# enable dpi scale
QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

sys.path.append("..\\auto_CoA")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
        # return True
    except:
        return False


if __name__ == "__main__":
    if not is_admin():
        # 以管理员身份重启进程，但会产生命令行窗口
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        # sys.exit()
    else:
        app = QApplication(sys.argv)
        app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

        w = MainWindow()

        sys.exit(app.exec_())
