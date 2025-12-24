import sys
sys.dont_write_bytecode = True
from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()

import os
from openai import OpenAI


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.base_url = os.getenv("LLM_BASE_URL")
        self.model = os.getenv("LLM_MODEL", "openai/gpt-4o-mini")

        if not self.api_key:
            raise ValueError("LLM_API_KEY is not set")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            default_headers={
                # Required by OpenRouter
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "MCP Support Bot Demo",
            },
        )

    def chat(self, messages, tools=None):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto" if tools else None,
            temperature=0.3,
        )
        return response
