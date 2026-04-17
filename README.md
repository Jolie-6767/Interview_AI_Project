# Interview_AI_Project
🤖 基于 RAG 的智能面试助手 (AI+HR 场景探索)

🌟 项目简介
本项目是一个探索 生成式 AI 在人力资源场景落地 的实验性案例。通过 RAG (检索增强生成) 技术，解决了大模型在处理特定企业知识库时的“幻觉”问题，为面试官提供精准的追问建议和背景核实。

🚀 核心功能
多源文档解析：支持 PDF/Word/Markdown 等格式的简历与岗位说明书上传。
精准语义检索：基于 FAISS 向量数据库，实现毫秒级知识匹配。
对话链路优化：采用 LangChain 构建长对话记忆，确保面试追问的连贯性。
交互式 UI：使用 Streamlit 搭建，支持即时预览与问答。

🛠️ 技术栈
LLM: DeepSeek-V3 / OpenAI API
框架: LangChain, Python 3.9+
向量库: FAISS
前端: Streamlit

📺 演示预览
