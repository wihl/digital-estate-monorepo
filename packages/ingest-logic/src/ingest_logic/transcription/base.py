from abc import ABC, abstractmethod

class TranscriptionProvider(ABC):
    @abstractmethod
    def transcribe(self, file_path: str) -> str:
        """
        Transcribes the given audio/video file.
        Returns the transcription text.
        """
        pass
