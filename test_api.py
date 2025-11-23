import requests
import json

# Test backend
try:
    response = requests.get("http://localhost:8000/health")
    print(f"Backend health check: {response.status_code} - {response.json()}")
except Exception as e:
    print(f"Backend not available: {e}")

# Test frontend
try:
    response = requests.get("http://localhost:5173")
    print(f"Frontend check: {response.status_code}")
except Exception as e:
    print(f"Frontend not available: {e}")