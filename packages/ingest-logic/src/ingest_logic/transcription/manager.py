import os
from .base import TranscriptionProvider
from .local_whisper import LocalWhisperProvider
from .gemini import GeminiProvider

class TranscriptionManager:
    def __init__(self, provider_type: str = None):
        # Default to local if not specified
        self.provider_type = provider_type or os.getenv("TRANSCRIPTION_PROVIDER", "local")
        self.provider = self._get_provider()

    def _get_provider(self) -> TranscriptionProvider:
        if self.provider_type == "gemini":
            return GeminiProvider()
        elif self.provider_type == "local":
            return LocalWhisperProvider()
        else:
            raise ValueError(f"Unknown transcription provider: {self.provider_type}")

    def transcribe(self, file_path: str) -> str:
        return self.provider.transcribe(file_path)
