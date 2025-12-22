"""Main entry point for the Sovereign Muse OS (SMOS) API."""

from fastapi import FastAPI

app = FastAPI(title="Sovereign Muse OS (SMOS)")


@app.get("/")
def read_root() -> dict:
    """Returns a welcome message for the SMOS API.

    Returns:
        dict: A dictionary containing the welcome message.
    """
    return {"message": "Welcome to SMOS"}


def main():
    """Main function to run the application using uvicorn."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
