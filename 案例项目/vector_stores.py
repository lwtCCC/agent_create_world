
import config_data as config
from langchain_chroma import Chroma

class VectorStoreService(object):
    def __init__(self, embedding):
        self.embedding = embedding
        self.vector_store = Chroma(
            embedding_function=self.embedding,
            collection_name=config.collection_name,
            persist_directory=config.persist_directory,
        )

    def get_retriever(self):
        '''返回向量检索器'''
        return self.vector_store.as_retriever(search_kwargs={"k":config.similarity_threshold})