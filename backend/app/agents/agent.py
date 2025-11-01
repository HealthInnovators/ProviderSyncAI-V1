from typing import List
from smolagents import CodeAgent, Tool
from ..infrastructure.settings import settings
from .tools.nppes_tool import NppesTool
from .tools.web_search_tool import WebSearchTool


def build_agent() -> CodeAgent:
    tools: List[Tool] = [NppesTool(), WebSearchTool()]
    model = None
    # CodeAgent will attempt to use OPENAI_API_KEY or HF token automatically if configured.
    agent = CodeAgent(tools=tools, model=model, name="coordinator")
    return agent


