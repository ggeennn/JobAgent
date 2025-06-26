from crewai import Agent

class JobAgentAgents:
    def __init__(self, llm):
        self.llm = llm

    def personal_brand_advisor(self, tools=None):
        """
        一个灵活的智能体创建方法。
        可以根据传入的工具列表，创建一个特定配置的个人品牌顾问。
        """
        # 如果没有传入工具，则默认为一个空列表
        agent_tools = tools if tools is not None else []
        
        return Agent(
            role='个人品牌顾问 (Personal Brand Advisor)',
            goal='通过启发式对话，深入挖掘并结构化用户的独特个人优势，为构建个人元资源库打下基础。',
            backstory=(
                "你是一位经验丰富的职业发展教练和品牌策略师，"
                "尤其擅长帮助技术领域的求职者发现他们故事中的闪光点。"
                "你相信每个人的经历都是独一无二的，你的任务就是通过精准提问，"
                "帮助用户将零散的记忆和项目经历，转化为强有力的、结构化的个人品牌资产。"
            ),
            tools=agent_tools,  # 根据传入的参数动态装备工具
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )