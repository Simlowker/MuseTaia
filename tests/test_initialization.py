from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app, main

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to SMOS v2 - Autonomous Muse Engine"}

def test_imports():
    import app.core
    import app.matrix
    import app.agents
    import app.state
    assert True

def test_main_help():
    """Test that main() displays help when no arguments are provided."""
    with patch("sys.argv", ["main.py"]):
        with patch("argparse.ArgumentParser.print_help") as mock_help:
            main()
            mock_help.assert_called_once()
