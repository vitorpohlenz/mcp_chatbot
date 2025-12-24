from llm_client import LLMClient
from mcp_client import MCPClient

SYSTEM_PROMPT = """
You are a helpful customer support assistant for a company
that sells computer products such as monitors, printers, and accessories.

Use available tools when necessary to retrieve accurate product
or troubleshooting information.
"""

class SupportChatbot:
    def __init__(self):
        self.llm = LLMClient()
        self.mcp = MCPClient()

    def handle_message(self, user_message: str, history: list):
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        # Step 1: Ask LLM
        response = self.llm.chat(messages)

        msg = response.choices[0].message

        # Step 2: Tool call?
        if msg.tool_calls:
            tool_call = msg.tool_calls[0]
            tool_payload = tool_call.function.arguments

            mcp_result = self.mcp.call(tool_payload)

            messages.append(msg)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(mcp_result)
            })

            # Step 3: Final LLM answer
            final_response = self.llm.chat(messages)
            return final_response.choices[0].message.content

        return msg.content
