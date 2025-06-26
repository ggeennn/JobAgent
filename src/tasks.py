from textwrap import dedent
from crewai import Task

class JobAgentTasks:
    def conversational_task(self, agent, context):
        """一个在循环中不断进行的对话任务"""
        return Task(
            description=dedent(f"""
                你正在与一位求职者进行深度对话，以挖掘他们的个人亮点。
                这是到目前为止的对话记录：
                ---
                {context}
                ---
                你的任务是分析整个对话的上下文，然后提出一个最能引导对话走向深入的、开放式的追问。
                你的回答必须只能是问题本身，不要包含任何客套话或前缀。
            """),
            expected_output="一个精准的、能引导对话向更深层次发展的追问。",
            agent=agent
        )

    def summary_and_save_task(self, agent, conversation_history, existing_summary):
        """一个专门用于总结和保存的任务"""
        return Task(
            description=dedent(f"""
                分析下方提供的“现有总结”和“最新对话记录”。
                你的任务是，将“最新对话记录”中的新信息，以智能的方式整合进“现有总结”中，形成一份更全面、更丰富的最终版本。
                最终版本必须严格基于所提供的所有信息，不允许添加任何外部信息。
                最后，调用文件写入工具，将这份最终的、完整的总结写入到 'personal_brand_assets.md' 文件中。

                ---
                现有总结:
                {existing_summary}
                ---
                最新对话记录:
                {conversation_history}
                ---
            """),
            expected_output="调用文件写入工具成功后的确认信息。",
            agent=agent
        )