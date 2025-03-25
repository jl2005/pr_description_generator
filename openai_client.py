import time
import json
import requests
from typing import Optional

class OpenAIClient:
    def __init__(self, base_url: str, api_key: str):
        """初始化OpenAI客户端
        
        Args:
            base_url: OpenAI API基础URL
            api_key: OpenAI API密钥
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        
    def chat_completion(self, 
                       system: str,
                       user: str,
                       model: str = "gpt-3.5-turbo",
                       temperature: float = 0.7) -> str:
        """调用OpenAI chat completion API
        
        Args:
            system: 系统提示
            user: 用户提示
            model: 模型名称
            temperature: 温度参数
            
        Returns:
            AI生成的响应文本
        """
        url = f"{self.base_url}/v1/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "temperature": temperature
        }
        
        response = requests.post(url, headers=headers, json=data)
        print(response.json())
        # 打印headers
        print(headers)
        # 打印data
        print(data)
        
        # 如果遇到429错误，增加请求间隔
        if response.status_code == 429:
            print("Rate limit exceeded. Waiting for 10 seconds...")
            time.sleep(10)  # 等待60秒后重试
            response = requests.post(url, headers=headers, json=data)
        
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"] 