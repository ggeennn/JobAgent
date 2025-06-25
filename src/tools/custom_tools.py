import os
from crewai.tools import BaseTool

class FileWriterTool(BaseTool):
    name: str = "文件写入工具 (File Writer Tool)"
    description: str = "将指定的文本内容写入或追加到本地文件中。对于创建和更新个人元资源库至关重要。"

    def _run(self, content: str, file_path: str = "personal_meta_resource.md") -> str:
        """
        核心执行逻辑：写入文件。
        参数:
            file_path: 要写入的文件路径。默认为 'personal_meta_resource.md'。
            content: 要写入的文本内容。
        """
        # 'a' 模式表示追加。如果文件不存在，则会创建。
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(content + "\n")
            return f"成功将内容追加到文件 {file_path}"
        except Exception as e:
            return f"写入文件 {file_path} 时发生错误: {e}"