'''
总结服务类
把知识和提问一起打包给模型
'''
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from 智能体项目.model.factory import chat_model
from 智能体项目.rag.vector_store import VectorStoreService
from 智能体项目.utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate


class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        chain = self.prompt_template | self.model | StrOutputParser()
        return chain

    def retriever_docs(self, query:str)->list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self, query:str)->str:

        context_docs = self.retriever_docs(query)

        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f'【参考资料{counter}】:参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n'

        return self.chain.invoke(
            {
                "input":query,
                "context":context,
            }
        )

if __name__ == '__main__':
    rag = RagSummarizeService()
    print(rag.rag_summarize("魔法的概念"))
