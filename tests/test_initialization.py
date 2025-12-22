from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app, main

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to SMOS"}

def test_imports():
    import app.core
    import app.matrix
    import app.agents
    import app.state
    assert True

def test_main():
    with patch("uvicorn.run") as mock_run:
        main()
        mock_run.assert_called_once()
