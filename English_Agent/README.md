# English Grammar Agent API

## 1. 简介

本项目是一个基于 FastAPI 的 API 服务，旨在提供一个专业、严谨且友好的英语语法与写作优化助手。该服务通过一个 API 端点接收用户输入的英文文本，并返回精确修正后的版本。

核心功能由 `agno` 代理框架驱动，能够识别并纠正文本中的语法、拼写和标点错误。

## 2. 环境准备

在运行此项目之前，请确保您已安装以下软件：

*   Python 3.8+
*   [uv](https://github.com/astral-sh/uv): 一个极速的 Python 包安装和解析器。

## 3. 安装与配置

### 3.1. 克隆项目

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 3.2. 创建虚拟环境并安装依赖

建议使用 `uv` 来管理虚拟环境和依赖项。

```bash
# 创建一个名为 .venv 的虚拟环境
uv venv

# 激活虚拟环境
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# 安装依赖 (假设有 requirements.txt)
uv pip install -r requirements.txt
```
*(如果 `requirements.txt` 不存在，请根据 `main_api.py` 中的 `import` 语句手动安装 `fastapi`, `uvicorn`, `python-dotenv`, `agno-ai`, `psycopg2-binary` 等)*

### 3.3. 配置环境变量

项目启动需要一些关键的环境变量。请在项目根目录下创建一个名为 `.env` 的文件，并根据 `.env.example` 文件的格式填充您的配置信息。

**重要**: `.env` 文件包含了敏感信息，请务必将其添加到 `.gitignore` 文件中，避免提交到版本库。

## 4. 运行服务

配置完成后，使用以下命令启动 FastAPI 服务：

```bash
uv run main_api.py
```

服务启动后，您将在终端看到类似以下的输出：

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

现在，您可以访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 查看自动生成的 Swagger UI API 文档。

## 5. API 端点说明

### `/chat`

此端点是与语法助手交互的核心。

*   **方法**: `POST`
*   **描述**: 发送一段英文文本进行语法检查和修正。
*   **Headers**:
    *   `X-User-ID` (可选, `string`): 用户的唯一标识符，用于跨会话追踪。
    *   `X-Session-ID` (可选, `string`): 当前会话的唯一标识符。如果提供，代理将加载此会话的历史记录。
*   **Request Body**:
    ```json
    {
      "message": "your english text here",
      "stream": false
    }
    ```
    *   `message` (`string`,必需): 需要检查的英文文本。
    *   `stream` (`boolean`, 可选, 默认 `false`): 是否以流式响应返回结果。
*   **Success Response (stream=false)**:
    *   **Code**: `200 OK`
    *   **Content**:
        ```json
        {
          "response": "corrected text here",
          "user_id": "ava",
          "session_id": "generated-session-id"
        }
        ```
*   **Example (cURL)**:
    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/chat' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "message": "i has a apple",
      "stream": false
    }'
    ```

## 6. 代理修正逻辑

代理会根据以下规则修正文本：

1.  **语法错误**: 在原句末尾用 `{}` 包裹正确的句子。
2.  **拼写/词语错误**: 在错误单词后用 `[]` 写入正确的单词。
3.  **标点错误**: 在需要修正的位置用 `<>` 插入正确的标点。
