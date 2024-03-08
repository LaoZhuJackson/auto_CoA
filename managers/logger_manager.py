import logging

from module.logger.logger import Stream, LogMessageHandler

# 日志处理器绑定到自定义流
text_stream = Stream()
handler = LogMessageHandler(text_stream)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
