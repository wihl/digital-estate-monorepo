import google.generativeai as genai
from .base import TranscriptionProvider
import os
import time

class GeminiProvider(TranscriptionProvider):
    def __init__(self, api_key: str = None, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        
        genai.configure(api_key=self.api_key)
        self.model_name = model_name

    def transcribe(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        print(f"Uploading {file_path} to Gemini...")
        video_file = genai.upload_file(path=file_path)
        
        # Wait for processing
        while video_file.state.name == "PROCESSING":
            print('.', end='', flush=True)
            time.sleep(2)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError(f"Gemini processing failed: {video_file.state.name}")

        print("\nRequesting transcription...")
        model = genai.GenerativeModel(model_name=self.model_name)
        
        # PROMPT: Derived from user requirement "one step transcription and translation"
        prompt = (
            "Please transcribe this audio file. "
            "If the audio is not in English, provide the original transcription first, "
            "followed by an English translation. Format clearly."
        )
        
        response = model.generate_content([video_file, prompt])
        
        # Cleanup? 
        # genai.delete_file(video_file.name) # Optional: auto-cleanup, but maybe we want to keep it briefly?
        # For now, let's delete to be clean.
        try:
             genai.delete_file(video_file.name)
        except:
             pass

        return response.text
