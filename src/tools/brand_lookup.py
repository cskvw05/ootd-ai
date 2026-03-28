import json
import os
from pathlib import Path
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from tavily import TavilyClient

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class BrandInput(BaseModel):
    brand_name: str = Field(..., description="Name of the fashion brand to look up")


class BrandLookupTool(BaseTool):
    name: str = "Fashion Brand Lookup"
    description: str = (
        "Looks up fashion brand information including sustainability rating, "
        "ethical practices, price range, and target demographic. "
        "Checks local curated data first, falls back to web search."
    )
    args_schema: type[BaseModel] = BrandInput

    def _run(self, brand_name: str) -> str:
        # Try local curated data first
        brand_file = DATA_DIR / "brand_ethics.json"
        if brand_file.exists():
            with open(brand_file, "r", encoding="utf-8") as f:
                brands = json.load(f)

            # Case-insensitive lookup
            for name, data in brands.items():
                if name.lower() == brand_name.lower():
                    lines = [f"Brand: {name}"]
                    for key, value in data.items():
                        if isinstance(value, list):
                            value = ", ".join(value)
                        lines.append(f"  {key.replace('_', ' ').title()}: {value}")
                    return "\n".join(lines)

        # Fallback to web search
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = client.search(
            query=f"{brand_name} fashion brand sustainability ethics values practices",
            max_results=3,
            include_answer="basic",
        )

        results = [f"Brand: {brand_name} (web search results)\n"]
        if response.get("answer"):
            results.append(f"Summary: {response['answer']}\n")
        for r in response.get("results", []):
            results.append(f"- {r['title']}: {r['content'][:300]}...")
        return "\n".join(results) if len(results) > 1 else f"No information found for brand '{brand_name}'."
