import os

import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import datetime

from dotenv import load_dotenv

load_dotenv()  # 这会加载项目根目录下的 .env 文件

def check_md5(md5_str:str):
    if not os.path.exists(config.md5_path):

        open(config.md5_path,'w',encoding="utf-8").close()

        return False
    else:
        for line in open(config.md5_path, 'r', encoding="utf-8").readlines():
            line = line.strip()
            if md5_str == line:
                return True

        return False


def save_md5(md5_str:str):
    with open(config.md5_path,'w',encoding="utf-8") as f:
        f.write(md5_str+"\n")

def get_md5(input_str:str,encoding="utf-8"):

    str_bytes = input_str.encode(encoding)
    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)
    return md5_obj.hexdigest()

class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory,exist_ok=True)

        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory,
        )  #向量存储实例
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len
        )  #文档分割器

    def upload_by_str(self,data:str,filename):
        #将传入的字符串向量化存入数据库
        md5_hex = get_md5(data)

        if check_md5(md5_hex):
            return "[重复]内容已上载数据库"

        if len(data) > config.max_split_char_number:
            knowledge_chunks:list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata ={
            "source": filename,
            "create_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"小明"
        }

        self.chroma.add_texts(
            texts=knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],
        )

        save_md5(md5_hex)

        return "[成功]内容已上载数据库"

if __name__ == '__main__':
    service = KnowledgeBaseService()
    service.upload_by_str("季非雪","textfile")
