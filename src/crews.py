from crewai import Crew, Process
from src.agents import JobAgentAgents
from src.tasks import JobAgentTasks
from src.tools.custom_tools import FileReaderTool, FileWriterTool

class JobAgentOrchestrator:
    def __init__(self, llm):
        self.agents = JobAgentAgents(llm)
        self.tasks = JobAgentTasks()

    def run_conversational_crew(self):
        """运行对话特工队，只负责聊天和记录。"""
        
        # 创建一个“赤手空拳”的对话专家，它没有任何工具，不会误操作
        advisor_agent = self.agents.personal_brand_advisor()
        
        print("--- 启动“个人品牌顾问”对话 ---")
        print("--- 我会记住我们的每一次对话。输入 '结束对话并保存' 来完成本次访谈。 ---")

        # 尝试读取现有元资源库，作为对话的开场记忆
        try:
            initial_context = FileReaderTool()._run("personal_brand_assets.md")
        except:
            initial_context = "这是我们的第一次对话。"
        
        conversation_history = [f"系统初始记忆:\n{initial_context}"]
        print(conversation_history[0])

        # 启动对话循环
        while True:
            user_input = input("\n> ")
            if user_input.lower() in ["结束对话并保存", "quit", "exit"]:
                print("\n好的，对话结束。现在开始为您总结...")
                return "\n".join(conversation_history)

            conversation_history.append(f"求职者: {user_input}")
            
            context_for_task = "\n".join(conversation_history)
            convo_task = self.tasks.conversational_task(advisor_agent, context_for_task)
            
            temp_crew = Crew(agents=[advisor_agent], tasks=[convo_task], verbose=False)
            ai_response = temp_crew.kickoff()
            
            print(f"\n个人品牌顾问: {ai_response}")
            conversation_history.append(f"个人品牌顾问: {ai_response}")

    def run_summarization_crew(self, full_conversation):
        """运行总结特工队，只负责分析对话并写入文件。"""
        
        # 创建一个持有“笔”的总结专家
        summarizer_agent = self.agents.personal_brand_advisor(tools=[FileWriterTool()])

        print("--- 启动“总结特工队” ---")
        
        # 在总结前，先读一次最新的文件内容
        existing_summary = FileReaderTool()._run("personal_brand_assets.md")
        
        summary_task = self.tasks.summary_and_save_task(
            agent=summarizer_agent,
            conversation_history=full_conversation,
            existing_summary=existing_summary
        )

        final_crew = Crew(
            agents=[summarizer_agent],
            tasks=[summary_task],
            process=Process.sequential,
            verbose=True
        )

        final_result = final_crew.kickoff()
        return final_result