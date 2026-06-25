import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from core.security import DataMasker

load_dotenv()

class BaseAgent:
    def __init__(self, name: str, system_prompt: str, model: str = "auto"):
        self.name = name
        self.system_prompt = system_prompt
        self.model = model
        self.client = OpenAI(base_url=os.getenv("LLM_BASE_URL"), api_key=os.getenv("OPENAI_API_KEY"))
        self.tools = []
        self.tool_map = {}

    def add_tool(self, tool_definition: dict, tool_function):
        self.tools.append(tool_definition)
        self.tool_map[tool_definition['function']['name']] = tool_function

    def process_message(self, message: str, context: dict = None) -> str:
        masked_message = DataMasker.mask(message)
        
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        if context:
            messages.append({
                "role": "system", 
                "content": f"Current Context: {json.dumps(context)}"
            })
            
        messages.append({"role": "user", "content": masked_message})

        kwargs = {
            "model": self.model,
            "messages": messages
        }
        if self.tools:
            kwargs["tools"] = self.tools

        response = self.client.chat.completions.create(**kwargs)
        response_message = response.choices[0].message
        
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_to_call = self.tool_map.get(function_name)
                if function_to_call:
                    function_args = json.loads(tool_call.function.arguments)
                    function_response = function_to_call(**function_args)
                    
                    messages.append(response_message)
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(function_response),
                    })
            
            second_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return second_response.choices[0].message.content
            
        return response_message.content
