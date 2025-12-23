"""Manual verification script for Go Dispatcher & Snapshot Orchestration."""

import requests
import time
import threading

def trigger_dispatch(job_id):
    url = "http://localhost:8080/dispatch"
    payload = {
        "ID": f"job-{job_id}",
        "Intent": "produce cinematic visual",
        "MuseID": "muse-01"
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Request {job_id}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Request {job_id} failed: {e}")

def verify_dispatcher():
    print("--- Testing Go Dispatcher Concurrency ---")
    # Simulate a burst of 5 concurrent requests
    threads = []
    for i in range(5):
        t = threading.Thread(target=trigger_dispatch, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

    print("\n--- Testing Python Checkpoint Endpoint ---")
    try:
        # Assumes uvicorn app.main:app is running on 8000
        res = requests.get("http://localhost:8000/internal/checkpoint-ready")
        print(f"Python Checkpoint: {res.status_code} - {res.json()}")
    except Exception as e:
        print(f"Python Checkpoint failed (ensure server is running): {e}")

if __name__ == "__main__":
    verify_dispatcher()
