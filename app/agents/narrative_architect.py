"""Narrative Architect for structural scene decomposition and nodal workflow planning."""

from typing import Dict, Any, List
from app.agents.narrative_agent import NarrativeAgent, ScriptOutput
from app.state.models import Mood

class NarrativeArchitect(NarrativeAgent):
    """Agent that translates high-level scripts into nodal technical plans.
    
    This agent represents the 'Creative Studio Lobe'.
    It specializes in breaking down a narrative into 'Production Nodes' 
    compatible with ComfyUI and Veo.
    """

    def plan_production_nodes(self, script: ScriptOutput) -> List[Dict[str, Any]]:
        """Decomposes a script into nodes with retention-optimized pattern interrupts."""
        nodes = []
        
        # 1. Base Visual Gen
        nodes.append({
            "type": "visual_gen",
            "prompt": script.title,
            "params": {"vvs_boost": script.attention_dynamics.hook_intensity}
        })
        
        # 2. Pattern Interrupt Nodes (Every 8s)
        # We inject specific technical triggers based on attention_dynamics
        for i, interrupt in enumerate(script.attention_dynamics.pattern_interrupts):
            timestamp = (i + 1) * 8
            if timestamp < script.estimated_duration:
                nodes.append({
                    "type": "pattern_interrupt",
                    "trigger_time": timestamp,
                    "action": interrupt,
                    "severity": "high"
                })
        
        # 3. Motion & Final Delivery
        nodes.append({
            "type": "motion_gen",
            "duration": script.estimated_duration,
            "tempo_curve": script.attention_dynamics.tempo_curve
        })
        
        return nodes

