import os

# 获取项目根目录
def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取项目中文件绝对路径
def get_abs_path(relative_path):
    return os.path.join(get_project_root(), relative_path)