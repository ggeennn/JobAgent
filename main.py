import os
from dotenv import load_dotenv
from langchain_community.chat_models.litellm import ChatLiteLLM
from src.crews import JobAgentCrew

def main():
    load_dotenv()
    print("## 欢迎来到求职特工队 v2.0 ##")

    # 使用 LiteLLM，可以轻松切换云端高性能模型
    llm = ChatLiteLLM(
        # model="groq/llama3-8b-8192", 
        # api_key=os.environ.get("GROQ_API_KEY"),
        model="gemini/gemini-2.0-flash", 
        api_key=os.environ.get("GEMINI_API_KEY"),
        temperature=0.2
    )
    
    # 实例化并运行我们的求职特工队
    crew_result = JobAgentCrew(llm).run() 

    print("\n\n## 工作流执行完成! ##")
    print(crew_result)
    print("\n请检查项目根目录下的 'personal_meta_resource.md' 文件。")

if __name__ == "__main__":
    main()