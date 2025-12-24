"""Manual verification script for Creative Studio Lobe (Architect, Virtuoso, Motion)."""

from app.agents.narrative_architect import NarrativeArchitect
from app.agents.visual_virtuoso import VisualVirtuoso
from app.agents.motion_engineer import MotionEngineer
from app.agents.narrative_agent import ScriptOutput, AttentionDynamics

def verify_studio_lobe():
    print("--- Verifying NarrativeArchitect ---")
    architect = NarrativeArchitect()
    script = ScriptOutput(
        title="Ephemeral Bloom",
        script="A digital flower blooming in a void.",
        caption="#digitalart",
        estimated_duration=4,
        attention_dynamics=AttentionDynamics(
            hook_intensity=0.8,
            pattern_interrupts=["flash"],
            tempo_curve=[0.5, 0.5]
        )
    )
    nodes = architect.plan_production_nodes(script)
    print(f"Planned Nodes: {[n['type'] for n in nodes]}")

    print("\n--- Verifying VisualVirtuoso ---")
    virtuoso = VisualVirtuoso()
    try:
        # Conceptual test of workflow generation
        prompt_id = virtuoso.generate_identity_image(
            prompt="A digital flower blooming in a void.",
            subject_id="muse-01"
        )
        print(f"ComfyUI Prompt ID: {prompt_id}")
    except Exception as e:
        print(f"VisualVirtuoso failed (likely no ComfyUI server): {e}")

    print("\n--- Verifying MotionEngineer ---")
    engineer = MotionEngineer()
    try:
        # Mock call to verify prompt construction logic
        video = engineer.execute_cinematic_handoff(b"start", b"end", "Transition between anchors")
        print("MotionEngineer logic executed (mocked result).")
    except Exception as e:
        print(f"MotionEngineer failed: {e}")

if __name__ == "__main__":
    verify_studio_lobe()
