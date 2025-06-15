# 在你的 englishAgent.py 或一个新文件中
from dataclasses import dataclass, field # 确保导入 field
from typing import List, Dict, Any, Optional, Tuple
from openai import OpenAI as OpenAIClient # OpenAI 客户端可以用于 SiliconFlow
from openai.types.create_embedding_response import CreateEmbeddingResponse # 导入响应类型
import os
# from agno.embedder import Embedder # 假设有一个基类 Embedder，如果 agno 提供的话

# 如果 agno 没有提供明确的 Embedder 基类，你可以先不继承，
# 或者定义一个简单的协议类，然后让你的类遵循它。
# 对于 LanceDb，关键是它能找到一个可调用的方法来获取嵌入和一个 'dimensions' 属性。

@dataclass
class SiliconFlowEmbedder: # 如果有 Embedder 基类，则继承： class SiliconFlowEmbedder(Embedder):
    model_id: str = "BAAI/bge-large-en-v1.5"
    # 维度需要根据你选择的 model_id 来确定
    # 对于 BAAI/bge-large-en-v1.5，维度是 1024
    dimensions: int = 1024 # 确保这个值与你的模型匹配
    api_key: Optional[str] = field(default_factory=lambda: os.getenv("SILICONFLOW_API_KEY"))
    base_url: Optional[str] = field(default_factory=lambda: os.getenv("SILICONFLOW_EMBEDDING_URL"))
    
    # 可以添加其他 SiliconFlow 特定的参数，例如 encoding_format
    encoding_format: str = "float" 

    _client: Optional[OpenAIClient] = field(init=False, repr=False, default=None)

    @property
    def client(self) -> OpenAIClient:
        if self._client is None:
            if not self.api_key:
                raise ValueError("SiliconFlow API key is not set.")
            if not self.base_url:
                raise ValueError("SiliconFlow base URL is not set.")
            
            self._client = OpenAIClient(
                api_key=self.api_key,
                base_url=self.base_url,
            )
        return self._client

    def create_embeddings_response(self, texts: List[str]) -> CreateEmbeddingResponse:
        """
        为一批文本创建嵌入响应。
        """
        # 注意：OpenAI 的 Python 库的 embeddings.create 通常一次处理一个输入字符串列表，
        # 或者单个字符串。SiliconFlow API 示例显示的是单个 input。
        # 如果 SiliconFlow 的 OpenAI 兼容接口支持批量输入，可以直接传递 texts。
        # 如果它只支持单个文本，你需要在这里进行循环或调整。
        # 假设它支持批量输入（这在 OpenAI API 中是标准的）
        try:
            response = self.client.embeddings.create(
                model=self.model_id,
                input=texts, # 将文本列表传递给 input
                encoding_format=self.encoding_format,
                # 如果你的模型或API需要其他参数，在这里添加
            )
            return response
        except Exception as e:
            # 更好地记录错误日志
            print(f"Error creating embeddings with SiliconFlow: {e}")
            raise

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        获取一批文本的嵌入向量。
        这是 LanceDb 或类似组件可能调用的方法。
        """
        if not texts:
            return []
        
        response = self.create_embeddings_response(texts)
        # 假设响应结构与 OpenAI 的 CreateEmbeddingResponse 一致
        # data 是一个列表，每个元素包含一个 embedding 列表
        return [item.embedding for item in response.data]

    # agno.embedder.openai.OpenAIEmbedder 有 get_embedding(self, text: str)
    # 为了接口一致性，或者如果 agno 明确需要单文本方法，可以添加它
    def get_embedding(self, text: str) -> List[float]:
        """
        获取单个文本的嵌入向量。
        """
        if not text:
            return [] # 或者抛出错误
        # 将单个文本包装成列表以适应 get_embeddings
        embeddings_list = self.get_embeddings([text])
        return embeddings_list[0] if embeddings_list else []

    # 可能还需要一个 embed_documents 方法，这在 LangChain 和 LlamaIndex 中很常见
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.get_embeddings(texts)

    # 如果需要处理查询嵌入（有时与文档嵌入不同）
    def embed_query(self, text: str) -> List[float]:
        return self.get_embedding(text)
