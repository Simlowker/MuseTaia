"""Benchmark script to measure SMOS agent boot times."""

import time
import requests
import os

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
ENDPOINT = "/internal/checkpoint-ready"

def measure_boot_time(mode_name="Cold Start"):
    print(f"Starting benchmark for: {mode_name}")
    start_time = time.time()
    
    # Simple polling loop to simulate waiting for readiness
    retries = 0
    while retries < 60:
        try:
            response = requests.get(f"{API_URL}{ENDPOINT}")
            if response.status_code == 200:
                end_time = time.time()
                duration = end_time - start_time
                print(f"SUCCESS: {mode_name} ready in {duration:.2f} seconds.")
                return duration
        except:
            pass
        
        time.sleep(1)
        retries += 1
        
    print(f"FAILURE: {mode_name} timed out.")
    return None

if __name__ == "__main__":
    # In a real environment, we would trigger a Pod restart here
    measure_boot_time()
