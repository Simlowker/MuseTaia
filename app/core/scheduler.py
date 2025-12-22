"""Scheduler for autonomous agent behaviors."""

import logging
from typing import List, Dict, Any
from app.agents.trend_scanner import TrendScanner
from app.core.workflow_engine import WorkflowEngine
from app.core.schemas.trend import RelevanceScore
from app.state.models import Mood

logger = logging.getLogger(__name__)

class ProactiveScheduler:
    """Manages autonomous scanning and triggering of content production."""

    def __init__(self):
        self.trend_scanner = TrendScanner()
        self.workflow_engine = WorkflowEngine()
        
        # Default topics to monitor
        self.interest_topics = [
            "Digital Fashion",
            "Generative AI Art",
            "Virtual Influencers",
            "Metaverse Events"
        ]

    def scan_and_activate(self, subject_id: str, current_mood: Mood) -> List[Dict[str, Any]]:
        """Scans interest topics and triggers production for high-relevance trends.

        Args:
            subject_id: The ID of the Muse.
            current_mood: The current mood of the Muse.

        Returns:
            List[Dict]: Results of any triggered workflows.
        """
        results = []
        
        logger.info(f"Starting proactive scan for {len(self.interest_topics)} topics...")
        
        for topic in self.interest_topics:
            logger.info(f"Analyzing topic: {topic}")
            report = self.trend_scanner.analyze_trend(topic)
            
            if report.relevance == RelevanceScore.HIGH:
                logger.info(f"HIGH relevance found for '{topic}'. Triggering production.")
                
                # Construct intent from trend analysis
                intent = f"Create content about {report.topic}. Context: {report.summary}. Sentiment: {report.sentiment}."
                
                try:
                    # Trigger the Magic Factory
                    production_result = self.workflow_engine.produce_video_content(
                        intent=intent,
                        mood=current_mood,
                        subject_id=subject_id
                    )
                    results.append({
                        "topic": topic,
                        "status": "produced",
                        "output": production_result
                    })
                except Exception as e:
                    logger.error(f"Production failed for '{topic}': {e}")
                    results.append({
                        "topic": topic,
                        "status": "failed",
                        "error": str(e)
                    })
            else:
                logger.info(f"Topic '{topic}' relevance: {report.relevance}. Skipping.")
                
        return results
