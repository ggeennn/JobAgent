from crewai import Crew, Process
from src.agents import JobAgentAgents
from src.tasks import JobAgentTasks

class JobAgentCrew:
    def __init__(self, llm):
        self.agents = JobAgentAgents(llm)
        self.tasks = JobAgentTasks()

    def run(self):
        # 实例化智能体
        advisor_agent = self.agents.personal_brand_advisor()

        # 模拟用户的第一次输入
        print("--- 启动“个人品牌顾问”对话 ---")
        user_initial_input = input("为了更好地为你打造个人品牌，请分享一个最近让你最有成就感的技术难题：\n> ")

        # 创建第一个对话任务
        discovery_task = self.tasks.brand_discovery_task(advisor_agent, user_initial_input)
        
        # 创建第二个文件写入任务
        resource_task = self.tasks.meta_resource_creation_task(advisor_agent)

        # 组建特工队
        crew = Crew(
            agents=[advisor_agent],
            tasks=[discovery_task, resource_task], # 任务将按顺序执行
            process=Process.sequential,
            verbose=True
        )

        # 启动任务
        result = crew.kickoff()
        return result