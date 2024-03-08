# 自定义Formatter，生成HTML格式的日志记录
import logging

from PyQt5.QtCore import QObject, pyqtSignal


class Stream(QObject):
    """
    自定义输出流，捕获 print 的输出
    """
    message = pyqtSignal(str)

    def write(self, message):
        # 发送html文本
        self.message.emit(str(message))

    def flush(self):
        pass


class HtmlFormatter(logging.Formatter):
    """
    捕获的输出转换为适合控件显示的html格式
    """
    formats = {
        logging.DEBUG: "gray",
        logging.INFO: "green",
        logging.WARNING: "orange",
        logging.ERROR: "red",
        logging.CRITICAL: "purple"
    }

    def __init__(self, fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"):
        super().__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record):
        # 通过logger等级获取对应颜色
        color = self.formats.get(record.levelno)
        # logger内容获取
        message = super().format(record)
        # 返回对应的html文本
        return f'<span style="color: {color};">{message}</span><br/>'


class LogMessageHandler(logging.Handler):
    """
    捕获 logger 的输出
    """

    def __init__(self, text_stream):
        super().__init__()
        self.text_stream = text_stream
        # 设置使用 HTML 格式化
        self.setFormatter(HtmlFormatter())

    def emit(self, record):
        # 调用format获取对应的html文本字符串
        msg = self.format(record)
        self.text_stream.write(msg)
