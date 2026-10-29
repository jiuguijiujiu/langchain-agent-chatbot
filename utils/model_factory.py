from abc import ABC, abstractmethod
from langchain_community.chat_models.tongyi import ChatTongyi
from utils.config_handler import rag_config
from langchain_community.embeddings import DashScopeEmbeddings

class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self):
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self):
        return ChatTongyi(model=rag_config['chat_model_name'])

class EmbeddingModelFactory(BaseModelFactory):
    def generator(self):
        return DashScopeEmbeddings(model=rag_config['embedding_model_name'])

# chat_model对象
chat_model = ChatModelFactory().generator()
# embedding_model对象
embedding_model = EmbeddingModelFactory().generator()