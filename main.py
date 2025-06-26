import os
from dotenv import load_dotenv
from langchain_community.chat_models.litellm import ChatLiteLLM
from src.crews import JobAgentOrchestrator

def main():
    load_dotenv()
    print("## 欢迎来到求职特工队 v2.0 ##")

    llm = ChatLiteLLM(
        model="gemini/gemini-2.0-flash", 
        api_key=os.environ.get("GEMINI_API_KEY"),
        # model="groq/llama3-8b-8192",
        # api_key=os.environ.get("GROQ_API_KEY"),
        temperature=0.2
    )
    
    # 实例化总编排器
    orchestrator = JobAgentOrchestrator(llm)

    # 第一步：运行对话流程
    conversation_result = orchestrator.run_conversational_crew()

    # 第二步：如果对话有内容，则运行总结流程
    if conversation_result:
        summary_result = orchestrator.run_summarization_crew(conversation_result)
        
        print("\n\n## 工作流执行完成! ##")
        print(summary_result)
        print("\n请检查项目根目录下的 'personal_brand_assets.md' 文件，查看最新的个人元资源库。")
    else:
        print("\n## 对话未开始，程序已退出。 ##")


if __name__ == "__main__":
    main()