# server_script.py
from fastmcp import FastMCP # 假设使用的是FastMCP 2.0+
# 或者 from mcp.server.fastmcp import FastMCP 如果是早期版本或官方SDK的mcp包 [7, 18]

# 1. 初始化MCP服务器，并指定一个名称
# 这个名称会在客户端配置中用到，用于识别此服务器
mcp_server = FastMCP(name="WILJobAgent") 

# 在 mcp_server = FastMCP(name="WILJobAgent") 之后，运行服务器之前

# 模拟的职位数据库 (初期硬编码)
mock_jobs_database = [
    {
        "id": "job2",
        "title": "QA Analyst Co-op",
        "company": "Finance Corp",
        "location": "Remote",
        "description": "Seeking a QA co-op student for testing financial software. Experience with Selenium is a plus.",
        "program_area": "Computer Programming and Analysis",
        "keywords": ["qa", "testing", "selenium", "finance", "co-op"]
    },
    {
        "id": "job3",
        "title": "Application Developer WIL",
        "company": "Healthcare Innovations",
        "location": "Toronto, ON",
        "description": "Develop and maintain healthcare applications using C# and.NET.",
        "program_area": "Computer Programming and Analysis",
        "keywords": ["c#", ".net", "application developer", "wil"]
    }
]

@mcp_server.tool() # 使用 @mcp.tool() 或 @mcp_server.tool() 取决于FastMCP版本和初始化方式
async def search_wil_jobs(keywords: list[str] = None, location: str = None, program: str = None) -> list[dict]:
    """
    Searches for WIL job postings based on keywords, location, and program area.
    
    :param keywords: A list of keywords to search for in job titles and descriptions.
    :param location: The desired job location (e.g., "Toronto, ON", "Remote").
    :param program: The student's program area (e.g., "Computer Programming").
    :return: A list of job dictionaries matching the criteria.
    """
    results = []
    # 如果没有提供任何搜索条件，则返回所有职位
    if not keywords and not location and not program:
        return mock_jobs_database # Return all if no criteria

    for job in mock_jobs_database:
        match = True
        if keywords:
            # 简单关键词匹配逻辑 (可以改进为更复杂的匹配)
            if not any(k.lower() in job["title"].lower() or k.lower() in job["description"].lower() or k.lower() in " ".join(job["keywords"]).lower() for k in keywords):
                match = False
        
        if location and match:
            if location.lower() not in job["location"].lower():
                match = False
        
        if program and match:
            if program.lower() not in job["program_area"].lower():
                match = False
        
        if match:
            results.append(job)
            
    return results

@mcp_server.tool()
async def get_job_details(job_id: str) -> dict | None:
    """
    Retrieves the details for a specific job ID.

    :param job_id: The ID of the job to retrieve.
    :return: A dictionary containing job details, or None if not found.
    """
    for job in mock_jobs_database:
        if job["id"] == job_id:
            return job
    return None

# 定义雇主列表（从文档 [1] 提取的数据）
wil_employers_list = [
    "CIBC",
    "RBC",
    "TD",
    "Manulife Financial",
    "Canadian Tire Corporation",
    "NexJ Systems Inc."
]

# 定义常见 WIL 职位头衔列表
wil_job_titles = [
    "Junior Systems Developer",
    "Software Engineer",
    "Programmer/Analyst",
    "Testing Specialist",
    "Application Developer",
    "Quality Assurance Analyst"
]

@mcp_server.resource("wil/employers")
async def get_wil_employers_resource() -> list[str]:
    """
    Provides a list of common WIL program employers.
    """
    return wil_employers_list

@mcp_server.resource("wil/job_titles")
async def get_wil_job_titles_resource() -> list[str]:
    """
    Provides a list of common WIL program job titles.
    """
    return wil_job_titles

# 4. 运行MCP服务器 (通常在脚本末尾)
if __name__ == '__main__':
    # mcp_server.run() # 早期FastMCP或官方SDK的运行方式 [18]
    # FastMCP 2.0+ 可能有更灵活的启动方式，例如:
    # mcp_server.serve_stdio() # 通过标准输入输出运行，适合本地CLI或VS Code集成
    # 或者 mcp_server.serve_http(host="localhost", port=8000) # 通过HTTP运行
    # 请参考FastMCP最新文档确定启动方式
    # 为了与VS Code集成，stdio通常是首选
    mcp_server.serve_stdio()