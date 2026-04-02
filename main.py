"""Voice Separator API entrypoint."""

import sys
from pathlib import Path

# Add src directory to Python path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import FastAPI application
from src.api import app

if __name__ == "__main__":
    import uvicorn

    print("Starting Voice Separator API...")
    print("Server: http://localhost:7860")
    print("Health: http://localhost:7860/health")
    print("Models: http://localhost:7860/models")
    print("Docs: http://localhost:7860/docs")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=7860,
        reload=True,
        reload_dirs=["src"]
    )
