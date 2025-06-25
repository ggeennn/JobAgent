from textwrap import dedent
from crewai import Task

class JobAgentTasks:
    def brand_discovery_task(self, agent, user_input):
        return Task(
            description=dedent(f"""
                你正在与一位求职者进行对话。这是他们刚刚分享的一段关于他们有成就感的技术经历：
                ---
                {user_input}
                ---

                你的任务是：
                1.  用一句话总结这段经历的核心亮点。
                2.  基于这个亮点，提出一个有深度的、开放式的追问，以挖掘更多关于求职者解决问题能力的细节。
            """),
            expected_output=dedent("""
                一个包含两部分的文本：
                1.  对用户经历的简短总结。
                2.  一个能引导用户进行更深层次思考的追问。
            """),
            agent=agent
        )

    def meta_resource_creation_task(self, agent):
        # 注意：这个任务没有直接的description，因为它依赖于上一个任务的输出作为上下文。
        return Task(
            description="将前面对话中总结出的用户经历亮点和追问，结构化地写入到个人元资源库文件中。确保格式清晰，便于未来查阅。",
            expected_output="调用FileWriterTool成功后的确认信息。",
            agent=agent,
            # context 允许我们将上一个任务的输出传递给这个任务
            # 我们将在crews.py中指定它的具体内容
            context=[] 
        )