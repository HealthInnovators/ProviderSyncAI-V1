from smolagents import Tool
from ...infrastructure.searxng import client as searxng_client


class WebSearchTool(Tool):
    name = "web_search"
    description = "Search the web via SearXNG and return top results"
    inputs = {"query": str, "categories": str, "num_results": int}
    output_type = "json"

    async def __call__(self, query: str, categories: str = "general", num_results: int = 5):
        return await searxng_client.search(query, categories=categories, num_results=num_results)


