import time
import logging
from typing import Dict, Any
from transformers import pipeline

logger = logging.getLogger("sentiment_model")
logging.basicConfig(level=logging.INFO)

DEFAULT_MODEL_NAME = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"


class SentimentClassifier:
    """
    Wrapper for Hugging Face sentiment analysis pipeline.
    Implements singleton-like model loading to avoid redundant model reloads on every request.
    """

    def __init__(self, model_name: str = DEFAULT_MODEL_NAME):
        self.model_name = model_name
        self.pipeline = None

    def load_model(self) -> None:
        """Loads model into memory if not already loaded."""
        if self.pipeline is None:
            logger.info("Loading model '%s' from Hugging Face Hub...", self.model_name)
            # Tải model vào bộ nhớ. Nếu chạy CPU thì device=-1 (mặc định)
            self.pipeline = pipeline(
                task="sentiment-analysis",
                model=self.model_name,
                framework="pt"
            )
            logger.info("Model '%s' successfully loaded and ready for inference.", self.model_name)

    def is_loaded(self) -> bool:
        """Checks if the model has been initialized."""
        return self.pipeline is not None

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Runs sentiment classification inference on the provided text.
        Returns label, confidence score, and inference time in milliseconds.
        """
        if not self.is_loaded():
            raise RuntimeError("Model pipeline has not been loaded.")

        start_time = time.perf_counter()
        raw_output = self.pipeline(text)
        elapsed_time_ms = (time.perf_counter() - start_time) * 1000

        # raw_output is a list like: [{'label': 'POSITIVE', 'score': 0.9998}]
        top_result = raw_output[0]

        return {
            "text": text,
            "label": top_result["label"],
            "confidence": round(float(top_result["score"]), 4),
            "elapsed_time_ms": round(elapsed_time_ms, 2)
        }


# Singleton instance across application
model_engine = SentimentClassifier()
