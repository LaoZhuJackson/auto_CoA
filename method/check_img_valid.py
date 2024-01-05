import os

from PIL import Image


def is_valid_image_path(image_path):
    try:
        # 尝试打开图片文件
        with Image.open(image_path) as img:
            # 图片成功打开
            return True
    except (FileNotFoundError, IOError):
        # 文件不存在或无法打开
        return False


# 输入的图片路径
# 获取当前脚本文件所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上一层目录的绝对路径
parent_directory = os.path.abspath(os.path.join(script_dir, '..'))
print(parent_directory)
user_input_path = 'image\\start_up\\start_tip.png'
# 构建图片文件的绝对路径
absolute_path = os.path.join(parent_directory, user_input_path)
print(absolute_path)

# 检查输入的图片路径是否有效
if is_valid_image_path(absolute_path):
    print("图片路径有效，可以成功打开图片。")
    # 这里可以添加进一步的代码
else:
    print("图片路径无效，无法打开图片。请检查路径是否正确。")
    # 这里可以添加进一步的代码
