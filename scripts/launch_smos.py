
import os
import subprocess
import time
import sys
from scripts.bootstrap_system import bootstrap

def launch():
    print("🚀 Launching Sovereign Muse OS (SMOS) v2...")
    
    # 1. Run Bootstrap
    print("\n[1/2] Bootstrapping System State...")
    try:
        bootstrap()
    except Exception as e:
        print(f"❌ Bootstrap failed: {e}")
        sys.exit(1)
        
    # 2. Start Uvicorn Server
    print("\n[2/2] Starting API Server (FastAPI)...")
    # Using sys.executable to ensure we use the same python interpreter
    cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 SMOS Shutdown requested.")
    except Exception as e:
        print(f"❌ Server crash: {e}")
        sys.exit(1)

if __name__ == "__main__":
    launch()
