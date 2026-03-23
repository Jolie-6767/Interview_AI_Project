import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.dashscope import DashScopeEmbedding  # 新加的

# 加载配置
load_dotenv()

# 1. 配置 LLM
Settings.llm = OpenAI(
    # 把它改成 LlamaIndex 认识的名字，防止它报错
    model="gpt-3.5-turbo",
    # 实际上由于 base_url 指向了阿里，
    # 阿里会忽略这个 gpt-3.5 名字，直接用你 API Key 对应的默认权限，
    # 或者我们通过额外的参数强制指定
    additional_kwargs={"model": "qwen-plus"},
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    api_base=os.getenv("DASHSCOPE_BASE_URL"),
    is_chat_model=True
)
# 2. 配置 Embedding (直接用阿里云云端，不占内存不下载)
Settings.embed_model = DashScopeEmbedding(
    model_name="text-embedding-v2",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)


def start_rag():
    if not os.path.exists("./data") or not os.listdir("./data"):
        print("❌ 错误：data 文件夹不存在或里面没放文件！")
        return

    print("📚 正在读取文档并建立索引（第一次运行可能需要几秒）...")
    documents = SimpleDirectoryReader("./data").load_data()
    index = VectorStoreIndex.from_documents(documents)

    query_engine = index.as_query_engine()

    print("\n✅ 知识库就绪！请输入关于你文档的问题：")
    while True:
        question = input("User: ")
        if question.lower() in ['quit', 'exit', '退出']:
            break

        print("🤖 AI 正在思考...")
        response = query_engine.query(question)
        print(f"AI: {response}\n")


if __name__ == "__main__":
    start_rag()