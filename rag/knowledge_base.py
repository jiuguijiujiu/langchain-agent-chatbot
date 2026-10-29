import os
from utils.logger_handler import logger
import hashlib
from utils.path_tool import get_abs_path
from utils.config_handler import chroma_config
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from utils.model_factory import embedding_model
from utils.file_handler import pdf_loader, text_loader, listdir_with_allowed_type

# 将文件内容转为md5值
def file_to_md5(file_path):
    if not os.path.exists(file_path):
        logger.error(f"[md5计算]文件{file_path}不存在")
        return None

    if not os.path.isfile(file_path):
        logger.error(f"[md5计算]路径{file_path}不是文件")
        return None

    md5_obj = hashlib.md5()
    chunk_size = 4096
    try:
        with open(file=file_path, mode="rb") as f:
            while chunk:= f.read(chunk_size):
                md5_obj.update(chunk)

            md5_str = md5_obj.hexdigest()
            return md5_str
    except Exception as e:
        logger.error(f"计算文件{file_path}md5失败，{str(e)}")
        return None

# 检测md5值是否重复
def check_md5(md5_str):
    md5_path = get_abs_path(chroma_config["md5_path"])
    dir_name = os.path.dirname(md5_path)
    if dir_name:
        os.makedirs(name=dir_name, exist_ok=True)

    if not os.path.exists(md5_path):
        open(file=md5_path, mode="w", encoding='utf-8').close()
        return False

    with open(file=md5_path, mode="r", encoding='utf-8') as f:
        for line in f:
            if md5_str == line.strip():
                return True

    return False

# 保存md5
def save_md5(md5_str):
    md5_path = get_abs_path(chroma_config["md5_path"])
    dir_name = os.path.dirname(md5_path)
    if dir_name:
        os.makedirs(name=dir_name, exist_ok=True)

    with open(file=md5_path, mode="a", encoding='utf-8') as f:
        f.write(md5_str + '\n')

# 知识库类
class KnowledgeBase:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = chroma_config["chunk_size"],
            chunk_overlap = chroma_config["chunk_overlap"],
            separators = chroma_config["separators"],
            length_function = len
        )

        persist_directory = get_abs_path(chroma_config["persist_directory"])
        os.makedirs(name=persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name = chroma_config["collection_name"],
            embedding_function = embedding_model,
            persist_directory = persist_directory,
        )

    # 获取检索器对象
    def get_retriever(self):
        return self.chroma.as_retriever(search_kwargs={'k':chroma_config["k"]})

    # 将文件内容导入向量库
    def store_knowledge(self):
        # 利用文件加载器加载文件
        def get_file_documents(file_path):
            if file_path.endswith(".txt"):
                return text_loader(file_path)

            if file_path.endswith(".pdf"):
                return pdf_loader(file_path)

            return []

        # 提取要存储的文件列表
        file_paths = listdir_with_allowed_type(
            path = get_abs_path(chroma_config["data_path"]),
            allowed_types = chroma_config["allow_knowledge_file_type"]
        )

        # 每个文件进行循环处理
        for file_path in file_paths:
            # 转为 md5
            md5_str = file_to_md5(file_path=file_path)
            # 检测 md5是否重复
            if check_md5(md5_str):
                logger.info(f"[加载知识库]{file_path}内容已经存在知识库内，跳过")
                continue

            try:
                # 加载器 加载文件内容，返回list[Document]
                documents = get_file_documents(file_path=file_path)
                if not documents:
                    logger.warning(f"[加载知识库]{file_path}内没有有效文本内容，跳过")
                    continue

                # 分割器 分割list[Document]
                split_documents = self.splitter.split_documents(documents)
                if not split_documents:
                    logger.warning(f"[加载知识库]{file_path}分片后没有有效文本内容，跳过")
                    continue

                # Chroma存储 list[Document]
                self.chroma.add_documents(split_documents)
                # 保存md5值到 md5文件中
                save_md5(md5_str)
                logger.info(f"[加载知识库]{file_path} 内容加载成功")
            except Exception as e:
                logger.error(f"[加载知识库]{file_path}加载失败：{str(e)}", exc_info=True)
                continue

if __name__ == '__main__':
    kb = KnowledgeBase()
    kb.store_knowledge()

    retriever = kb.get_retriever()
    res = retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("-"*20)