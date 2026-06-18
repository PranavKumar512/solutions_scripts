from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from app.utils.questions import solve_question  # Ensure this module exists
from mangum import Mangum
from pathlib import Path
import tempfile

# Read allowed origins from environment, default to repository homepage domain if not set
_allowed = os.environ.get("ALLOWED_ORIGINS")
if _allowed:
    ALLOWED_ORIGINS = [origin.strip() for origin in _allowed.split(",") if origin.strip()]
else:
    # Restrict to the known production origin by default
    ALLOWED_ORIGINS = ["https://solutions-scripts.vercel.app"]

app = FastAPI()

# Enable CORS with a restricted set of origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Ensure 'file' directory exists (used as storage for temporary uploads)
os.makedirs("file", exist_ok=True)


@app.get("/")
async def hello():
    return {"message": "Hello from Vercel"}


@app.post("/api/answers")
async def upload_file(
    question: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    file_location = None
    temp_path = None
    if file:
        # Sanitize filename to avoid path traversal
        filename = Path(file.filename).name
        # Use a secure temporary file to avoid predictable paths
        tmp = tempfile.NamedTemporaryFile(delete=False, dir="file", prefix="upload_", suffix="_" + filename)
        try:
            content = await file.read()
            tmp.write(content)
            tmp.flush()
            temp_path = tmp.name
            file_location = temp_path
        finally:
            tmp.close()

    # Call the solve_question function (Ensure it exists)
    result = await solve_question(question, file_location)

    # Clean up the uploaded file after processing
    if temp_path and os.path.exists(temp_path):
        try:
            os.remove(temp_path)
        except Exception:
            pass

    return result


# ✅ ASGI handler for Vercel
handler = Mangum(app)
