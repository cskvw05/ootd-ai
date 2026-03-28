from crewai import Agent, Crew, Process, Task
from src.llm import get_llm
from src.tools.web_search import TavilySearchTool
from src.tools.trend_scraper import TrendScraperTool
from src.tools.brand_lookup import BrandLookupTool
from src.tools.fashion_kb import FashionKnowledgeBaseTool

# Shared tool instances
_tavily = TavilySearchTool()
_trend_scraper = TrendScraperTool()
_brand_lookup = BrandLookupTool()
_fashion_kb = FashionKnowledgeBaseTool()


class OoftdCrew:
    """ooftd — Fashion Market Research Multi-Agent Crew."""

    def __init__(self):
        self.llm = get_llm()

    def _build_agents(self):
        self.query_router = Agent(
            role="Fashion Query Analyst",
            goal=(
                "Analyze the user's fashion question and produce a structured research brief. "
                "Identify which domains the query touches: trends, culture, brands, outfit suggestions, "
                "color/style matching, or a combination."
            ),
            backstory=(
                "You are an expert fashion query analyst who understands the nuances of fashion-related questions. "
                "You break down complex requests into clear research briefs that other specialists can act on."
            ),
            llm=self.llm,
            verbose=True,
        )

        self.trend_researcher = Agent(
            role="Fashion Trend Analyst",
            goal=(
                "Find current and emerging fashion trends using real-time web data. "
                "Cover social media trends, seasonal shifts, runway-to-street pipeline, "
                "and generational style differences."
            ),
            backstory=(
                "You are a fashion trend researcher who monitors runway shows, social media, "
                "street style, and retail data. You specialize in identifying what's trending now "
                "and how trends flow from runways to TikTok to mainstream retail."
            ),
            llm=self.llm,
            tools=[_tavily, _trend_scraper],
            verbose=True,
        )

        self.cultural_expert = Agent(
            role="Fashion Historian & Cultural Analyst",
            goal=(
                "Provide cultural context for fashion in specific regions, historical evolution of styles, "
                "and travel-appropriate outfit guidance based on destination culture and customs."
            ),
            backstory=(
                "You are a fashion anthropologist who understands how clothing relates to culture, "
                "history, religion, and climate across the world. You give respectful, specific advice."
            ),
            llm=self.llm,
            tools=[_fashion_kb, _tavily],
            verbose=True,
        )

        self.style_advisor = Agent(
            role="Personal Fashion Stylist",
            goal=(
                "Generate specific, actionable outfit recommendations considering body type, "
                "color preferences, occasion, mood, budget, and context from other researchers. "
                "Always suggest complete outfits with specific items."
            ),
            backstory=(
                "You are a professional personal stylist who creates complete outfit recommendations. "
                "You understand color theory, body proportions, and occasion-appropriate dressing. "
                "You give specific suggestions — never vague advice."
            ),
            llm=self.llm,
            tools=[_fashion_kb, _brand_lookup],
            verbose=True,
        )

        self.synthesizer = Agent(
            role="Fashion Insights Editor",
            goal=(
                "Synthesize all research and recommendations into one cohesive, engaging, "
                "personalized response. Format with clear sections and actionable takeaways."
            ),
            backstory=(
                "You are a fashion editor who transforms complex research into engaging, practical advice. "
                "Your tone is like a knowledgeable friend — never robotic. You include brand ethics notes "
                "and always end with clear next steps."
            ),
            llm=self.llm,
            tools=[_brand_lookup],
            verbose=True,
        )

    def _build_tasks(self, query: str, user_profile: dict):
        profile_str = ", ".join(f"{k}: {v}" for k, v in user_profile.items() if v)

        self.route_task = Task(
            description=(
                f'Analyze this fashion query: "{query}"\n'
                f"User profile: {profile_str}\n\n"
                "Break it down into a structured research brief with: primary intent, "
                "sub-questions, recommended data sources, and user profile considerations."
            ),
            expected_output="A structured research brief with primary intent, sub-questions, data sources, and profile notes.",
            agent=self.query_router,
        )

        self.trends_task = Task(
            description=(
                "Based on the research brief, find current fashion trend information relevant to the query. "
                "Use web search and trend scraper tools. Be targeted — only research what's relevant."
            ),
            expected_output="A trend report with specific trend names, descriptions, key items, and sources.",
            agent=self.trend_researcher,
            context=[self.route_task],
        )

        self.culture_task = Task(
            description=(
                "Based on the research brief, provide cultural and historical fashion context. "
                "Use the Fashion Knowledge Base for curated data. Supplement with web search if needed. "
                "Be specific and respectful about cultural norms."
            ),
            expected_output="Cultural and historical fashion insights with dress code advice and local brand recommendations.",
            agent=self.cultural_expert,
            context=[self.route_task],
        )

        self.outfit_task = Task(
            description=(
                f"Generate personalized outfit recommendations.\nUser profile: {profile_str}\n\n"
                "Consider: body type, style preferences, budget, current trends, cultural context, "
                "color palettes, and occasion. For each outfit specify: items, colors, brands, prices, and why it works."
            ),
            expected_output="2-3 complete outfit recommendations with specific items, colors, brands, and styling tips.",
            agent=self.style_advisor,
            context=[self.route_task, self.trends_task, self.culture_task],
        )

        self.synthesize_task = Task(
            description=(
                "Synthesize all research into one cohesive, conversational response. "
                "Lead with the most relevant insight, include outfit recommendations, "
                "add trend context, note brand sustainability, and end with actionable next steps. "
                "Tone: knowledgeable friend, not a textbook."
            ),
            expected_output="A well-formatted, conversational response with personalized fashion insights and actionable next steps.",
            agent=self.synthesizer,
            context=[self.route_task, self.trends_task, self.culture_task, self.outfit_task],
        )

    def kickoff(self, inputs: dict) -> str:
        """Run the ooftd crew with the given query and user profile."""
        query = inputs.get("query", "")
        user_profile = inputs.get("user_profile", {})

        self._build_agents()
        self._build_tasks(query, user_profile)

        crew = Crew(
            agents=[
                self.query_router,
                self.trend_researcher,
                self.cultural_expert,
                self.style_advisor,
                self.synthesizer,
            ],
            tasks=[
                self.route_task,
                self.trends_task,
                self.culture_task,
                self.outfit_task,
                self.synthesize_task,
            ],
            process=Process.sequential,
            memory=True,
            verbose=True,
        )

        result = crew.kickoff()
        return result.raw if hasattr(result, "raw") else str(result)
