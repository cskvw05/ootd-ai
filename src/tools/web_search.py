import os
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from tavily import TavilyClient


class SearchInput(BaseModel):
    query: str = Field(..., description="The search query for fashion-related information")
    max_results: int = Field(default=5, description="Maximum number of results to return")


class TavilySearchTool(BaseTool):
    name: str = "Fashion Web Search"
    description: str = (
        "Searches the web for current fashion trends, news, and information. "
        "Use this for any real-time fashion data that isn't available in local datasets."
    )
    args_schema: type[BaseModel] = SearchInput

    def _run(self, query: str, max_results: int = 5) -> str:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = client.search(
            query=f"fashion {query}",
            max_results=max_results,
            include_answer="basic",
        )

        results = []
        if response.get("answer"):
            results.append(f"Summary: {response['answer']}")
        for r in response.get("results", []):
            results.append(
                f"- {r['title']}: {r['content'][:300]}... (Source: {r['url']})"
            )
        return "\n".join(results) if results else "No results found for this query."
