'''
向量数据库
'''
from langchain_chroma import Chroma
import os

from langchain_core.documents import Document

from 智能体项目.model.factory import embed_model
from 智能体项目.utils.config_handler import chroma_config
from 智能体项目.utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
from 智能体项目.utils.logger_handler import logger
from 智能体项目.utils.path_tools import get_abs_path
from langchain_text_splitters import RecursiveCharacterTextSplitter


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_config['collection_name'],
            embedding_function=embed_model,
            persist_directory=get_abs_path(chroma_config['persist_directory']),
        )

        self.spliter=RecursiveCharacterTextSplitter(
            chunk_size=chroma_config['chunk_size'],
            chunk_overlap=chroma_config['chunk_overlap'],
            separators=chroma_config['separators'],
            length_function=len
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={'k': chroma_config['k']})

    def load_document(self):

        def check_md5_hex(md5_for_check:str):
            if not os.path.exists(get_abs_path(chroma_config['md5_hex_store'])):
                open(get_abs_path(chroma_config['md5_hex_store']),'w',encoding='utf-8').close()
                return False

            with open(get_abs_path(chroma_config['md5_hex_store']),'r',encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True
                return False

        def save_md5_hex(md5_for_check:str):
            with open(get_abs_path(chroma_config['md5_hex_store']),'a',encoding='utf-8') as f:
                f.write(md5_for_check + '\n')

        def get_file_documents(read_path:str):
            if read_path.endswith('.txt'):
                return txt_loader(read_path)
            if read_path.endswith('.pdf'):
                return pdf_loader(read_path)
            return []

        allow_file_path:tuple[str] = listdir_with_allowed_type(
            get_abs_path(chroma_config['data_path']),
            tuple(chroma_config['allow_knowledge_file_type'])
        )

        for file_path in allow_file_path:
            md5_hex = get_file_md5_hex(file_path)
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{file_path}内容已经存在于知识库中")
                continue

            try:
                documents:list[Document] = get_file_documents(file_path)

                if not documents:
                    logger.warning(f'[加载知识库]{file_path}文件内没有有效内容')
                    continue

                split_documents:list[Document] = self.spliter.split_documents(documents)
                if not split_documents:
                    logger.warning(f'[加载知识库]{file_path}文件内没有有效内容')
                    continue

                self.vector_store.add_documents(split_documents)
                save_md5_hex(md5_hex)
                logger.info(f'[加载知识库]{file_path}文件内容已上传')

            except Exception as e:
                logger.error(f'[加载知识库]{file_path}加载失败，原因：{str(e)}',exc_info=True)


if __name__ == '__main__':
    vs = VectorStoreService()
    vs.load_document()
    retriever = vs.get_retriever()
    res = retriever.invoke("魔法")

    for r in res:
        print(r.page_content)
        print('-'*20)



