import whisper
from .base import TranscriptionProvider
import os

class LocalWhisperProvider(TranscriptionProvider):
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self._model = None

    @property
    def model(self):
        if self._model is None:
            print(f"Loading Local Whisper model: {self.model_size}...")
            self._model = whisper.load_model(self.model_size)
        return self._model

    def transcribe(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        print(f"Transcribing {file_path} locally...")
        result = self.model.transcribe(file_path)
        return result["text"]
