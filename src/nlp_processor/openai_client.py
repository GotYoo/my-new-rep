# src/nlp_processor/openai_client.py
from openai import OpenAI
from config import Settings
import json

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=Settings.API_KEY,
            base_url=Settings.API_BASE
        )
    
    def chat_completion(self, messages, model="xdeepseekr1llama70b"):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                temperature=0.0,
                max_tokens=8192,
                extra_headers={"lora_id": "0"},
                stream_options={"include_usage": True}
            )
            
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
            return full_response, None
        except Exception as e:
            return None, str(e)