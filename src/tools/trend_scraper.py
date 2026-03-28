import os
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from tavily import TavilyClient

TREND_QUERY_TEMPLATES = {
    "social_media": "TikTok Instagram fashion trends {region} {year}",
    "generational": "Gen Z fashion vs millennial fashion trends {year}",
    "seasonal": "{season} fashion trends {year} outfit ideas",
    "runway": "runway fashion trends {season} {year} street style",
}


class TrendInput(BaseModel):
    trend_type: str = Field(
        ...,
        description="Type of trend to search: 'social_media', 'generational', 'seasonal', or 'runway'",
    )
    region: str = Field(default="global", description="Region to focus on, e.g. 'USA', 'Japan', 'Europe'")
    season: str = Field(default="spring", description="Season, e.g. 'spring', 'summer', 'fall', 'winter'")
    year: str = Field(default="2026", description="Year to search trends for")


class TrendScraperTool(BaseTool):
    name: str = "Fashion Trend Scraper"
    description: str = (
        "Searches for specific types of fashion trends using curated query templates. "
        "Supports social_media, generational, seasonal, and runway trend types."
    )
    args_schema: type[BaseModel] = TrendInput

    def _run(
        self,
        trend_type: str,
        region: str = "global",
        season: str = "spring",
        year: str = "2026",
    ) -> str:
        template = TREND_QUERY_TEMPLATES.get(trend_type)
        if not template:
            return f"Unknown trend type '{trend_type}'. Use: social_media, generational, seasonal, runway."

        query = template.format(region=region, season=season, year=year)
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = client.search(query=query, max_results=5, include_answer="basic")

        results = [f"Trend Search ({trend_type}): {query}\n"]
        if response.get("answer"):
            results.append(f"Summary: {response['answer']}\n")
        for r in response.get("results", []):
            results.append(
                f"- {r['title']}: {r['content'][:300]}... (Source: {r['url']})"
            )
        return "\n".join(results) if len(results) > 1 else "No trend data found."
