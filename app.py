import streamlit as st
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.dashscope import DashScopeEmbedding

# 1. 页面配置（网页标签和图标）
st.set_page_config(page_title="AI 面试助手", page_icon="🤖")
st.title("💬 我的私有 AI 面试助手")
st.caption("基于 LlamaIndex + 通义千问 + Streamlit 构建")

# 2. 初始化后台 AI 配置
load_dotenv()


@st.cache_resource  # 这个装饰器能让模型只加载一次，不用每次刷新网页都重连
def init_index():
    Settings.llm = OpenAILike(
        model="qwen-plus",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        api_base=os.getenv("DASHSCOPE_BASE_URL"),
        is_chat_model=True,
        context_window=4096
    )
    Settings.embed_model = DashScopeEmbedding(
        model_name="text-embedding-v2",
        api_key=os.getenv("DASHSCOPE_API_KEY")
    )

    # 读取 data 文件夹
    documents = SimpleDirectoryReader("./data").load_data()
    return VectorStoreIndex.from_documents(documents)


index = init_index()
query_engine = index.as_query_engine()

# 3. 构建聊天界面
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史聊天记录
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入框
if prompt := st.chat_input("问问关于我文档里的内容..."):
    # 记录并显示用户提问
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 记录并显示 AI 回答
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = query_engine.query(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": str(response)})