"""Executable tools for the Sovereign Muse swarm, compatible with Gemini Tool Use."""

from typing import Dict, Any, List, Optional
from google.genai import types
from app.core.services.search_service import SearchService
from app.agents.narrative_agent import NarrativeAgent
from app.agents.visual_agent import VisualAgent
from app.agents.trend_scanner import TrendScanner
from app.state.db_access import StateManager

class SwarmToolbox:
    """Encapsulates swarm agents as tools for real-time orchestration."""

    def __init__(self):
        self.search_service = SearchService()
        self.narrative_agent = NarrativeAgent()
        self.visual_agent = VisualAgent()
        self.trend_scanner = TrendScanner()
        self.state_manager = StateManager()

    def get_tool_definitions(self) -> List[types.Tool]:
        """Returns the list of tool definitions for the Gemini API."""
        return [
            types.Tool(
                function_declarations=[
                    types.FunctionDeclaration(
                        name="search_web",
                        description="Searches the web for real-time information, news, and cultural trends.",
                        parameters=types.Schema(
                            type="OBJECT",
                            properties={
                                "query": types.Schema(type="STRING", description="The search query.")
                            },
                            required=["query"]
                        )
                    ),
                    types.FunctionDeclaration(
                        name="generate_narrative",
                        description="Generates a creative script and caption for a given topic based on the Muse's persona.",
                        parameters=types.Schema(
                            type="OBJECT",
                            properties={
                                "topic": types.Schema(type="STRING", description="The subject or idea for the script.")
                            },
                            required=["topic"]
                        )
                    ),
                    types.FunctionDeclaration(
                        name="generate_visual_asset",
                        description="Generates a high-fidelity image asset for the Muse's content bank.",
                        parameters=types.Schema(
                            type="OBJECT",
                            properties={
                                "prompt": types.Schema(type="STRING", description="Detailed description of the image to generate."),
                                "subject_id": types.Schema(type="STRING", description="Optional Muse ID for identity consistency.")
                            },
                            required=["prompt"]
                        )
                    ),
                    types.FunctionDeclaration(
                        name="analyze_trend",
                        description="Analyzes a specific trend topic against the Muse's moral graph and persona constraints.",
                        parameters=types.Schema(
                            type="OBJECT",
                            properties={
                                "topic": types.Schema(type="STRING", description="The trend topic to evaluate.")
                            },
                            required=["topic"]
                        )
                    )
                ]
            )
        ]

    async def execute_tool(self, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a tool by name with provided arguments."""
        if name == "search_web":
            result = self.search_service.search(args["query"])
            return {"result": result}
        
        elif name == "generate_narrative":
            mood = self.state_manager.get_mood()
            result = self.narrative_agent.generate_content(args["topic"], mood)
            return result.model_dump()
        
        elif name == "generate_visual_asset":
            prompt = args["prompt"]
            subject_id = args.get("subject_id")
            image_bytes = self.visual_agent.generate_image(prompt, subject_id=subject_id)
            return {"status": "success", "message": "Image generated and stored in memory."}
            
        elif name == "analyze_trend":
            result = self.trend_scanner.analyze_trend(args["topic"])
            return result.model_dump()
            
        else:
            raise ValueError(f"Unknown tool: {name}")
