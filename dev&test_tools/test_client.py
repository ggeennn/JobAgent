# test_client.py (最终修正版)
import asyncio
import traceback
import json

from fastmcp.client.transports import PythonStdioTransport 
from fastmcp import Client

async def main():
    print("--- 启动本地MCP测试客户端 (最终修正版) ---")
    
    try:
        transport = PythonStdioTransport(script_path="server_script.py")
        client = Client(transport=transport)

        async with client:
            print("[成功] 客户端已连接！")
            
            tool_to_call = 'search_wil_jobs'
            
            print(f"\n>>> 调用工具: {tool_to_call} ...")
            response = await client.call_tool(tool_to_call, {})
            
            print("<<< 收到响应。")
            print("\n--- ✅ 工具调用成功！解析最终结果 ---")
            if response:
                # 1. 响应是一个列表，其中包含一个TextContent对象
                content_object = response[0]
                
                # 2. 从.text属性获取包含整个职位列表的JSON字符串
                jobs_list_json_string = content_object.text
                
                # 3. 将JSON字符串解析成一个Python列表
                jobs_list = json.loads(jobs_list_json_string)
                
                # 4. 现在，遍历这个职位列表
                for job_dict in jobs_list:
                    # 5. 从每个职位字典中安全地获取信息
                    print(f"  - 找到职位: {job_dict.get('title')}")
            else:
                print("  - 未找到职位。")
            print("------------------------------------------\n")

    except Exception as e:
        print(f"\n[错误] 发生异常: {e}")
        print("\n--- 详细错误追踪 ---")
        traceback.print_exc()
        print("----------------------\n")
    
    print("--- 测试结束 ---")

if __name__ == "__main__":
    asyncio.run(main())