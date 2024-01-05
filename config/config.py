from qfluentwidgets import QConfig, ConfigItem, qconfig, ColorConfigItem


class Config(QConfig):
    all_character = ConfigItem("User", "all_character", '1')
    coa_window_name = ConfigItem("Game", "coa_window_name", '晶核：魔导觉醒')
    checked_list = ConfigItem("Setting", "checked_list", [False, False, False,False, False, False, False])


VERSION = "0.0.1"
font_size = 15
CoA_path = "D:\\Game\\CoA\\\u6676\u6838\uff1a\u9b54\u5bfc\u89c9\u9192.exe"
# checked_list = [False, False, False, False, False, False, False]
# message = "\u6b22\u8fce\u4f7f\u7528auto_CoA\n"

cfg = Config()
# qconfig.themeColor = ColorConfigItem("QFluentWidgets", "ThemeColor", '#70d5f3')
qconfig.load('config.json', cfg)
