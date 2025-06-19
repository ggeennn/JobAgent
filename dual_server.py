from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
import logging

# 1. Initialize MCP server
mcp_server = FastMCP(
    name="wiljobagent",
    #stateless_http=True  # enable stateless HTTP (no sessions), compatible with cline
    # json_response can be default True for HTTP; SSE uses streaming
)

# 2. Mock data setup
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
        "description": "Develop and maintain healthcare applications using C# and .NET.",
        "program_area": "Computer Programming and Analysis",
        "keywords": ["c#", ".net", "application developer", "wil"]
    }
]

#define tools
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

# 4. Define resources
wil_employers_list = [
    "CIBC",
    "RBC",
    "TD",
    "Manulife Financial",
    "Canadian Tire Corporation",
    "NexJ Systems Inc."
]

wil_job_titles = [
    "Junior Systems Developer",
    "Software Engineer",
    "Programmer/Analyst",
    "Testing Specialist",
    "Application Developer",
    "Quality Assurance Analyst"
]

@mcp_server.resource("mcp://jobAgent/wil/employers")
async def get_wil_employers_resource() -> list[str]:
    return wil_employers_list

@mcp_server.resource("mcp://jobAgent/wil/job_titles")
async def get_wil_job_titles_resource() -> list[str]:
    return wil_job_titles

# 5. Logging setup
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    filename="mcp_server.log")
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log each request and response."""
    async def dispatch(self, request, call_next):
        logger.debug(f"Incoming request: {request.method} {request.url}")
        logger.debug(f"Headers: {dict(request.headers)}")
        logger.debug(f"Query params: {dict(request.query_params)}")
        response = await call_next(request)
        logger.debug(f"Response status: {response.status_code}")
        return response

# Prepare Starlette middleware
middleware = [
    Middleware(LoggingMiddleware)
]

if __name__ == "__main__":
    import uvicorn
    from starlette.applications import Starlette
    from starlette.routing import Mount
    from contextlib import asynccontextmanager

    # 1. 像之前一样，创建两个 transport-specific 的 app
    http_app = mcp_server.http_app(path="/jobagent", transport="streamable-http", middleware=middleware)
    sse_app = mcp_server.http_app(path="/jobagent", transport="sse")

    # 2. 定义一个统一的 lifespan 管理器
    #    这个管理器会确保两个子应用的 lifespan 都被正确执行
    @asynccontextmanager
    async def unified_lifespan(app):
        # 服务器启动时...
        async with http_app.lifespan(app):
            async with sse_app.lifespan(app):
                print("Lifespan started: Both HTTP and SSE transports are ready.")
                yield
        # 服务器关闭时...
        print("Lifespan shutdown: Cleaning up resources.")


    # 3. 创建根应用，并把统一的 lifespan 管理器传给它
    root_app = Starlette(
        routes=[
            Mount("/http", app=http_app),
            Mount("/sse", app=sse_app),
        ],
        lifespan=unified_lifespan  # <--- 这是解决问题的关键
    )

    # 4. 打印访问地址 (与之前相同)
    print("Starting unified MCP Server on http://127.0.0.1:8000")
    print("  - HTTP endpoint for Copilot: http://127.0.0.1:8000/http/jobagent")
    print("  - SSE endpoint for cline:    http://127.0.0.1:8000/sse/jobagent")

    # 5. 运行这一个根应用
    uvicorn.run(root_app, host="127.0.0.1", port=8000)