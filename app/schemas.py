from pydantic import BaseModel, Field
from typing import Optional


class SentimentRequest(BaseModel):
    """Schema for prediction request."""
    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The input text to analyze for sentiment.",
        json_schema_extra={"example": "FastAPI with Hugging Face is powerful and fun to use!"}
    )


class SentimentResponse(BaseModel):
    """Schema for prediction response."""
    text: str = Field(description="Original input text")
    label: str = Field(description="Predicted sentiment label (e.g., POSITIVE or NEGATIVE)")
    confidence: float = Field(description="Model prediction confidence score between 0.0 and 1.0")
    elapsed_time_ms: float = Field(description="Model inference execution time in milliseconds")


class HealthResponse(BaseModel):
    """Schema for system health check."""
    status: str = Field(description="Current status of the service (e.g., 'healthy', 'degraded')")
    model_name: str = Field(description="Identifier of the loaded Hugging Face model")
    model_loaded: bool = Field(description="Whether the machine learning model is ready in memory")
