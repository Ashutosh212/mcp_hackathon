from smolagents import InferenceClientModel, CodeAgent, ToolCollection
from mcp.client.stdio import StdioServerParameters
from smolagents import CodeAgent, OpenAIServerModel

GEMINI_API_KEY = "AIzaSyA-YO8PdPw3Pq0Ip5nIPMjiKtMKALwSWE8"

model = OpenAIServerModel(
    model_id="gemini-2.0-flash",
    api_key=GEMINI_API_KEY,
    # Google Gemini OpenAI-compatible API base URL
    api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
)

server_parameters = StdioServerParameters(command="uv", args=["run", "server.py"])

with ToolCollection.from_mcp(
    server_parameters, trust_remote_code=True
) as tool_collection:
    agent = CodeAgent(tools=[*tool_collection.tools], model=model)
    agent.run("What's the weather in Tokyo?")