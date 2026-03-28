import json
from pathlib import Path
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class KBInput(BaseModel):
    query_type: str = Field(
        ...,
        description="Type of data to query: 'history', 'culture', or 'color_palette'",
    )
    parameters: str = Field(
        default="{}",
        description='JSON string of filter parameters, e.g. \'{"region": "Japan"}\' or \'{"decade": "2020s"}\'',
    )


FILE_MAP = {
    "history": "fashion_history.json",
    "culture": "cultural_fashion.json",
    "color_palette": "color_palettes.json",
}


class FashionKnowledgeBaseTool(BaseTool):
    name: str = "Fashion Knowledge Base"
    description: str = (
        "Queries the curated fashion knowledge base for historical fashion data, "
        "cultural fashion norms by region, or color palette recommendations. "
        "Use query_type: 'history', 'culture', or 'color_palette'."
    )
    args_schema: type[BaseModel] = KBInput

    def _run(self, query_type: str, parameters: str = "{}") -> str:
        filename = FILE_MAP.get(query_type)
        if not filename:
            return f"Unknown query_type '{query_type}'. Use: history, culture, color_palette."

        data_file = DATA_DIR / filename
        if not data_file.exists():
            return f"Data file '{filename}' not found."

        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        params = json.loads(parameters) if isinstance(parameters, str) else parameters

        # Filter based on parameters
        if query_type == "culture" and "region" in params:
            region = params["region"]
            for key, value in data.items():
                if region.lower() in key.lower():
                    return f"Cultural Fashion — {key}:\n{json.dumps(value, indent=2)}"
            return f"No cultural fashion data found for region '{region}'. Available: {', '.join(data.keys())}"

        if query_type == "history" and "decade" in params:
            decade = params["decade"]
            for key, value in data.items():
                if decade.lower() in key.lower():
                    return f"Fashion History — {key}:\n{json.dumps(value, indent=2)}"
            return f"No history data for decade '{decade}'. Available: {', '.join(data.keys())}"

        if query_type == "color_palette" and "skin_tone" in params:
            tone = params["skin_tone"]
            for key, value in data.items():
                if tone.lower() in key.lower():
                    return f"Color Palette — {key}:\n{json.dumps(value, indent=2)}"
            return f"No palette for skin tone '{tone}'. Available: {', '.join(data.keys())}"

        # Return all data if no specific filter
        return json.dumps(data, indent=2)[:3000]
