from error_translator.core import translate_error
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from importlib.metadata import version, PackageNotFoundError

try:
    VERSION = version("error-translator-cli-v2")
except PackageNotFoundError:
    VERSION = "unknown (not installed via pip)"

app = FastAPI(
    title="Error translator API",
    description="An API that translates Python errors into human-readable English.",
    version=VERSION
)
class ErrorRequest(BaseModel):
    traceback_setting: str

# API endpoint (existing functionality, unchanged)
@app.post("/translate")
def translation_endpoint(request: ErrorRequest):
    translation_result = translate_error(request.traceback_setting)
    return translation_result

# Serve the web UI at the root
@app.get("/")
def read_root():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "message": "Error translation API is running. Web UI not found. Please ensure static/index.html exists."
    }

# Health check (useful for monitoring)
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Mount static files directory (CSS, etc.)
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")