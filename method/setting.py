import json
import os

json_path = "config\\config.json"


def relative_to_absolute(relative_path: str):
    # 获取当前脚本文件所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取上一层目录的绝对路径
    parent_directory = os.path.abspath(os.path.join(script_dir, '..'))
    # 构建图片文件的绝对路径
    absolute_path = os.path.join(parent_directory, relative_path)
    return absolute_path


def save_settings(settings_dict: dict):
    file_path = relative_to_absolute(json_path)
    with open(file_path, 'w') as json_file:
        json.dump(settings_dict, json_file, indent=4)


def load_settings():
    file_path = relative_to_absolute(json_path)
    try:
        with open(file_path, 'r') as json_file:
            settings_dict = json.load(json_file)
            return settings_dict
    except FileNotFoundError:
        # 如果文件不存在，返回一个默认的设置字典
        return {}


def update_settings(new_settings: dict):
    current_settings = load_settings()
    current_settings.update(new_settings)
    save_settings(current_settings)

# # 示例：保存用户设置到 JSON 文件
# user_settings = {
#     "version": "1.0.0",
#     "font_size": 14,
#     "CoA_path": "D:\\Game\\CoA\\晶核：魔导觉醒.exe"
# }
#
# new_setting = {
#     "font_size": 15,
#     "haha": 13
# }
#
# path = relative_to_absolute("config\\config.json")
# print(path)
# save_settings(user_settings, path)
#
# # 示例：从 JSON 文件加载用户设置
# loaded_settings = load_settings(path)
# print("Loaded Settings:", loaded_settings)
#
# update_settings(new_setting, path)
#
# loaded_settings = load_settings(path)
# print("Loaded Settings:", loaded_settings)
#
# print(load_settings("config\\config.json")["CoA_path"])
