'''
模型工厂
'''
from abc import ABC,abstractmethod
from typing import Optional

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models import ChatTongyi
from 智能体项目.utils.config_handler import rag_config
from dotenv import load_dotenv
import os

load_dotenv()

class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(
            model=rag_config['chat_model_name'],
            api_key=os.environ.get('DASHSCOPE_API_KEY')
        )

class EmbeddingModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(
            model=rag_config['embedding_model_name'],
            dashscope_api_key=os.environ.get('DASHSCOPE_API_KEY')
        )

chat_model = ChatModelFactory().generator()
embed_model = EmbeddingModelFactory().generator()