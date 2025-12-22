"""Utility for optimizing and expanding prompts for image generation."""

import google.genai as genai
from google.genai import types
from app.core.config import settings

OPTIMIZER_SYSTEM_INSTRUCTION = """You are a Prompt Engineering expert for Imagen 3.
Your task is to take a simple scene description and expand it into a highly detailed, technical, and photorealistic prompt.

Follow these rules:
1. Specify lighting (e.g., golden hour, cinematic lighting, soft studio light).
2. Specify camera angle and lens (e.g., wide shot, 35mm lens, low angle).
3. Add descriptive adjectives for textures and atmosphere.
4. Maintain the core subject and action from the original prompt.
5. Focus on realism and high quality.
6. Do NOT include quality buzzwords like '8k' or 'masterpiece' unless they are part of a technical description.
7. Output ONLY the optimized prompt text.
"""

class PromptOptimizer:
    """Uses Gemini to transform simple descriptions into optimized image generation prompts."""

    def __init__(self, model_name: str = "gemini-3.0-flash-preview"):
        """Initializes the PromptOptimizer.

        Args:
            model_name: The Gemini model to use for rewriting.
        """
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name

    def optimize(self, simple_prompt: str) -> str:
        """Expands a simple prompt into an optimized technical prompt.

        Args:
            simple_prompt: The original simple description.

        Returns:
            str: The expanded technical prompt.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=f"Optimize this prompt for Imagen 3: {simple_prompt}")]
                )
            ],
            config=types.GenerateContentConfig(
                system_instruction=OPTIMIZER_SYSTEM_INSTRUCTION,
                temperature=0.7
            )
        )
        return response.text.strip()
