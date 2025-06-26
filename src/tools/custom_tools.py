import os
from crewai.tools import BaseTool

class FileReaderTool(BaseTool):
    name: str = "文件读取工具 (File Reader Tool)"
    description: str = "从本地文件中读取内容。用于加载现有的个人元资源库作为对话上下文。"

    def _run(self, file_path: str) -> str:
        """核心执行逻辑：读取文件。"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "文件未找到。这可能是第一次对话，元资源库尚未创建。"
        except Exception as e:
            return f"读取文件 {file_path} 时发生错误: {e}"

class FileWriterTool(BaseTool):
    name: str = "文件写入工具 (File Writer Tool)"
    description: str = "将指定的文本内容写入或追加到本地文件中。用于创建和更新个人元资源库。"

    def _run(self, content: str, file_path: str = "personal_brand_assets.md") -> str:
        """核心执行逻辑：写入文件。"""
        # 'w' 模式表示覆盖写入，确保每次都是最新的总结。
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"成功将最新总结写入文件 {file_path}"
        except Exception as e:
            return f"写入文件 {file_path} 时发生错误: {e}"