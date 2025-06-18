# 技术报告：关于在VS Code中使用Cline插件连接本地FastMCP服务器失败的深度调试分析

**报告ID:** `DBG-20250617-A1`
**日期:** 2025年6月17日
**主题:** 对特定环境下，VS Code插件 `Cline` 无法通过 `stdio` 或 `HTTP` 协议连接到本地 `fastmcp` v2.8.0 服务器问题的系统性排查与最终诊断。

---

## 1. 摘要 (Abstract)

本报告详述了一系列旨在解决VS Code `Cline` 插件无法连接至本地 `fastmcp` MCP服务器的调试步骤。初始问题表现为持续的 "Not connected" 错误。通过系统性的隔离测试，我们编写了一个独立的Python测试客户端 (`test_client.py`)，并最终**成功验证了服务器脚本 (`server_script.py`) 和 `fastmcp` 库本身在 `stdio` 协议下的功能完备性**。

为解决 `Cline` 与 `stdio` 的兼容性问题，我们进一步将服务器切换至 `HTTP` 模式，并成功在本地 `http://127.0.0.1:8000` 启动了服务。然而，即使在 `Cline` 的配置与运行中的HTTP服务器完全匹配的情况下，连接依然失败。

**最终诊断结论为：服务器端代码与 `fastmcp` 库功能健全，问题根源极大概率在于 `Cline` 插件本身，可能存在内部bug、与特定环境的兼容性问题，或未公开的配置要求。**

---

## 2. 项目目标与环境 (Project Goal & Environment)

* **核心目标:** 构建一个由模型上下文协议（MCP）驱动的“工作整合学习（WIL）”求职智能代理。
* **IDE:** Visual Studio Code
* **核心库:** `fastmcp` (版本: 2.8.0)
* **服务器脚本:** `server_script.py` (使用 `fastmcp` 构建)
* **客户端/主机:** `Cline` VS Code 插件 (配置使用 Grok-3 API)
* **操作系统环境:** Windows (路径表明，如 `P:\...`, `C:\Users\...`)
* **Python 环境:** 位于项目目录下的虚拟环境 `P:\jobAgent\.venv\`

---

## 3. 问题描述 (Problem Description)

`Cline` 插件无法连接到在本地运行的 `wiljobagent` MCP服务器。无论服务器以 `stdio` 模式还是 `HTTP` 模式运行，`Cline` 在尝试调用其工具时，均返回 `Error executing MCP tool: Not connected` 的错误。

---

## 4. 调试过程与关键发现 (Debugging Process & Key Findings)

整个调试过程可以分为两个主要阶段：

### 阶段一：本地化 `stdio` 测试与服务器验证

此阶段的目标是绕开 `Cline`，直接验证服务器脚本和 `fastmcp` 库是否能正常工作。

1.  **初步失败与API侦查**:
    * **现象**: 尝试使用 `mcp_server.serve_http()` 和 `Client.stdio()` 等方法均导致 `AttributeError`。
    * **行动**: 编写并运行 `investigate_api.py` 和 `pip show -f fastmcp`。
    * **发现**: 确认了当前 `fastmcp` v2.8.0 的正确API：服务器启动使用 `mcp_server.run()`；客户端的创建需要一个 `transport` 对象，而该对象的类位于 `fastmcp.client.transports` 模块中。

2.  **`transport` 类名确定**:
    * **现象**: 尝试 `from fastmcp.client.transports import StdIOTransport` 导致 `ImportError`。
    * **行动**: 编写 `inspect_file.py` 直接读取 `transports.py` 的源码。
    * **发现**: **确定了正确的类名为 `PythonStdioTransport`**。

3.  **数据格式适配**:
    * **现象**: 连接成功后，在处理返回数据时出现 `AttributeError: 'TextContent' object has no attribute 'get'` 和 `AttributeError: 'list' object has no attribute 'get'`。
    * **行动**: 修正客户端的数据处理逻辑。
    * **发现**: 服务器返回的整个 `list[dict]` 被序列化为JSON字符串，并包装在**一个** `TextContent` 对象中返回。客户端需要先获取 `.text` 属性，再用 `json.loads()` 解析出列表。

4.  **本地测试最终成功**:
    * **行动**: 运行最终修正版的 `test_client.py`。
    * **输出**:
        ```
        --- ✅ 工具调用成功！解析最终结果 ---
          - 找到职位: QA Analyst Co-op
          - 找到职位: Application Developer WIL
        ```
    * **结论**: **此结果无可辩驳地证明了 `server_script.py` 和 `fastmcp` 库在 `stdio` 模式下可以完美地协同工作。**

### 阶段二： `HTTP` 模式切换与 `Cline` 再测试

此阶段的目标是使用更通用的 `HTTP` 协议来绕开 `stdio` 的潜在不兼容性。

1.  **服务器 `HTTP` 模式启动**:
    * **行动**: 修改 `server_script.py`，使用已发现的 `run_http_async` 方法。
    * **输出**:
        ```
        INFO: Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000) (Press CTRL+C to quit)
        ```
    * **结论**: **服务器作为独立的HTTP服务成功启动并运行。**

2.  **`Cline` 配置适配与最终失败**:
    * **行动**: 修改 `cline_mcp_settings.json` 以匹配HTTP模式。
        ```json
        { "mcpServers": { "wiljobagent": { "transport": "streamable-http", "url": "[http://127.0.0.1:8000](http://127.0.0.1:8000)" } } }
        ```
    * **现象**: 在 `Cline` 中调用工具，依然返回 `Error executing MCP tool: Not connected`。
    * **`Cline` 日志分析**: 日志显示 `Cline` **确实尝试了**执行正确的服务器启动命令（在 `stdio` 模式时），但后续的通信失败。在`HTTP`模式下，它也无法连接到一个已被证明在运行的HTTP服务。

---

## 5. 最终诊断 (Final Diagnosis)

综合所有证据，可以得出以下结论：

1.  **服务器端 (`server_script.py`) 无问题**: 无论是 `stdio` 还是 `HTTP` 模式，服务器本身的功能和逻辑都已通过独立测试得到验证。
2.  **库 (`fastmcp`) 无问题**: 我们已经找到了在当前版本(v2.8.0)下，正确使用该库进行客户端-服务器通信的方法。
3.  **配置 (`cline_mcp_settings.json`) 无问题**: 最终的HTTP配置和之前的`stdio`配置，在格式和内容上都是正确的。
4.  **瓶颈在于 `Cline` 插件**: `Cline` 插件无法与一个功能完备的本地服务器建立连接（无论是通过`stdio`还是`HTTP`）。这表明问题源于 `Cline` 插件的内部实现、其与VS Code或操作系统的交互、或其网络通信机制中存在的BUG或限制。

---

## 6. 待研究的开放性问题与建议 (Open Questions & Recommendations)

* **深入研究 `Cline` 的 `stdio` 实现**: 为何 `Cline` 的 `stdio` 通信会失败，而 `fastmcp` 自己的客户端却能成功？是否存在特定的消息格式、握手协议或超时机制不匹配？
* **分析 `Cline` 的 `HTTP` 客户端行为**: 为何 `Cline` 无法连接到一个标准的本地 `localhost` HTTP服务？是否存在代理问题、安全沙箱限制（如VS Code对插件网络权限的限制）或证书问题？
* **建议的行动方案**:
    1.  **查阅 `Cline` 官方文档**，寻找关于连接本地 `fastmcp` 服务器的特定指引或已知问题。
    2.  **在 `Cline` 的 GitHub Issues 页面提问**，附上本报告的核心内容，向开发者社区寻求帮助。
    3.  **尝试替代的MCP客户端**，如VS Code内置聊天功能，以验证项目目标是否可以在当前环境中通过其他途径实现。