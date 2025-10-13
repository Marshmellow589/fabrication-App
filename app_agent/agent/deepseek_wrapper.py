from typing import Any, Dict, List, Optional
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.outputs import ChatResult, ChatGeneration
import requests
import json
from loguru import logger
import os

class DeepSeekWrapper(BaseChatModel):
    """Wrapper for DeepSeek API to work with LangChain"""
    
    model_name: str = "deepseek-chat"
    api_key: str = ""
    base_url: str = "https://api.deepseek.com/v1"
    temperature: float = 0.7
    
    def __init__(self, model_name: str = "deepseek-chat", api_key: str = None, base_url: str = "https://api.deepseek.com/v1", temperature: float = 0.7):
        super().__init__()
        self.model_name = model_name
        self.base_url = base_url
        self.temperature = temperature
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
        
        if not self.api_key:
            logger.warning("DeepSeek API key not provided. Please set DEEPSEEK_API_KEY environment variable.")
    
    def _generate(self, messages: List[BaseMessage], **kwargs: Any) -> ChatResult:
        try:
            if not self.api_key:
                raise ValueError("DeepSeek API key is required. Please set DEEPSEEK_API_KEY environment variable.")
            
            # Convert LangChain messages to DeepSeek format
            deepseek_messages = []
            for message in messages:
                if hasattr(message, 'content'):
                    role = "user" if isinstance(message, HumanMessage) else "assistant"
                    deepseek_messages.append({"role": role, "content": message.content})
            
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model_name,
                "messages": deepseek_messages,
                "temperature": self.temperature,
                "stream": False,
                **kwargs
            }
            
            # Call DeepSeek API
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"DeepSeek API call failed: {response.status_code} - {response.text}")
                raise Exception(f"DeepSeek API error: {response.status_code} - {response.text}")
            
            response_data = response.json()
            
            # Extract the response content
            if "choices" in response_data and len(response_data["choices"]) > 0:
                content = response_data["choices"][0]["message"]["content"]
            else:
                raise Exception("Invalid response format from DeepSeek API")
            
            # Convert response to LangChain format
            ai_message = AIMessage(content=content)
            generation = ChatGeneration(message=ai_message)
            
            return ChatResult(generations=[generation])
            
        except Exception as e:
            logger.error(f"DeepSeek API call failed: {e}")
            raise
    
    async def _agenerate(self, messages: List[BaseMessage], **kwargs: Any) -> ChatResult:
        # For async, we'll just call the sync version for now
        return self._generate(messages, **kwargs)
    
    @property
    def _llm_type(self) -> str:
        return "deepseek"
