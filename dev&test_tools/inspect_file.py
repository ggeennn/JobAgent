# inspect_file.py
import os
import sys

# 我们将直接使用错误消息中提供的绝对路径，这是最可靠的方式
file_path = r'P:\jobAgent\.venv\Lib\site-packages\fastmcp\client\transports.py'

print(f"--- 准备读取文件: {file_path} ---")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        print("\n" + "="*20 + " 文件内容开始 " + "="*20)
        # 逐行打印，并附上行号，方便查看
        for i, line in enumerate(f, 1):
            print(f"{i:03d}: {line.rstrip()}")
        print("="*20 + "  文件内容结束  " + "="*20 + "\n")

except FileNotFoundError:
    print(f"\n[错误] 找不到文件: {file_path}")
    print("请确认该路径是否仍然有效。")
except Exception as e:
    print(f"\n[错误] 读取文件时发生意外: {e}")