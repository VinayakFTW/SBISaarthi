import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

class BaseAgent:
    def __init__(self, name: str, system_prompt: str, model: str = "gpt-4o"):
        self.name = name
        self.system_prompt = system_prompt
        self.model = model
        self.client = OpenAI(base_url=os.getenv("LLM_BASE_URL"),api_key=os.getenv("OPENAI_API"))

    def process_message(self, message: str, context: dict = None) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        if context:
            messages.append({
                "role": "system", 
                "content": f"Current Context: {json.dumps(context)}"
            })
            
        messages.append({"role": "user", "content": message})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content
