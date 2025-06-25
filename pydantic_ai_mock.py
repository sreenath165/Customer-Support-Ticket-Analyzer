import os
import re
import json
import requests
from dotenv import load_dotenv
from typing import TypeVar, Generic, Type
from pydantic import BaseModel
from datetime import datetime

load_dotenv()

T = TypeVar("T", bound=BaseModel)


class OpenAIChatModel:
    def __init__(self, model: str, api_key_env: str):
        self.model = model
        self.api_key = os.getenv(api_key_env)

    def chat(self, messages):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://your-project-name.com",
            "X-Title": "Draconic Case Study"
        }
        body = {
            "model": self.model,
            "messages": messages
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            raise Exception("OpenRouter API call failed.")

        result = response.json()
        return result["choices"][0]["message"]["content"]


class PydanticAgent(Generic[T]):
    def __init__(self, model: OpenAIChatModel, system_prompt: str, output_model: Type[T]):
        self.model = model
        self.system_prompt = system_prompt
        self.output_model = output_model
        self.agent_name = output_model.__name__.replace("Output", "") 

    def run(self, input_data: dict, routing_decision: str = "N/A") -> T:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": str(input_data)}
        ]

        output_text = self.model.chat(messages)

        try:
            # Extract first valid JSON object from output
            json_match = re.search(r"{.*?}", output_text, re.DOTALL)
            if not json_match:
                raise ValueError("No JSON object found in model output.")

            json_text = json_match.group(0)
            parsed = json.loads(json_text)

            validated = self.output_model.model_validate(parsed)

            # Write to ai_chat_history.txt
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("ai_chat_history.txt", "a", encoding="utf-8") as f:
                f.write(f"\n\n [{self.agent_name}Agent] - {timestamp}\n")
                f.write("User Input:\n")
                f.write(str(input_data) + "\n\n")
                f.write("Model Output:\n")
                f.write(json.dumps(parsed, indent=2) + "\n\n")

                if "reasoning" in parsed:
                    f.write("Reasoning:\n")
                    f.write(parsed["reasoning"] + "\n\n")

                f.write(f"Routing Decision: {routing_decision}\n")
                f.write("-" * 50 + "\n")

            return validated

        except Exception as e:
            print("\n Failed to parse output:\n", output_text)
            raise e
