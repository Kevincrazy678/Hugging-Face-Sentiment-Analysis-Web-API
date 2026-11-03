import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas import SentimentRequest, SentimentResponse, HealthResponse
from app.model import model_engine

logger = logging.getLogger("api_main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager:
    Initializes and caches the Hugging Face model on application startup.
    """
    logger.info("Initializing Sentiment Analysis API server...")
    try:
        model_engine.load_model()
    except Exception as e:
        logger.error("Failed to load model during startup: %s", str(e))
    yield
    logger.info("Shutting down Sentiment Analysis API server...")


app = FastAPI(
    title="Hugging Face Sentiment Analysis API",
    description=(
        "Production-ready Web API deployed with FastAPI and Hugging Face Transformers. "
        "Performs real-time sentiment analysis on input text using DistilBERT."
    ),
    version="1.0.0",
    lifespan=lifespan
)


@app.get(
    "/",
    summary="System Introduction & API Capabilities",
    tags=["System"]
)
async def root():
    """
    Root endpoint:
    Returns system overview, model information, and a map of available endpoints.
    """
    return {
        "service": "Sentiment Analysis Inference Service",
        "author": "HCMUS Student",
        "description": "Analyzes the emotional tone of English text (POSITIVE / NEGATIVE) with confidence scores.",
        "model": {
            "name": model_engine.model_name,
            "architecture": "DistilBERT (DistilbertForSequenceClassification)",
            "source": f"https://huggingface.co/{model_engine.model_name}"
        },
        "endpoints": {
            "GET /": "Service introduction and route documentation",
            "GET /health": "Health and operational status check",
            "POST /predict": "Submit text to perform sentiment classification",
            "GET /docs": "Interactive Swagger UI documentation",
            "GET /redoc": "Alternative ReDoc API documentation"
        }
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Check Service Operational Status",
    tags=["System"]
)
async def health_check():
    """
    Health check endpoint:
    Verifies that the web service is alive and the Hugging Face model is resident in memory.
    """
    is_ready = model_engine.is_loaded()
    status_str = "healthy" if is_ready else "degraded"

    return HealthResponse(
        status=status_str,
        model_name=model_engine.model_name,
        model_loaded=is_ready
    )


@app.post(
    "/predict",
    response_model=SentimentResponse,
    status_code=status.HTTP_200_OK,
    summary="Classify Text Sentiment",
    tags=["Inference"]
)
async def predict(payload: SentimentRequest):
    """
    Prediction endpoint:
    - Receives text payload from the client.
    - Performs basic validation (checks for non-empty text).
    - Invokes model inference and returns the sentiment classification as structured JSON.
    """
    text = payload.text.strip()
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input text cannot be empty or contain only whitespace characters."
        )

    if not model_engine.is_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not ready. Please try again in a few moments."
        )

    try:
        result = model_engine.predict(text)
        return SentimentResponse(**result)
    except Exception as exc:
        logger.error("Inference failure for text '%s': %s", text, str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error encountered: {str(exc)}"
        )
