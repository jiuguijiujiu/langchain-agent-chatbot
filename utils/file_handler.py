import os
from utils.logger_handler import logger
from langchain_community.document_loaders import PyPDFLoader, TextLoader

# 返回文件夹内允许的文件列表
def listdir_with_allowed_type(path, allowed_types):
    allowed_types = tuple(allowed_types)
    files = []
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return ()

    for file_name in os.listdir(path):
        if file_name.endswith(allowed_types):
            files.append(os.path.join(path, file_name))
    return tuple(files)

# 返回pdf加载器加载结果
def pdf_loader(file_path, password=None):
    return PyPDFLoader(file_path=file_path, password=password).load()

# 返回txt加载器加载结果
def text_loader(file_path, encoding='utf-8'):
    return TextLoader(file_path=file_path, encoding=encoding).load()