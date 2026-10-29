from utils.path_tool import get_abs_path
import os
import logging
from datetime import datetime

# 获取日志存储根目录
LOG_ROOT = get_abs_path(relative_path='logs')

# 创建日志存储根目录
os.makedirs(name=LOG_ROOT, exist_ok=True)

# 设置日志格式
DEFAULT_LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

# 设置日志处理器
def get_logger(
        name = 'Agent',
        console_level = logging.INFO,
        file_level = logging.DEBUG,
        log_path = None
):
    # 创建日志处理器对象
    logger = logging.getLogger(name=name)
    logger.setLevel(level=logging.DEBUG)

    if logger.handlers:
        return logger

    # 创建与设置 控制台handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt=DEFAULT_LOG_FORMAT)
    console_handler.setLevel(level=console_level)
    logger.addHandler(console_handler)

    # 创建与设置 文件handler
    if not log_path:
        log_path = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.FileHandler(filename=log_path, encoding='utf-8')
    file_handler.setFormatter(fmt=DEFAULT_LOG_FORMAT)
    file_handler.setLevel(level=file_level)
    logger.addHandler(file_handler)

    return logger

# 创建日志处理器
logger = get_logger()