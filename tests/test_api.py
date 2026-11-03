"""
Automated API Verification Script using `requests`.
Validates all endpoints required by Practice 01:
- GET /
- GET /health
- POST /predict (Valid positive & negative scenarios, and edge cases)
"""

import sys
import json
import requests

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://127.0.0.1:8000"


def banner(title: str):
    print("\n" + "=" * 65)
    print(f">> {title}")
    print("=" * 65)


def test_root_endpoint():
    banner("1. Testing GET / (System Introduction)")
    url = f"{BASE_URL}/"
    resp = requests.get(url, timeout=10)
    print(f"Status Code: {resp.status_code}")
    print("Response JSON:\n", json.dumps(resp.json(), indent=2, ensure_ascii=False))
    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}"
    data = resp.json()
    assert "service" in data and "endpoints" in data
    print("[PASS] GET / test passed.")


def test_health_endpoint():
    banner("2. Testing GET /health (Health & Model Status)")
    url = f"{BASE_URL}/health"
    resp = requests.get(url, timeout=10)
    print(f"Status Code: {resp.status_code}")
    print("Response JSON:\n", json.dumps(resp.json(), indent=2))
    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}"
    data = resp.json()
    assert data["status"] == "healthy", f"Service is not healthy: {data}"
    assert data["model_loaded"] is True, "Model is not marked as loaded"
    print("[PASS] GET /health test passed.")


def test_predict_positive():
    banner("3. Testing POST /predict (Positive Sentiment Case)")
    url = f"{BASE_URL}/predict"
    payload = {"text": "This course provides excellent practical experience and clear guidance!"}
    resp = requests.post(url, json=payload, timeout=15)
    print(f"Payload: {json.dumps(payload)}")
    print(f"Status Code: {resp.status_code}")
    print("Response JSON:\n", json.dumps(resp.json(), indent=2))
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    result = resp.json()
    assert result["label"] == "POSITIVE", f"Expected POSITIVE, got {result['label']}"
    assert result["confidence"] > 0.9, f"Expected high confidence, got {result['confidence']}"
    print(f"[PASS] Predict Positive passed (Label: {result['label']}, Score: {result['confidence']}).")


def test_predict_negative():
    banner("4. Testing POST /predict (Negative Sentiment Case)")
    url = f"{BASE_URL}/predict"
    payload = {"text": "The delivery was delayed, package was broken, and customer service was terrible."}
    resp = requests.post(url, json=payload, timeout=15)
    print(f"Payload: {json.dumps(payload)}")
    print(f"Status Code: {resp.status_code}")
    print("Response JSON:\n", json.dumps(resp.json(), indent=2))
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    result = resp.json()
    assert result["label"] == "NEGATIVE", f"Expected NEGATIVE, got {result['label']}"
    assert result["confidence"] > 0.9, f"Expected high confidence, got {result['confidence']}"
    print(f"[PASS] Predict Negative passed (Label: {result['label']}, Score: {result['confidence']}).")


def test_predict_empty_whitespace():
    banner("5. Testing POST /predict (Validation: Empty/Whitespace String)")
    url = f"{BASE_URL}/predict"
    payload = {"text": "    "}
    resp = requests.post(url, json=payload, timeout=10)
    print(f"Payload: {json.dumps(payload)}")
    print(f"Status Code: {resp.status_code} (Expected 400 Bad Request)")
    print("Response JSON:\n", json.dumps(resp.json(), indent=2, ensure_ascii=False))
    assert resp.status_code == 400, f"Expected 400 for empty whitespace text, got {resp.status_code}"
    print("[PASS] Validation test (empty whitespace) passed.")


def test_predict_missing_field():
    banner("6. Testing POST /predict (Validation: Missing Required Field)")
    url = f"{BASE_URL}/predict"
    payload = {}  # missing 'text' key
    resp = requests.post(url, json=payload, timeout=10)
    print(f"Payload: {json.dumps(payload)}")
    print(f"Status Code: {resp.status_code} (Expected 422 Unprocessable Entity)")
    print("Response JSON:\n", json.dumps(resp.json(), indent=2))
    assert resp.status_code == 422, f"Expected 422 for missing field, got {resp.status_code}"
    print("[PASS] Validation test (missing field) passed.")


def main():
    print(">> Starting API Verification Suite against", BASE_URL)
    try:
        test_root_endpoint()
        test_health_endpoint()
        test_predict_positive()
        test_predict_negative()
        test_predict_empty_whitespace()
        test_predict_missing_field()
        print("\n" + "*" * 65)
        print(">> ALL TESTS PASSED SUCCESSFULLY! (100% Endpoints Verified)")
        print("*" * 65 + "\n")
    except requests.exceptions.ConnectionError:
        print(f"\n[FAIL] Connection Error: Could not connect to {BASE_URL}.")
        print("Hint: Ensure you have started the server first:")
        print("   uvicorn app.main:app --reload")
        sys.exit(1)
    except AssertionError as ae:
        print(f"\n[FAIL] Assertion Failed: {str(ae)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

