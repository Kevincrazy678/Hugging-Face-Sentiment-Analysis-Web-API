# Hugging Face Sentiment Analysis Web API

## 1. Student Information

- **Full Name**: Nguyễn Phúc Gia Bảo
- **Student ID**: 25127018
- **Class**: 25C09, in Computational Class is 25C06
- **Email**: npgbao2521@clc.fitus.edu.vn

---

## 2. Selected Model

- **Model Identifier**: [`distilbert/distilbert-base-uncased-finetuned-sst-2-english`](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english)
- **Hugging Face Model Hub**: [https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english)
- **Task**: Binary Text Classification / Sentiment Analysis
- **Architecture**: DistilBERT (`DistilBertForSequenceClassification`)
- **Fine-tuning Dataset**: Stanford Sentiment Treebank (SST-2).

---

## 3. System Functionality & Architecture

The application is architected as a production-ready RESTful Web API built with **FastAPI** and **Hugging Face Transformers**.

### Key Architectural Highlights:
1. **Singleton Model Lifecycle (`lifespan`)**: The Transformer model is loaded into memory exactly once during application startup using FastAPI's modern `lifespan` context manager. This eliminates costly redundant disk/network I/O on inference requests, yielding low response latencies (~15–30 ms on CPU).
2. **Robust Input Validation**: Incoming payloads are validated against Pydantic schemas (`SentimentRequest`), enforcing non-empty strings, character boundaries, and proper JSON data types.
3. **Structured HTTP Exception Handling**: Graceful error handling with appropriate HTTP status codes (`400 Bad Request` for whitespace/empty strings, `422 Unprocessable Entity` for malformed payloads, and `500 Internal Server Error` for unexpected pipeline faults).

### API Endpoints Summary:
| HTTP Method | Route | Description |
| :--- | :--- | :--- |
| `GET` | `/` | System overview, model metadata, and endpoint directory. |
| `GET` | `/health` | Healthcheck probing service operational status and model readiness in RAM. |
| `POST` | `/predict` | Ingests input text, runs model inference, and returns sentiment prediction as JSON. |
| `GET` | `/docs` | Interactive Swagger UI (OpenAPI specification). |
| `GET` | `/redoc` | Alternative ReDoc documentation interface. |

---

## 4. Installation & Environment Setup

### Prerequisites
- Python 3.10 or higher.
- Git.

### Step-by-Step Setup:

1. **Clone the repository**:
   ```bash
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   cd W2
   ```
  For exam: git clone https://github.com/Kevincrazy678/Hugging-Face-Sentiment-Analysis-Web-API.git
  
2. **Create and activate a virtual environment**:
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
     *(If script execution is disabled, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*
   - **Windows (CMD)**:
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **macOS / Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 5. Running the Application

Start the local Uvicorn ASGI web server:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Once running:
- **Base URL**: `http://127.0.0.1:8000`
- **Interactive Swagger Documentation**: `http://127.0.0.1:8000/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

---

## 6. API Usage & Example Requests

### 6.1. System Introduction (`GET /`)
- **Request (cURL)**:
  ```bash
  curl -X 'GET' 'http://127.0.0.1:8000/'
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "service": "Sentiment Analysis Inference Service",
    "author": "HCMUS Student",
    "description": "Analyzes the emotional tone of English text (POSITIVE / NEGATIVE) with confidence scores.",
    "model": {
      "name": "distilbert/distilbert-base-uncased-finetuned-sst-2-english",
      "architecture": "DistilBERT (DistilbertForSequenceClassification)",
      "source": "https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    },
    "endpoints": {
      "GET /": "Service introduction and route documentation",
      "GET /health": "Health and operational status check",
      "POST /predict": "Submit text to perform sentiment classification",
      "GET /docs": "Interactive Swagger UI documentation",
      "GET /redoc": "Alternative ReDoc API documentation"
    }
  }
  ```

---

### 6.2. Health Check (`GET /health`)
- **Request (cURL)**:
  ```bash
  curl -X 'GET' 'http://127.0.0.1:8000/health'
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "status": "healthy",
    "model_name": "distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    "model_loaded": true
  }
  ```

---

### 6.3. Sentiment Prediction — Positive Example 
- **Request (cURL)**:
  ```bash
  curl -X 'POST' \
    'http://127.0.0.1:8000/predict' \
    -H 'Content-Type: application/json' \
    -d '{"text": "This course provides excellent practical experience and clear guidance!"}'
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "text": "This course provides excellent practical experience and clear guidance!",
    "label": "POSITIVE",
    "confidence": 0.9999,
    "elapsed_time_ms": 17.33
  }
  ```

---

### 6.4. Sentiment Prediction — Negative Example
- **Request (cURL)**:
  ```bash
  curl -X 'POST' \
    'http://127.0.0.1:8000/predict' \
    -H 'Content-Type: application/json' \
    -d '{"text": "The delivery was delayed, package was broken, and customer service was terrible."}'
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "text": "The delivery was delayed, package was broken, and customer service was terrible.",
    "label": "NEGATIVE",
    "confidence": 0.9998,
    "elapsed_time_ms": 20.47
  }
  ```

---

### 6.5. Automated Test Suite Execution
An automated test script using Python's `requests` library is provided under `tests/test_api.py`. To run all test cases (happy path and edge cases):

```bash
python tests/test_api.py
```

Expected output:
```text
>> Starting API Verification Suite against http://127.0.0.1:8000
>> 1. Testing GET / (System Introduction)            -> [PASS]
>> 2. Testing GET /health (Health & Model Status)    -> [PASS]
>> 3. Testing POST /predict (Positive Sentiment Case) -> [PASS]
>> 4. Testing POST /predict (Negative Sentiment Case) -> [PASS]
>> 5. Testing POST /predict (Validation: Empty Text) -> [PASS] (400 Bad Request)
>> 6. Testing POST /predict (Validation: Missing Key) -> [PASS] (422 Unprocessable)
>> ALL TESTS PASSED SUCCESSFULLY! (100% Endpoints Verified)
```

---

## 7. Demonstration Video

- **Video Link**: https://drive.google.com/file/d/1xH2rrlDyHww_3CTu3cXkKY-MoS_dLJdi/view?usp=sharing
- **Repo Link**: https://github.com/Kevincrazy678/Hugging-Face-Sentiment-Analysis-Web-API.git
