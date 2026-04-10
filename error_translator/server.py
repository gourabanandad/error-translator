from error_translator.core import translate_error
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI(
  title="Error translator API",
  description="An API that translates Python errors into human-readable English.",
  version='1.0.0'
)

class ErrorRequest(BaseModel):
  traceback_setting: str


@app.post("/translate")
def translation_endpoint(request: ErrorRequest):
  translation_result = translate_error(request.traceback_setting)
  return translation_result

@app.get('/')
def read_root():
  return {
    "message": "Error translation API is running"
  }