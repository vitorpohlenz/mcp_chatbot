import httpx

MCP_SERVER_URL = "https://vipfapwm3x.us-east-1.awsapprunner.com/mcp"

class MCPClient:
    def __init__(self, base_url: str = MCP_SERVER_URL):
        self.client = httpx.Client(timeout=30)

    def call(self, payload: dict):
        """
        Generic MCP call.
        Assumes MCP follows streamable HTTP response.
        """
        response = self.client.post(
            self.base_url,
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()
