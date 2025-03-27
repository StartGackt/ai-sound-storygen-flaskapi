import os
import requests
from typing import Dict, Any, List, Optional

class CompletionChoice:
    def __init__(self, text: str):
        self.text = text

class CompletionResponse:
    def __init__(self, choices: List[CompletionChoice]):
        self.choices = choices

class Completions:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1/completions"
    
    def create(self, model: str, prompt: str, max_tokens: int = 1000, 
               temperature: float = 0.7, top_p: float = 1.0, **kwargs) -> CompletionResponse:
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p
        }
        
        # Add any additional parameters
        for key, value in kwargs.items():
            payload[key] = value
        
        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        choices = [CompletionChoice(text=choice.get("text", "")) for choice in data.get("choices", [])]
        
        return CompletionResponse(choices=choices)

class DeepSeekAI:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DeepSeek API key is required")
        
        self.completions = Completions(api_key=self.api_key)