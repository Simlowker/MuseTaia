"""Sovereign Audio Service using Google Cloud Text-to-Speech (Studio Voices)."""

import logging
from typing import Optional
from google.cloud import texttospeech
from app.core.config import settings

logger = logging.getLogger(__name__)

class SovereignAudioService:
    """Service for generating the Muse's unique voice using Google Cloud TTS.
    
    Utilizes high-fidelity 'Studio' voices which provide natural prosody 
    and emotional depth comparable to ElevenLabs.
    """

    def __init__(self):
        try:
            self.client = texttospeech.TextToSpeechClient()
        except Exception as e:
            logger.error(f"AUDIO: Failed to initialize Google TTS Client: {e}")
            self.client = None

    def generate_voice(self, text: str, voice_name: str = "en-US-Studio-O") -> bytes:
        """Transforms text into the Muse's unique vocal timbre using Google Studio Voices."""
        logger.info(f"AUDIO: Synthesizing voice using Google Studio: {voice_name}")
        
        if not self.client:
            logger.warning("AUDIO: TTS Client not available. Returning silent placeholder.")
            return b"silent_audio_data"

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select the language code and the studio voice name
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=voice_name
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            effects_profile_id=["small-bluetooth-speaker-class-device"],
            pitch=0,
            speaking_rate=1.0
        )

        try:
            response = self.client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            return response.audio_content
        except Exception as e:
            logger.error(f"AUDIO: Google TTS Synthesis failed: {e}")
            return b"error_audio_data"