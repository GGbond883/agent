from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from openai import OpenAI
from config import Config


class BaseAgent(ABC):
    """所有 Agent 的基类"""

    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def llm_call(self, user_message: str, temperature: float = 0.7) -> str:
        """调用 LLM 的通用方法"""
        try:
            response = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in {self.name}: {str(e)}"

    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """每个 Agent 需要实现的具体执行逻辑"""
        pass

    def __str__(self):
        return f"Agent({self.name}, Role={self.role})"