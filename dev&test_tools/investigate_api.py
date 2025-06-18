# investigate_api.py
import fastmcp

print("--- 正在侦查 fastmcp.FastMCP 对象 ---")
# dir() 是Python的内置函数，可以列出一个对象的所有属性和方法名
# 为了看得更清楚，我们过滤掉以双下划线开头的特殊方法
server_methods = [method for method in dir(fastmcp.FastMCP) if not method.startswith('__')]
print("fastmcp.FastMCP 上可用的方法/属性有:")
print(server_methods)

print("\n" + "="*40 + "\n")

print("--- 正在侦查 fastmcp.Client 对象 ---")
client_methods = [method for method in dir(fastmcp.Client) if not method.startswith('__')]
print("fastmcp.Client 上可用的方法/属性有:")
print(client_methods)