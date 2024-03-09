from PyQt5.QtCore import QThread, pyqtSignal


class TaskThread(QThread):
    """
    创建一个线程类来运行任务
    """
    # 定义信号，用于通知GUI任务的完成或者停止
    finished = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, tasks):
        super(TaskThread, self).__init__()
        self.tasks = tasks
        self.is_running = False

    def run(self):
        self.is_running = True
        # 依次执行选中的任务
        for task in self.tasks:
            if self.is_running:
                task()  # 这里调用点击位置的函数
            else:
                break
        self.finished.emit()

    def stop(self):
        self.is_running = False
        self.stopped.emit()