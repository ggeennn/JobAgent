# server_script.py
from fastmcp import FastMCP # 假设使用的是FastMCP 2.0+
# 或者 from mcp.server.fastmcp import FastMCP 如果是早期版本或官方SDK的mcp包 [7, 18]

# 1. 初始化MCP服务器，并指定一个名称
# 这个名称会在客户端配置中用到，用于识别此服务器
mcp_server = FastMCP(name="WILJobAgent") 

#... 此处将定义MCP工具和资源...

# 4. 运行MCP服务器 (通常在脚本末尾)
if __name__ == '__main__':
    # mcp_server.run() # 早期FastMCP或官方SDK的运行方式 [18]
    # FastMCP 2.0+ 可能有更灵活的启动方式，例如:
    # mcp_server.serve_stdio() # 通过标准输入输出运行，适合本地CLI或VS Code集成
    # 或者 mcp_server.serve_http(host="localhost", port=8000) # 通过HTTP运行
    # 请参考FastMCP最新文档确定启动方式
    # 为了与VS Code集成，stdio通常是首选
    mcp_server.serve_stdio()