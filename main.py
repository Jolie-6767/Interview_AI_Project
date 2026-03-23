import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. 加载 .env 配置
load_dotenv()

# 2. 初始化客户端 (适配通义千问)
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)

try:
    print("🚀 正在连接通义千问大模型...\n")

    # 3. 发起请求
    response = client.chat.completions.create(
        model="qwen-plus",  # 通义千问的主力模型，通常有免费额度
        messages=[
            {"role": "system", "content": "你是一位专业的 Java 技术专家。"},
            {"role": "user", "content": "请用通俗易懂的话解释什么是 Java 的封装？"}
        ],
        stream=True
    )

    # 4. 打印回答
    print("💡 千问的回答：")
    for chunk in response:
        # 注意：兼容模式下，我们要确保获取到内容
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

except Exception as e:
    print(f"\n❌ 还是出错了：{e}")
    print("排查建议：1. 检查 API Key 是否正确；2. 确认阿里云百炼里的 'qwen-plus' 模型是否已开通。")
# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
