import streamlit as st

from knowledge_base import KnowledgeBaseService

st.title("RAG开发")

upload_file = st.file_uploader(
    label="请上传TXT文件",
    type=["txt"],
    accept_multiple_files=False, #仅支持一个文件上传
)

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if upload_file is not None:
    file_name = upload_file.name
    file_type = upload_file.type
    file_size = upload_file.size / 1024

    st.subheader(f"文件名:{file_name}")
    st.write(f"文件类型:{file_type},文件大小:{file_size:2f}KB")

    text = upload_file.getvalue().decode("utf-8")
    result = st.session_state["service"].upload_by_str(text, file_name)
    st.write(result)
