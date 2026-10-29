import yaml
from utils.path_tool import get_abs_path
import os
from utils.logger_handler import logger

# str 转为 字典
def load_config(config_path, encoding='utf-8'):
    if not os.path.exists(config_path):
        logger.error(f'[参数提取]文件{config_path}不存在')
        raise FileNotFoundError(f"配置文件不存在，请检查路径: {config_path}")

    with open(file=config_path, mode='r', encoding=encoding) as f:
        return yaml.load(stream=f, Loader=yaml.FullLoader)

rag_config = load_config(get_abs_path('config/rag.yml'))
chroma_config = load_config(get_abs_path('config/chroma.yml'))
prompts_config = load_config(get_abs_path('config/prompts.yml'))
agent_config = load_config(get_abs_path('config/agent.yml'))