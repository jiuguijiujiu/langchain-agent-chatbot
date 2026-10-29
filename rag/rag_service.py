from langchain_core.runnables import RunnableLambda
from utils.model_factory import chat_model
from langchain_core.prompts import PromptTemplate
from utils.prompt_loader import load_rag_prompts
from rag.knowledge_base import KnowledgeBase
from langchain_core.output_parsers import StrOutputParser

# 输出提示词函数
def print_prompt(prompt):
    print("=" * 100)
    print(prompt.to_string())
    print("=" * 100)
    print("=" * 100)
    return prompt

class RagService:
    def __init__(self):
        self.chat_model = chat_model
        self.prompt_template = PromptTemplate.from_template(load_rag_prompts())
        self.retriever = KnowledgeBase().get_retriever()
        self.chain = self.__get_chain()

    def __get_chain(self):
        return self.prompt_template | RunnableLambda(print_prompt) | self.chat_model | StrOutputParser()

    # 检索器检索动作实现
    def retrieval(self, query):
        return self.retriever.invoke(query)

    def rag(self, query):
        # 检索器检索
        list_documents = self.retrieval(query)
        # 处理检索结果
        content = ''
        counter = 0
        for document in list_documents:
            counter += 1
            content += f"【参考资料{counter}】: 参考资料：{document.page_content} | 参考元数据：{document.metadata}\n"

        # 调用self.chain
        return self.chain.invoke({'input': query, 'content': content})

if __name__ == '__main__':
    rag = RagService()
    print(rag.rag("小户型适合哪些扫地机器人"))